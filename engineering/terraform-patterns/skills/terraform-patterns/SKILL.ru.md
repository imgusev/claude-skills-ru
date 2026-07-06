---
name: "terraform-patterns"
description: "Скилл агента Terraform infrastructure-as-code и плагин для Claude Code, Codex, Gemini CLI, Cursor, OpenClaw. Охватывает шаблоны проектирования модулей, стратегии управления состоянием, конфигурацию провайдера, усиление безопасности, политику в виде кода с помощью Sentinel/OPA и воркфлоу планирования/применения CI/CD. Используйте, когда: пользователь хочет разрабатывать модули Terraform, управлять бэкендами состояния, ревью безопасности Terraform, внедрять мультирегиональные развертывания или следовать рекомендациям IaC."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  updated: 2026-03-15
---

# Модели терраформирования { #terraform-patterns }

> Предсказуемая инфраструктура. Безопасное состояние. Модули, которые составляют. Никакого дрейфа.

Самоуверенный воркфлоу Terraform, который превращает обширный HCL в хорошо структурированный, безопасный инфраструктурный код производственного уровня. Охватывает проектирование модулей, управление состоянием, шаблоны поставщиков, усиление безопасности и интеграцию CI/CD.

Не учебник по терраформированию — набор конкретных решений о том, как написать инфраструктурный код, который не ломается в 3 часа ночи.

---

## Слэш-команды { #slash-commands }

| Команда | Что он делает |
|---------|-------------|
| `/terraform:review` | Проанализируйте код Terraform на наличие анти-шаблонов, проблем с безопасностью и структурой |
| `/terraform:module` | Спроектируйте или реорганизовайте модуль Terraform с надлежащими входами, выходами и композицией |
| `/terraform:security` | Аудит кода Terraform на наличие уязвимостей в системе безопасности, раскрытия секретов и неправильных настроек IAM |

---

## Когда активируется этот Скилл { #when-this-skill-activates }

Распознать эти шаблоны у пользователя:

- "Ревью этот код терраформирования"
- "Спроектируйте модуль терраформирования для..."
- "Мое состояние терраформирования - это..."
- "Настройка серверной части удаленного состояния"
- "Развертывание мультирегиональной терраформы"
- "Ревью безопасности Terraform"
- "Лучшие практики построения модульной структуры"
- "Пайплайн Terraform CI/CD"
- Любой запрос, связанный с: `.tf` файлы, HCL, модули Terraform, управление состоянием, конфигурация поставщика, инфраструктура как код

Если у пользователя есть `.tf` файлы или хочет предоставить инфраструктуру с помощью Terraform → применяется этот скилл.

---

## Воркфлоу { #workflow }

### `/terraform:review` — Ревью кода Terraform { #terraformreview--terraform-code-review }

1. **Анализ текущего состояния**
   - Прочитать все `.tf` файлы в целевом каталоге
   - Определить структуру модуля (плоская или вложенная)
   - Подсчитывайте ресурсы, источники данных, переменные, выходные данные
   - Проверьте соглашения об именовании

2. **Примените чек-лист для ревью-контроля review review**

   ```
   MODULE STRUCTURE
   ├── Variables have descriptions and type constraints
   ├── Outputs expose only what consumers need
   ├── Resources use consistent naming: {provider}_{type}_{purpose}
   ├── Locals used for computed values and DRY expressions
   └── No hardcoded values — everything parameterized or in locals

   STATE & BACKEND
   ├── Remote backend configured (S3, GCS, Azure Blob, Terraform Cloud)
   ├── State locking enabled (DynamoDB for S3, native for others)
   ├── State encryption at rest enabled
   ├── No secrets stored in state (or state access is restricted)
   └── Workspaces or directory isolation for environments

   PROVIDERS
   ├── Version constraints use pessimistic operator: ~> 5.0
   ├── Required providers block in terraform {} block
   ├── Provider aliases for multi-region or multi-account
   └── No provider configuration in child modules

   SECURITY
   ├── No hardcoded secrets, keys, or passwords
   ├── IAM follows least-privilege principle
   ├── Encryption enabled for storage, databases, secrets
   ├── Security groups are not overly permissive (no 0.0.0.0/0 ingress on sensitive ports)
   └── Sensitive variables marked with sensitive = true
   ```

