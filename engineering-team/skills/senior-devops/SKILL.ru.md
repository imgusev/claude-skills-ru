---
name: "senior-devops"
description: "Всесторонний скилл DevOps для CI/CD, автоматизации инфраструктуры, контейнеризации и облачных платформ (AWS, GCP, Azure). Включает в себя настройку пайплайна, инфраструктуру в виде кода, автоматизацию развертывания и мониторинг. Используется при настройке пайплайнов, деплою приложений, управлении инфраструктурой, внедрении мониторинга или оптимизации процессов развертывания."
---

# Старший разработчик { #senior-devops }

Полный набор инструментов для старших разработчиков с современными инструментами и лучшими практиками.

## Быстрый старт { #quick-start }

### Основные возможности { #main-capabilities }

Этот скилл предоставляет три основные возможности с помощью автоматизированных сценариев:

```bash
# Script 1: Pipeline Generator — scaffolds CI/CD pipelines for GitHub Actions or CircleCI
python scripts/pipeline_generator.py ./app --platform=github --stages=build,test,deploy

# Script 2: Terraform Scaffolder — generates and validates IaC modules for AWS/GCP/Azure
python scripts/terraform_scaffolder.py ./infra --provider=aws --module=ecs-service --verbose

# Script 3: Deployment Manager — generates deployment manifests + runbooks with rollback support
python3 scripts/deployment_manager.py deploy --env=staging --image=app:1.2.3 --strategy=blue-green --verbose --json
```

## Основные возможности { #core-capabilities }

### 1. Генератор пайплайна { #1-pipeline-generator }

Скаффолды обеспечивают конфигурацию пайплайна CI/CD для GitHub Actions или CircleCI с этапами сборки, тестирования, проверки безопасности и деплою.

**Пример — воркфлоу действий на GitHub:**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  build-docker:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    needs: build-docker
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service app-service \
            --force-new-deployment
