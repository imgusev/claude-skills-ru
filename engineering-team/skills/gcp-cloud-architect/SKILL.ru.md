---
name: "gcp-cloud-architect"
description: "Разрабатывайте архитектуры GCP для стартапов и предприятий. Используйте, когда вас попросят спроектировать облачную инфраструктуру Google, деплою в GKE или Cloud Run, настроить пайплайны BigQuery, оптимизировать затраты на GCP или перейти на GCP. Охватывает облачный запуск, GKE, облачные функции, облачный SQL, BigQuery и оптимизацию затрат."
---

# Облачный архитектор GCP { #gcp-cloud-architect }

Разрабатывайте масштабируемые и экономически эффективные облачные архитектуры Google для стартапов и предприятий с помощью шаблонов "инфраструктура как код".

---

## Воркфлоу { #workflow }

### Шаг 1: Соберите требования { #step-1-gather-requirements }

Сбор спецификаций приложений:

```
- Application type (web app, mobile backend, data pipeline, SaaS)
- Expected users and requests per second
- Budget constraints (monthly spend limit)
- Team size and GCP experience level
- Compliance requirements (GDPR, HIPAA, SOC 2)
- Availability requirements (SLA, RPO/RTO)
```

### Шаг 2: Проектирование архитектуры { #step-2-design-architecture }

Запустите конструктор архитектуры, чтобы получить рекомендации по шаблону:

```bash
python scripts/architecture_designer.py --input requirements.json
```

**Пример вывода:**

```json
{
  "recommended_pattern": "serverless_web",
  "service_stack": ["Cloud Storage", "Cloud CDN", "Cloud Run", "Firestore", "Identity Platform"],
  "estimated_monthly_cost_usd": 30,
  "pros": ["Low ops overhead", "Pay-per-use", "Auto-scaling", "No cold starts on Cloud Run min instances"],
  "cons": ["Vendor lock-in", "Regional limitations", "Eventual consistency with Firestore"]
}
```

Выберите один из рекомендуемых шаблонов:
- ** Бессерверный Веб **: Облачное хранилище + Облачный CDN + Облачный запуск + Firestore
- **Микросервисы на GKE**: Автопилот GKE + облачный SQL + Хранилище памяти + Облачный Pub/Sub
- **Бессерверный пайплайн передачи данных**: Pub/Sub + Поток данных + BigQuery + Looker
- ** Платформа ML**: Vertex AI + облачное хранилище + BigQuery + облачные функции

Видишь `references/architecture_patterns.md` для получения подробных спецификаций рисунка.

**Контрольная точка проверки:** Убедитесь, что рекомендуемый шаблон соответствует операционной зрелости команды и требованиям соответствия, прежде чем переходить к шагу 3.

### Шаг 3: Оцените стоимость { #step-3-estimate-cost }

Проанализируйте предполагаемые затраты и возможности оптимизации:

```bash
python scripts/cost_optimizer.py --resources current_setup.json --monthly-spend 2000
```

**Пример вывода:**

```json
{
  "current_monthly_usd": 2000,
  "recommendations": [
    { "action": "Right-size Cloud SQL db-custom-4-16384 to db-custom-2-8192", "savings_usd": 380, "priority": "high" },
    { "action": "Purchase 1-yr committed use discount for GKE nodes", "savings_usd": 290, "priority": "high" },
    { "action": "Move Cloud Storage objects >90 days to Nearline", "savings_usd": 75, "priority": "medium" }
  ],
  "total_potential_savings_usd": 745
}
```

Выходные данные включают в себя:
- Ежемесячная разбивка расходов по видам услуг
- Рекомендации по правильному подбору размера
- Обязанный использовать возможности получения скидок
- Анализ скидок при длительном использовании
- Потенциальная ежемесячная экономия

Используйте [Калькулятор ценообразования GCP](https://cloud.google.com/products/calculator) для получения подробных оценок.

### Шаг 4: Сгенерируйте IaC { #step-4-generate-iac }

Создайте инфраструктуру как код для выбранного шаблона:

```bash
python scripts/deployment_manager.py --app-name my-app --pattern serverless_web --region us-central1
```

**Пример вывода Terraform HCL (облачный запуск + Firestore):**

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

resource "google_cloud_run_v2_service" "api" {
  name     = "${var.environment}-${var.app_name}-api"
  location = var.region

  template {
    containers {
      image = "gcr.io/${var.project_id}/${var.app_name}:latest"
      resources {
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
      }
      env {
        name  = "FIRESTORE_PROJECT"
        value = var.project_id
      }
    }
    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }
  }
}

resource "google_firestore_database" "default" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}
```

**Пример развертывания gcloud CLI:**

```bash
# Deploy Cloud Run service
gcloud run deploy my-app-api \
  --image gcr.io/$PROJECT_ID/my-app:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10