3. **Сгенерировать отчет**
   ```bash
   python3 scripts/tf_module_analyzer.py ./terraform
   ```

4. **Запустить проверку безопасности**
   ```bash
   python3 scripts/tf_security_scanner.py ./terraform
   ```

### `/terraform:module` — Модульная конструкция { #terraformmodule--module-design }

1. **Определить область применения модуля**
   - Единая ответственность: один модуль = одна логическая группировка
   - Определите входные данные (переменные), выходные данные и границы ресурсов
   - Решите: плоский модуль (один каталог) или вложенный (вызывающий дочерние модули)

2. **Примените чек-лист по проектированию модуля design design**

   ```
   STRUCTURE
   ├── main.tf        — Primary resources
   ├── variables.tf   — All input variables with descriptions and types
   ├── outputs.tf     — All outputs with descriptions
   ├── versions.tf    — terraform {} block with required_providers
   ├── locals.tf      — Computed values and naming conventions
   ├── data.tf        — Data sources (if any)
   └── README.md      — Usage examples and variable documentation

   VARIABLES
   ├── Every variable has: description, type, validation (where applicable)
   ├── Sensitive values marked: sensitive = true
   ├── Defaults provided for optional settings
   ├── Use object types for related settings: variable "config" { type = object({...}) }
   └── Validate with: validation { condition = ... }

   OUTPUTS
   ├── Output IDs, ARNs, endpoints — things consumers need
   ├── Include description on every output
   ├── Mark sensitive outputs: sensitive = true
   └── Don't output entire resources — only specific attributes

   COMPOSITION
   ├── Root module calls child modules
   ├── Child modules never call other child modules
   ├── Pass values explicitly — no hidden data source lookups in child modules
   ├── Provider configuration only in root module
   └── Use module "name" { source = "./modules/name" }
   ```

3. **Создание каркаса модуля**
   - Структура выходного файла с шаблоном
   - Включать блоки проверки переменных
   - Добавьте правила жизненного цикла, где это уместно

### `/terraform:security` — Аудит безопасности { #terraformsecurity--security-audit }

1. **Аудит на уровне кода**

   | Проверьте | Серьезность | Исправить |
   |-------|----------|-----|
   | Жестко закодированные секреты в `.tf` файлы | Критический | Используйте переменные с sensitive = true или vault |
   | Политика IAM в отношении `*` действия | Критический | Сфера охвата конкретных действий и ресурсов |
   | Группа безопасности с 0.0.0.0/0 на порту 22/3389 | Критический | Ограничьтесь известными блоками CIDR или используйте SSM/bastion |
   | Корзина S3 без шифрования | Высокий | Добавить `server_side_encryption_configuration` блокировать |
   | Корзина S3 с общедоступным доступом | Высокий | Добавить `aws_s3_bucket_public_access_block` |
   | RDS без шифрования | Высокий | Набор `storage_encrypted = true` |
   | RDS общедоступен | Высокий | Набор `publicly_accessible = false` |
   | CloudTrail не включен | Средний | Добавить `aws_cloudtrail` ресурс |
   | Пропавший без вести `prevent_destroy` на ресурсах с сохранением состояния | Средний | Добавить `lifecycle { prevent_destroy = true }` |
   | Переменные без `sensitive = true` ради секретов | Средний | Добавить `sensitive = true` к секретным переменным |

2. **Аудит государственной безопасности**

   | Проверьте | Серьезность | Исправить |
   |-------|----------|-----|
   | Файл локального состояния | Критический | Переход на удаленный сервер с шифрованием |
   | Удаленное состояние без шифрования | Высокий | Включить шифрование на серверной части (SSE-S3, KMS) |
   | Отсутствие блокировки состояния | Высокий | Включите DynamoDB для S3, встроенную для TF Cloud |
   | Состояние, доступное для всех членов команды | Средний | Ограничение с помощью политик IAM или облачных команд TF |