```

**Использование:**
```bash
python scripts/pipeline_generator.py <project-path> --platform=github|circleci --stages=build,test,deploy
```

### 2. Строительные леса для терраформирования { #2-terraform-scaffolder }

Генерирует, проверяет и планирует модули Terraform. Обеспечивает согласованную структуру модуля и запускает `terraform validate` + `terraform plan` перед любым применением.

**Пример — сервисный модуль AWS ECS:**
```hcl
# modules/ecs-service/main.tf
resource "aws_ecs_task_definition" "app" {
  family                   = var.service_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.cpu
  memory                   = var.memory

  container_definitions = jsonencode([{
    name      = var.service_name
    image     = var.container_image
    essential = true
    portMappings = [{
      containerPort = var.container_port
      protocol      = "tcp"
    }]
    environment = [for k, v in var.env_vars : { name = k, value = v }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/${var.service_name}"
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "app" {
  name            = var.service_name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = var.service_name
    container_port   = var.container_port
  }
}
```

**Использование:**
```bash
python scripts/terraform_scaffolder.py <target-path> --provider=aws|gcp|azure --module=ecs-service|gke-deployment|aks-service [--verbose]
```

### 3. Менеджер развертывания { #3-deployment-manager }

Генерирует манифесты развертывания Kubernetes и упорядоченные рансбуки kubectl для стратегий "синий/зеленый" или "переходящий", с гейтами проверки работоспособности перед переключением трафика и откатом рансбуков. Инструмент записывает манифесты и печатает команды — он никогда не применяет их к самому кластеру, поэтому каждое изменение проходит ревью человека.

**Пример — развертывание Kubernetes синим/зеленым цветом (элементы, относящиеся к синему слоту):**
```yaml
# k8s/deployment-blue.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  labels:
    app: myapp
    slot: blue      # slot label distinguishes blue from green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      slot: blue
  template:
    metadata:
      labels:
        app: myapp
        slot: blue
    spec:
      containers:
        - name: app
          image: ghcr.io/org/app:1.2.3
          readinessProbe:       # gate: pod must pass before traffic switches
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

**Использование:**
```bash
python scripts/deployment_manager.py deploy \
  --env=staging|production \
  --image=app:1.2.3 \
  --strategy=blue-green|rolling \
  --health-check-url=https://app.example.com/healthz

python scripts/deployment_manager.py rollback --env=production --to-version=1.2.2
python scripts/deployment_manager.py --analyze --env=production   # audit current state
```

## Ресурсы { #resources }

- Ссылка на шаблон: `references/cicd_pipeline_guide.md` — подробные шаблоны CI/CD, лучшие практики, анти-шаблоны
- Руководство по воркфлоу: `references/infrastructure_as_code.md` — Пошаговые процессы IaC, оптимизация, устранение неполадок
- Техническое руководство: `references/deployment_strategies.md` — конфигурации стратегии развертывания, соображения безопасности, масштабируемость
- Инструментальные скрипты: `scripts/` каталог

## Воркфлоу-процесс разработки { #development-workflow }

### 1. Изменения инфраструктуры (Терраформирование) { #1-infrastructure-changes-terraform }

```bash
# Scaffold or update module
python scripts/terraform_scaffolder.py ./infra --provider=aws --module=ecs-service --verbose

# Validate and plan — review diff before applying
terraform -chdir=infra init
terraform -chdir=infra validate
terraform -chdir=infra plan -out=tfplan

# Apply only after plan review
terraform -chdir=infra apply tfplan

# Verify resources are healthy
aws ecs describe-services --cluster production --services app-service \
  --query 'services[0].{Status:status,Running:runningCount,Desired:desiredCount}'
```

### 2. Развертывание приложения { #2-application-deployment }

```bash
# Generate or update pipeline config
python scripts/pipeline_generator.py . --platform=github --stages=build,test,security,deploy

# Build and tag image
docker build -t ghcr.io/org/app:$(git rev-parse --short HEAD) .
docker push ghcr.io/org/app:$(git rev-parse --short HEAD)

# Deploy with health-check gate
python scripts/deployment_manager.py deploy \
  --env=production \
  --image=app:$(git rev-parse --short HEAD) \
  --strategy=blue-green \
  --health-check-url=https://app.example.com/healthz

# Verify pods are running
kubectl get pods -n production -l app=myapp
kubectl rollout status deployment/app-blue -n production

# Switch traffic after verification
kubectl patch service app-svc -n production \
  -p '{"spec":{"selector":{"slot":"blue"}}}'
```

### 3. Процедура отката { #3-rollback-procedure }

```bash
# Immediate rollback via deployment manager
python scripts/deployment_manager.py rollback --env=production --to-version=1.2.2

# Or via kubectl
kubectl rollout undo deployment/app -n production
kubectl rollout status deployment/app -n production

# Verify rollback succeeded
kubectl get pods -n production -l app=myapp
curl -sf https://app.example.com/healthz || echo "ROLLBACK FAILED — escalate"
```

## Перекрестные ссылки в нескольких облаках { #multi-cloud-cross-references }

Используйте эти сопутствующие скиллы для глубоких погружений в облаках:

| Скилл | Облако | Используйте, когда |
|-------|-------|----------|
| **aws-архитектор решений** | AWS | ECS/EKS, Лямбда, проектирование VPC, оптимизация затрат |
| **azure-облачный архитектор** | Лазурный | AKS, Служба приложений, виртуальные сети, Azure DevOps |
| **gcp-облачный архитектор** | GCP | GKE, Облачный запуск, VPC, облачная сборка * (скоро появится)* |

**Решение для нескольких облаков по сравнению с одним облаком:**
- **Единое облако** (по умолчанию) - меньшая сложность эксплуатации, более глубокая интеграция управляемых сервисов, лучшее соотношение затрат за счет скидок при обязательном использовании.
- ** Мультиоблачность** - требуется, когда это требуется в соответствии с требованиями законодательства / резидентства данных, при приобретении компаний в разных облаках или при необходимости предоставления лучших в своем классе услуг от разных поставщиков (например, AWS для compute + GCP для ML).
- **Гибрид** — on-prem + облако; используется, когда регулируемые рабочие нагрузки должны оставаться включенными, в то время как пакетные/ нечувствительные рабочие нагрузки выполняются в облаке.

> Запустите single-cloud. Добавляйте второе облако только тогда, когда есть конкретные бизнес—требования или требования соответствия требованиям - не для теоретической избыточности.

---

## Не зависящий от облаков IaC { #cloud-agnostic-iac }

### Terraform / OpenTofu (выбор по умолчанию) { #terraform--opentofu-default-choice }

Terraform (или его форк с открытым исходным кодом OpenTofu) является рекомендуемым инструментом IaC для большинства команд:
- Единый язык (HCL) для AWS, Azure, GCP и более 3000 провайдеров
- Управление состоянием с помощью удаленных бэкендов (S3, GCS, Azure Blob)
- Воркфлоу "Планируй перед применением" предотвращает неожиданные отклонения
- Перекрестные ссылки **шаблоны терраформирования** для структуры модуля, изоляции состояний и интеграции CI/CD

### Пулуми (язык программирования IaC) { #pulumi-programming-language-iac }

Выбирайте Pulumi, если команда отдает предпочтение TypeScript, Python, Go или C# перед HCL:
- Полноценный язык программирования — циклы, условные выражения, модульные тесты.
- Тот же охват облачных провайдеров, что и у Terraform
- Упрощенный онбординг для команд разработчиков, которые сопротивляются изучению HCL

### Когда использовать облачный IaC { #when-to-use-cloud-native-iac }

| Инструмент | Используйте, когда |
|------|----------|
| **Формирование облака** | Магазин только для AWS; требуется встроенная поддержка AWS (наборы пакетов, каталог сервисов) |
| **Бицепс** | Магазин только для Azure; синтаксис проще, чем у шаблонов ARM |
| **Менеджер облачного развертывания** | Только для GCP; редко — большинство команд GCP предпочитают Terraform |

> ** Эмпирическое правило: ** Используйте Terraform/OpenTofu, если вы на 100% не привязаны к одному облаку, а облачный инструмент предлагает функцию, которую Terraform не может воспроизвести (например, интеграцию с каталогом сервисов AWS).

---

## Устранение неполадок { #troubleshooting }

Ознакомьтесь с разделом "Комплексное устранение неполадок" в `references/deployment_strategies.md`.