# Create Firestore database
gcloud firestore databases create --location=us-central1
```

> Полные шаблоны, включая облачный CDN, платформу идентификации, IAM и облачный мониторинг, создаются с помощью `deployment_manager.py` а также доступен в `references/architecture_patterns.md`.

### Шаг 5: Настройте CI/CD { #step-5-configure-cicd }

Настройте автоматическое развертывание с помощью действий Cloud Build или GitHub:

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA']

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-app-api'
      - '--image=gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'

images:
  - 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA'
```

```bash
# Connect repo and create trigger
gcloud builds triggers create github \
  --repo-name=my-app \
  --repo-owner=my-org \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

### Шаг 6: Ревью системы безопасности { #step-6-security-review }

Проверьте конфигурацию безопасности:

```bash
# Review IAM bindings
gcloud projects get-iam-policy $PROJECT_ID --format=json

# Check service account permissions
gcloud iam service-accounts list --project=$PROJECT_ID

# Verify VPC Service Controls (if applicable)
gcloud access-context-manager perimeters list --policy=$POLICY_ID
```

** Чек-лист по обеспечению безопасности (#):**
- Роли IAM имеют наименьшие привилегии (предпочитают предопределенные роли базовым)
- Учетные записи служб используют идентификатор рабочей нагрузки для GKE
- Элементы управления службами VPC, настроенные для чувствительных API
- Облачные ключи шифрования KMS для шифрования, управляемого клиентом
- Облачный аудит журналов включен для всех действий администратора
- Политики организации ограничивают общедоступный доступ
- Секретный менеджер, используемый для всех учетных данных

**В случае сбоя развертывания:**

1. Проверьте причину сбоя:
   ```bash
   gcloud run services describe my-app-api --region us-central1
   gcloud logging read "resource.type=cloud_run_revision" --limit=20
   ```
2. Ревью Облачный журнал на предмет ошибок приложений.
3. Исправьте конфигурацию или образ контейнера.
4. Повторно развернуть:
   ```bash
   gcloud run deploy my-app-api --image gcr.io/$PROJECT_ID/my-app:latest --region us-central1
   ```

**Распространенные причины сбоев:**
- Ошибки разрешения IAM - проверка ролей учетной записи службы и `--allow-unauthenticated` флаг
- Превышена квота -- запросить увеличение квоты через IAM & Admin > Квоты
- Ошибка запуска контейнера - проверьте журналы контейнера и конфигурацию проверки работоспособности
- Регион не включен - включите необходимые API с помощью `gcloud services enable`

---

## Инструменты { #tools }

### architecture_designer.py { #architecture_designerpy }

Рекомендует службы GCP на основе требований к рабочей нагрузке.

```bash
python scripts/architecture_designer.py --input requirements.json --output design.json
```

** Ввод:** JSON с указанием типа приложения, масштаба, бюджета, требований к соответствию
** Выходные данные:** Рекомендуемый шаблон, набор услуг, оценка затрат, плюсы/cons

### cost_optimizer.py { #cost_optimizerpy }

Анализирует ресурсы GCP для экономии средств.

```bash
python scripts/cost_optimizer.py --resources inventory.json --monthly-spend 5000
```

**Результат:** Рекомендации для:
- Удаление незанятых ресурсов
- Тип машины с правильным размером
- Обязательные скидки на использование
- Переходы между классами хранения
- Оптимизация выхода из сети

### deployment_manager.py { #deployment_managerpy }

Генерирует сценарии развертывания gcloud CLI и конфигурации Terraform.

```bash
python scripts/deployment_manager.py --app-name my-app --pattern serverless_web --region us-central1
```

**Результат:** Готовые к производству сценарии развертывания с:
- Запуск в облаке или развертывание GKE
- Настройка Firestore или Cloud SQL
- Конфигурация платформы идентификации
- Роли IAM с наименьшими привилегиями
- Облачный мониторинг и ведение журнала

---

## Быстрый старт { #quick-start }

### Веб-приложение для запуска в облаке (<100 долларов США/month) { #web-app-on-cloud-run--100month }

```
Ask: "Design a serverless web backend for a mobile app with 1000 users"

Result:
- Cloud Run for API (auto-scaling, no cold start with min instances)
- Firestore for data (pay-per-operation)
- Identity Platform for authentication
- Cloud Storage + Cloud CDN for static assets
- Estimated: $15-40/month
```

### Микросервисы на GKE ($500-2000/month) { #microservices-on-gke-500-2000month }

```
Ask: "Design a scalable architecture for a SaaS platform with 50k users"

Result:
- GKE Autopilot for containerized workloads
- Cloud SQL (PostgreSQL) with read replicas
- Memorystore (Redis) for session caching
- Cloud CDN for global delivery
- Cloud Build for CI/CD
- Multi-zone deployment
```

### Бессерверный пайплайн передачи данных { #serverless-data-pipeline }

```
Ask: "Design a real-time analytics pipeline for event data"