3. **Создание отчета о безопасности**
   ```bash
   python3 scripts/tf_security_scanner.py ./terraform
   python3 scripts/tf_security_scanner.py ./terraform --output json
   ```

---

## Оснастка { #tooling }

### `scripts/tf_module_analyzer.py` { #scriptstf_module_analyzerpy }

Утилита CLI для анализа структуры каталогов Terraform и качества модулей.

**Особенности:**
- Подсчет ресурсов и источников данных
- Анализ переменных и выходных данных (отсутствующие описания, типы, проверка)
- Проверка соглашения об именовании
- Определение состава модуля
- Проверка файловой структуры
- Вывод JSON и текста

**Использование:**
```bash
# Analyze a Terraform directory
python3 scripts/tf_module_analyzer.py ./terraform

# JSON output
python3 scripts/tf_module_analyzer.py ./terraform --output json

# Analyze a specific module
python3 scripts/tf_module_analyzer.py ./modules/vpc
```

### `scripts/tf_security_scanner.py` { #scriptstf_security_scannerpy }

Утилита CLI для сканирования `.tf` файлы для решения распространенных проблем безопасности.

**Особенности:**
- Жестко запрограммированное обнаружение секретов (AWS-ключи, пароли, токены)
- Обнаружение чрезмерно разрешительной политики IAM
- Обнаружение открытой группы безопасности (0.0.0.0/0 для чувствительных портов)
- Пропущенные проверки шифрования (S3, RDS, EBS)
- Обнаружение общего доступа (S3, RDS, EC2)
- Аудит чувствительных переменных
- Вывод JSON и текста

**Использование:**
```bash
# Scan a Terraform directory
python3 scripts/tf_security_scanner.py ./terraform

# JSON output
python3 scripts/tf_security_scanner.py ./terraform --output json

# Strict mode (elevate warnings)
python3 scripts/tf_security_scanner.py ./terraform --strict
```

---

## Шаблоны проектирования модулей { #module-design-patterns }

### Образец 1: Плоский модуль (малые/средние проекты) { #pattern-1-flat-module-smallmedium-projects }

```
infrastructure/
├── main.tf          # All resources
├── variables.tf     # All inputs
├── outputs.tf       # All outputs
├── versions.tf      # Provider requirements
├── terraform.tfvars # Environment values (not committed)
└── backend.tf       # Remote state configuration
```

Лучше всего подходит для: одного приложения, < 20 ресурсов, одна команда владеет всем.

### Шаблон 2: Вложенные модули (средние/крупные проекты) { #pattern-2-nested-modules-mediumlarge-projects }

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf          # Calls modules with dev params
│   │   ├── backend.tf       # Dev state backend
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── compute/
│   │   └── ...
│   └── database/
│       └── ...
└── versions.tf
```

Лучше всего подходит для: нескольких сред, общих моделей инфраструктуры, совместной работы в команде.

### Шаблон 3: Моно-репозиторий с террагрунтом { #pattern-3-mono-repo-with-terragrunt }

```
infrastructure/
├── terragrunt.hcl           # Root config
├── modules/                  # Reusable modules
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── dev/
│   ├── terragrunt.hcl       # Dev overrides
│   ├── vpc/
│   │   └── terragrunt.hcl   # Module invocation
│   └── eks/
│       └── terragrunt.hcl
└── prod/
    ├── terragrunt.hcl
    └── ...
```

Лучше всего подходит для: крупномасштабных, многочисленных сред, сухой конфигурации, изоляции на уровне команды.

---

## Шаблоны конфигурации поставщика { #provider-configuration-patterns }

### Закрепление версии { #version-pinning }
```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"    # Allow 5.x, block 6.0
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

### Мультирегион с псевдонимами { #multi-region-with-aliases }
```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

resource "aws_s3_bucket" "primary" {
  bucket = "my-app-primary"
}

resource "aws_s3_bucket" "replica" {
  provider = aws.west
  bucket   = "my-app-replica"
}
```

### Множественная учетная запись с предполагаемой ролью { #multi-account-with-assume-role }
```hcl
provider "aws" {
  alias  = "production"
  region = "us-east-1"

  assume_role {
    role_arn = "arn:aws:iam::PROD_ACCOUNT_ID:role/TerraformRole"
  }
}
```

---

## Дерево решений по управлению состоянием { #state-management-decision-tree }

```
Single developer, small project?
├── Yes → Local state (but migrate to remote ASAP)
└── No
    ├── Using Terraform Cloud/Enterprise?
    │   └── Yes → TF Cloud native backend (built-in locking, encryption, RBAC)
    └── No
        ├── AWS?
        │   └── S3 + DynamoDB (encryption, locking, versioning)
        ├── GCP?
        │   └── GCS bucket (native locking, encryption)
        ├── Azure?
        │   └── Azure Blob Storage (native locking, encryption)
        └── Other?
            └── Consul or PostgreSQL backend

Environment isolation strategy:
├── Separate state files per environment (recommended)
│   ├── Option A: Separate directories (dev/, staging/, prod/)
│   └── Option B: Terraform workspaces (simpler but less isolation)
└── Single state file for all environments (never do this)
```

---

## Шаблоны интеграции CI/CD { #cicd-integration-patterns }

### План действий на GitHub/Применить { #github-actions-planapply }

```yaml
# .github/workflows/terraform.yml
name: Terraform
on:
  pull_request:
    paths: ['terraform/**']
  push:
    branches: [main]
    paths: ['terraform/**']

jobs:
  plan:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform validate
      - run: terraform plan -out=tfplan
      - run: terraform show -json tfplan > plan.json
      # Post plan as PR comment

  apply:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform apply -auto-approve
```

### Обнаружение дрейфа { #drift-detection }

```yaml
# Run on schedule to detect drift
name: Drift Detection
on:
  schedule:
    - cron: '0 6 * * 1-5'  # Weekdays at 6 AM

jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: |
          terraform plan -detailed-exitcode -out=drift.tfplan 2>&1 | tee drift.log
          EXIT_CODE=$?
          if [ $EXIT_CODE -eq 2 ]; then
            echo "DRIFT DETECTED — review drift.log"
            # Send alert (Slack, PagerDuty, etc.)
          fi
```

---

## Проактивные триггеры { #proactive-triggers }

Отмечайте их, не спрашивая:

- **Удаленный серверный сервер не настроен ** → Перейти на S3/GCS/Azure Blob-объект с блокировкой и шифрованием.
- **Поставщик без ограничения версии ** → Добавить `version = "~> X.0"` чтобы предотвратить сбой обновлений.
- **Жестко закодированные секреты в файлах .tf** → Использовать переменные с `sensitive = true`, или интегрировать Vault/SSM.
- **Политика IAM в отношении `"Action": "*"`** → Область применения для конкретных действий. Никаких действий с подстановочными знаками в процессе производства.
- **Группа безопасности открыта для 0.0.0.0/0 по SSH/RDP** → Ограничить доступ к bastion CIDR или использовать SSM Session Manager.
- **Нет блокировки состояния ** → Включите таблицу DynamoDB для серверной части S3 или используйте TF Cloud.
- **Ресурсы без тегов** → Добавьте default_tags в блок provider. Теги обязательны для отслеживания затрат.
- **Отсутствует `prevent_destroy` в базах данных/хранилище** → Добавить блок жизненного цикла для предотвращения случайного удаления.

---

## Конфигурация поставщика с несколькими облаками { #multi-cloud-provider-configuration }

Когда один корневой модуль должен быть подготовлен в AWS, Azure и GCP одновременно.