Result:
- Pub/Sub for event ingestion
- Dataflow (Apache Beam) for stream processing
- BigQuery for analytics and warehousing
- Looker for dashboards
- Cloud Functions for lightweight transforms
```

### Платформа ML { #ml-platform }

```
Ask: "Design a machine learning platform for model training and serving"

Result:
- Vertex AI for training and prediction
- Cloud Storage for datasets and model artifacts
- BigQuery for feature store
- Cloud Functions for preprocessing triggers
- Cloud Monitoring for model drift detection
```

---

## Входные требования { #input-requirements }

Предоставьте эти детали для архитектурного проектирования:

| Требование | Описание | Пример |
|-------------|-------------|---------|
| Тип приложения | То, что ты строишь | Платформа SaaS, мобильный сервер |
| Ожидаемый масштаб | Пользователи, запросы/sec | 10 тысяч пользователей, 100 RPS |
| Бюджет | Ежемесячный лимит GCP | $500/month макс. |
| Командный контекст | Размер, опыт работы в GCP | 3 разработчика, средний уровень |
| Соответствие требованиям | Нормативные потребности | HIPAA, GDPR, SOC 2 |
| Доступность | Требования к времени безотказной работы | 99,9% SLA, 1 час RPO |

**Формат JSON:**

```json
{
  "application_type": "saas_platform",
  "expected_users": 10000,
  "requests_per_second": 100,
  "budget_monthly_usd": 500,
  "team_size": 3,
  "gcp_experience": "intermediate",
  "compliance": ["SOC2"],
  "availability_sla": "99.9%"
}
```

---

## Выходные форматы { #output-formats }

### Архитектурный дизайн { #architecture-design }

- Рекомендация по образцу с обоснованием
- Диаграмма стека служб (ASCII)
- Ежемесячная смета расходов и компромиссы

### Шаблоны IaC { #iac-templates }

- **Terraform HCL**: готовые к производству конфигурации Google provider
- **gcloud CLI**: команды развертывания по сценарию
- **Облачная сборка YAML**: Определения пайплайна CI/CD

### Анализ затрат { #cost-analysis }

- Разбивка текущих расходов с рекомендациями по оптимизации
- Список приоритетных действий (высокий/medium/low) и чек-лист по внедрению

---

## Анти-паттерны { #anti-patterns }

| Анти-паттерн | Почему это терпит неудачу | Лучший подход |
|---|---|---|
| Использование VPC по умолчанию для производства | Никакой изоляции, общие правила брандмауэра | Создайте пользовательский VPC с частными подсетями |
| Избыточная подготовка пулов узлов GKE | Напрасные затраты на простаивающую мощность | Используйте автопилот GKE или кластерный автомасштабировщик |
| Хранение секретов в переменных окружения | Виден в облачной консоли, журналы | Используйте Secret Manager с идентификатором рабочей нагрузки |
| Игнорирование скидок на длительное использование | Недостающие 20-30% автоматической экономии | Виртуальные машины нужного размера для согласованного базового использования |
| Развертывание SaaS в одном регионе | Отключение в одном регионе = полное время простоя | Мультирегиональность с балансировкой нагрузки в облаке |
| Большой запрос по запросу для больших рабочих нагрузок | Непредсказуемые затраты в масштабах | Используйте слоты BigQuery (с фиксированной скоростью) для постоянной рабочей нагрузки |
| Запуск облачных функций для длительных задач | 9-минутный тайм-аут, холодный запуск | Используйте облачный запуск для задач продолжительностью более 60 секунд |

---

## Перекрестные ссылки { #cross-references }

| Скилл | Отношения |
|-------|-------------|
| `engineering-team/aws-solution-architect` | Эквивалент AWS — тот же 6-шаговый воркфлоу, разные сервисы |
| `engineering-team/azure-cloud-architect` | Эквивалент Azure — завершает облачный трифект |
| `engineering-team/senior-devops` | Более широкая сфера применения DevOps — пайплайны, мониторинг, контейнеризация |
| `engineering/terraform-patterns` | Реализация IaC — использование для модулей Terraform, ориентированных на GCP |
| `engineering/ci-cd-pipeline-builder` | Построение пайплайна — автоматизирует сборку и развертывание в облаке |

---

## Справочная документация { #reference-documentation }

| Документ | Содержание |
|----------|----------|
| `references/architecture_patterns.md` | 6 шаблонов: бессерверный, микросервисы GKE, трехуровневый, пайплайн передачи данных, платформа ML, мультирегиональный |
| `references/service_selection.md` | Матрицы принятия решений для вычислений, баз данных, хранилища, обмена сообщениями |
| `references/best_practices.md` | Именование, ярлыки, IAM, сетевое взаимодействие, мониторинг, аварийное восстановление |