### Шаблон наложения псевдонимов поставщиком { #provider-aliasing-pattern }

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}
```

### Общие переменные для разных поставщиков { #shared-variables-across-providers }

```hcl
variable "environment" {
  description = "Environment name used across all providers"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod."
  }
}

locals {
  common_tags = {
    environment = var.environment
    managed_by  = "terraform"
    project     = var.project_name
  }
}
```

### Когда следует использовать Мультиоблачный { #when-to-use-multi-cloud }

- **Да**: Нормативные требования предписывают хранение данных у разных поставщиков, или организация имеет существующие рабочие нагрузки в нескольких облаках.
- **Нет**: само по себе "избегание привязки к поставщику" не является достаточным оправданием. Мультиоблачность удваивает сложность эксплуатации. Отдавайте предпочтение единому облаку, если только нет конкретных бизнес-требований.

---

## Совместимость с OpenTofu { #opentofu-compatibility }

OpenTofu - это форк Terraform с открытым исходным кодом, поддерживаемый Linux Foundation под лицензией MPL 2.0.

### Миграция с Terraform на OpenTofu { #migration-from-terraform-to-opentofu }

```bash
# 1. Install OpenTofu
brew install opentofu        # macOS
snap install --classic tofu  # Linux

# 2. Replace the binary — state files are compatible
tofu init                    # Re-initializes with OpenTofu
tofu plan                    # Identical plan output
tofu apply                   # Same apply workflow
```

### Соображения по поводу лицензии { #license-considerations }

| | Терраформирование (1.6+) | Открытый доступ |
|---|---|---|
| **Лицензия** | BSL 1.1 (источник - доступен) | MPL 2.0 (с открытым исходным кодом) |
| **Коммерческое использование** | Ограничено для конкурирующих продуктов | Неограниченный |
| **Управление сообществом** | Хашикорп | Основа Linux |

### Четность характеристик { #feature-parity }

OpenTofu отслеживает возможности Terraform 1.6.x. Ключевые дополнения, уникальные для OpenTofu:
- Шифрование состояния на стороне клиента (`tofu init -encryption`)
- Ранняя оценка переменных/локальных данных
- Функции, определяемые поставщиком

### Когда выбирать OpenTofu { #when-to-choose-opentofu }

- Вам нужна лицензия с полностью открытым исходным кодом для вашей цепочки поставок.
- Вам нужно шифрование состояния на стороне клиента без Terraform Cloud.
- В противном случае работает любой из инструментов — синтаксис HCL и экосистема провайдера идентичны.

---

## Интеграция Infracost { #infracost-integration }

Infracost оценивает затраты на облако на основе кода Terraform до выделения ресурсов.

### PR-воркфлоу { #pr-workflow }

```bash
# Show cost breakdown for current code
infracost breakdown --path .

# Compare cost difference between current branch and main
infracost diff --path . --compare-to infracost-base.json
```

### Комментарий о стоимости действий на GitHub { #github-actions-cost-comment }

```yaml
# .github/workflows/infracost.yml
name: Infracost
on: [pull_request]

jobs:
  cost:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}
      - run: infracost breakdown --path ./terraform --format json --out-file /tmp/infracost.json
      - run: infracost comment github --path /tmp/infracost.json --repo $GITHUB_REPOSITORY --pull-request ${{ github.event.pull_request.number }} --github-token ${{ secrets.GITHUB_TOKEN }} --behavior update
```

### Бюджетные пороговые значения и политика в области затрат { #budget-thresholds-and-cost-policy }

```yaml
# infracost.yml — policy file
version: 2.9.0
policies:
  - path: "*"
    max_monthly_cost: "5000"    # Fail PR if estimated cost exceeds $5,000/month
    max_cost_increase: "500"    # Fail PR if cost increase exceeds $500/month
```

---

## Импорт Существующей инфраструктуры { #import-existing-infrastructure }

Передайте созданные вручную ресурсы под управление Terraform.

### Воркфлоу импорта terraform { #terraform-import-workflow }

```bash
# 1. Write the resource block first (empty body is fine)
# main.tf:
# resource "aws_s3_bucket" "legacy" {}

# 2. Import the resource into state
terraform import aws_s3_bucket.legacy my-existing-bucket-name

# 3. Run plan to see attribute diff
terraform plan

# 4. Fill in the resource block until plan shows no changes
```

### Массовый импорт с генерацией конфигурации (Terraform 1.5+) { #bulk-import-with-config-generation-terraform-15 }

```bash
# Generate HCL for imported resources
terraform plan -generate-config-out=generated.tf

# Review generated.tf, then move resources into proper files
```

### Распространенные подводные камни { #common-pitfalls }

- **Смещение ресурса после импорта**: Импортированный ресурс может иметь атрибуты, которыми Terraform не управляет. Бежать `terraform plan` немедленно устраняйте все различия.
- **Манипулирование состоянием**: Используйте `terraform state mv` для переименования или реорганизации. Использование `terraform state rm` удалить, не разрушая. Всегда создавайте резервную копию состояния перед манипуляцией: `terraform state pull > backup.tfstate`.
- **Конфиденциальные значения по умолчанию**: Импортированные ресурсы могут раскрывать секреты в состоянии. Ограничьте доступ к состоянию и включите шифрование.

---

## Рельефные узоры { #terragrunt-patterns }

Terragrunt - это тонкая оболочка для Terraform, которая обеспечивает сухую конфигурацию для настройки в нескольких средах.

### Корневой terragrunt.hcl (общая конфигурация) { #root-terragrunthcl-shared-config }

```hcl
# terragrunt.hcl (root)
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "my-org-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Дочерний terragrunt.hcl (переопределение среды) { #child-terragrunthcl-environment-override }

```hcl
# prod/vpc/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../modules/vpc"
}

inputs = {
  environment = "prod"
  cidr_block  = "10.0.0.0/16"
}
```

### Зависимости между модулями { #dependencies-between-modules }

```hcl
# prod/eks/terragrunt.hcl
dependency "vpc" {
  config_path = "../vpc"
}

inputs = {
  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.private_subnet_ids
}
```

### Когда Террагрунт повышает ценность { #when-terragrunt-adds-value }

- **Да**: более 3 сред с идентичной структурой модулей, общей конфигурацией серверной части или межмодульными зависимостями.
- **Нет**: Единая среда, небольшая команда или простая изоляция на основе каталогов уже работают. Terragrunt добавляет кривую обучения и еще один двоичный файл для управления.

---

## Установка { #installation }

### Однострочник (любой инструмент) { #one-liner-any-tool }
```bash
git clone https://github.com/imgusev/claude-skills-ru.git
cp -r claude-skills-ru/engineering/terraform-patterns ~/.claude/skills/
```

### Установка с несколькими инструментами { #multi-tool-install }
```bash
./scripts/convert.sh --skill terraform-patterns --tool codex|gemini|cursor|windsurf|openclaw
```

### Открытый коготь { #openclaw }
```bash
clawhub install terraform-patterns
```

---

## Связанные скиллы { #related-skills }

- **старший-devops** — Более широкий охват DevOps (CI/CD, мониторинг, контейнеризация). Дополняющие друг друга — используйте шаблоны terraform для работы, специфичной для IaC, senior-devops для пайплайна и операций с инфраструктурой.
- **aws-solution-architect** — проектирование архитектуры AWS. Complementary — terraform-patterns реализует инфраструктуру, aws-solution-architect проектирует ее.
- **старший-безопасность** — Безопасность приложений. Дополнительные шаблоны terraform охватывают состояние безопасности инфраструктуры, senior-security охватывает угрозы прикладного уровня.
- **ci-cd-пайплайн-строитель** — строительство пайплайна. Дополнительные шаблоны terraform определяют инфраструктуру, ci-cd-пайплайн-builder автоматизирует развертывание.
