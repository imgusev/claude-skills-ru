---
name: "azure-cloud-architect"
description: "Разрабатывайте архитектуры Azure для стартапов и предприятий. Используйте, когда вас попросят спроектировать инфраструктуру Azure, создать шаблоны Bicep/ARM, оптимизировать затраты Azure, настроить пайплайны Azure DevOps или перейти на Azure. Охватывает AKS, службу приложений, функции Azure, Cosmos DB и оптимизацию затрат."
---

# Облачный архитектор Azure { #azure-cloud-architect }

Разрабатывайте масштабируемые, экономически эффективные архитектуры Azure для стартапов и предприятий с помощью шаблонов Bicep infrastructure-as-code.

---

## Воркфлоу { #workflow }

### Шаг 1: Соберите требования { #step-1-gather-requirements }

Сбор спецификаций приложений:

```
- Application type (web app, mobile backend, data pipeline, SaaS, microservices)
- Expected users and requests per second
- Budget constraints (monthly spend limit)
- Team size and Azure experience level
- Compliance requirements (GDPR, HIPAA, SOC 2, ISO 27001)
- Availability requirements (SLA, RPO/RTO)
- Region preferences (data residency, latency)
```

### Шаг 2: Проектирование архитектуры { #step-2-design-architecture }

Запустите конструктор архитектуры, чтобы получить рекомендации по шаблону:

```bash
python scripts/architecture_designer.py \
  --app-type web_app \
  --users 10000 \
  --requirements '{"budget_monthly_usd": 500, "compliance": ["SOC2"]}'
```

**Пример вывода:**

```json
{
  "recommended_pattern": "app_service_web",
  "service_stack": ["App Service", "Azure SQL", "Front Door", "Key Vault", "Entra ID"],
  "estimated_monthly_cost_usd": 280,
  "pros": ["Managed platform", "Built-in autoscale", "Deployment slots"],
  "cons": ["Less control than VMs", "Platform constraints", "Cold start on consumption plans"]
}
```

Выберите один из рекомендуемых шаблонов:
- ** Веб-служба приложений **: Входная дверь + Служба приложений + Azure SQL + кэш Redis
- **Микросервисы на AKS**: AKS + Служебная шина + База данных Cosmos + Управление API
- ** Бессерверное управление событиями**: Функции + Сетка событий + Служебная шина + База данных Cosmos
- ** Пайплайн данных**: Фабрика данных + Аналитика Synapse + Хранилище Data Lake + Центры событий

Видишь `references/architecture_patterns.md` для получения подробных спецификаций рисунка.

**Контрольная точка проверки:** Убедитесь, что рекомендуемый шаблон соответствует операционной зрелости команды и требованиям соответствия, прежде чем переходить к шагу 3.

### Шаг 3: Создайте шаблоны IaC { #step-3-generate-iac-templates }

Создайте инфраструктуру как код для выбранного шаблона:

```bash
# Web app stack (Bicep)
python scripts/bicep_generator.py --arch-type web-app --output main.bicep
```

**Пример вывода на бицепс (основные ресурсы веб-приложения):**

```bicep
@description('The environment name')
param environment string = 'dev'

@description('The Azure region for resources')
param location string = resourceGroup().location

@description('The application name')
param appName string = 'myapp'

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${environment}-${appName}-plan'
  location: location
  sku: {
    name: 'P1v3'
    tier: 'PremiumV3'
    capacity: 1
  }
  properties: {
    reserved: true // Linux
  }
}

// App Service
resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: '${environment}-${appName}-web'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      alwaysOn: true
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// Azure SQL Database
resource sqlServer 'Microsoft.Sql/servers@2023-05-01-preview' = {
  name: '${environment}-${appName}-sql'
  location: location
  properties: {
    administrators: {
      azureADOnlyAuthentication: true
    }
    minimalTlsVersion: '1.2'
  }
}

resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-05-01-preview' = {
  parent: sqlServer
  name: '${appName}-db'
  location: location
  sku: {
    name: 'GP_S_Gen5_2'
    tier: 'GeneralPurpose'
  }
  properties: {
    autoPauseDelay: 60
    minCapacity: json('0.5')
  }
}
```

> Полные шаблоны, включая входную дверь, хранилище ключей, управляемую идентификацию и мониторинг, создаются с помощью `bicep_generator.py` а также доступен в `references/architecture_patterns.md`.

**Bicep - рекомендуемый язык IaC для Azure.** Предпочитайте Bicep шаблонам ARM JSON: Bicep компилируется в ARM JSON, имеет более чистый синтаксис, поддерживает модули и поддерживается Microsoft от первого лица.

### Шаг 4: Ревью затрат { #step-4-review-costs }

Проанализируйте предполагаемые затраты и возможности оптимизации:

```bash
python scripts/cost_optimizer.py \
  --config current_resources.json \
  --json
```

**Пример вывода:**

```json
{
  "current_monthly_usd": 2000,
  "recommendations": [
    { "action": "Right-size SQL Database GP_S_Gen5_8 to GP_S_Gen5_2", "savings_usd": 380, "priority": "high" },
    { "action": "Purchase 1-year Reserved Instances for AKS node pools", "savings_usd": 290, "priority": "high" },
    { "action": "Move Blob Storage to Cool tier for objects >30 days old", "savings_usd": 65, "priority": "medium" }
  ],
  "total_potential_savings_usd": 735
}
```

Выходные данные включают в себя:
- Ежемесячная разбивка расходов по видам услуг
- Рекомендации по правильному подбору размера
- Зарезервированный экземпляр и возможности плана экономии
- Потенциальная ежемесячная экономия

### Шаг 5: Настройте CI/CD { #step-5-configure-cicd }

Настраивайте пайплайны Azure DevOps или действия GitHub с помощью Azure:

```yaml
# GitHub Actions — deploy Bicep to Azure
name: Deploy Infrastructure
on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - uses: azure/arm-deploy@v2
        with:
          resourceGroupName: rg-myapp-dev
          template: ./infra/main.bicep
          parameters: environment=dev
```

```yaml
# Azure DevOps Pipeline
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: AzureCLI@2
    inputs:
      azureSubscription: 'MyServiceConnection'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        az deployment group create \
          --resource-group rg-myapp-dev \
          --template-file infra/main.bicep \
          --parameters environment=dev
```

### Шаг 6: Ревью системы безопасности { #step-6-security-review }

Проверьте состояние безопасности перед началом производства:

- **Идентификация**: Entra ID (Azure AD) с RBAC, управляемая идентификация для авторизации от службы к службе - никогда не сохраняйте учетные данные в коде
- **Секреты**: Хранилище ключей для всех секретов, сертификатов и строк подключения
- **Сеть**: NSGS во всех подсетях, частные конечные точки для служб PaaS, шлюз приложений с WAF
- **Шифрование**: TLS 1.2+ в процессе передачи, ключи, управляемые Azure или клиентом, находятся в состоянии покоя
- **Мониторинг**: Включен защитник Microsoft для облака, политика Azure для защитных барьеров
- **Соответствие требованиям**: Назначения политик Azure для инициатив SOC 2 / HIPAA / ISO 27001

**В случае сбоя развертывания:**

1. Проверьте статус развертывания:
   ```bash
   az deployment group show \
     --resource-group rg-myapp-dev \
     --name main \
     --query 'properties.error'
   ```
2. Ревью журнал действий на наличие ошибок RBAC или политики.
3. Проверьте шаблон бицепса перед деплою:
   ```bash
   az bicep build --file main.bicep
   az deployment group validate \
     --resource-group rg-myapp-dev \
     --template-file main.bicep
   ```

**Распространенные причины сбоев:**
- Ошибки разрешений RBAC — убедитесь, что у участника, деплою которого выполняется развертывание, есть участник в группе ресурсов
- Поставщик ресурсов не зарегистрирован — запуск `az provider register --namespace Microsoft.Web`
- Конфликты именования — имена ресурсов Azure часто глобально уникальны (учетные записи хранилища, веб-приложения).
- Превышена квота — запросите увеличение квоты через портал Azure > Подписки > Использование + квоты

---

## Инструменты { #tools }

### architecture_designer.py { #architecture_designerpy }

Генерирует рекомендации по архитектурному шаблону на основе требований.

```bash
python scripts/architecture_designer.py \
  --app-type web_app \
  --users 50000 \
  --requirements '{"budget_monthly_usd": 1000, "compliance": ["HIPAA"]}' \
  --json
```

** Входные данные:** Тип приложения, ожидаемые пользователи, требования к JSON
** Выходные данные:** Рекомендуемый шаблон, набор услуг, оценка затрат, плюсы/cons

### cost_optimizer.py { #cost_optimizerpy }

Анализирует конфигурации ресурсов Azure для экономии средств.

```bash
python scripts/cost_optimizer.py --config resources.json --json
```

**Входные данные:** JSON-файл с текущей инвентаризацией ресурсов Azure
**Результат:** Рекомендации для:
- Удаление незанятых ресурсов
- Правильный размер виртуальной машины и базы данных
- Покупки зарезервированных экземпляров
- Переходы между уровнями хранения
- Неиспользуемые общедоступные IP-адреса и средства балансировки нагрузки

### bicep_generator.py { #bicep_generatorpy }

Генерирует каркасы шаблона бицепса из типа архитектуры.

```bash
python scripts/bicep_generator.py --arch-type microservices --output main.bicep
```

**Результат:** Готовые к производству шаблоны для бицепсов с:
- Управляемая идентификация (без паролей)
- Интеграция хранилища ключей
- Диагностические настройки для Azure Monitor
- Группы сетевой безопасности
- Теги для распределения затрат

---

## Быстрый старт { #quick-start }

### Архитектура веб-приложения (<100 долларов США/month) { #web-app-architecture--100month }

```
Ask: "Design an Azure web app for a startup with 5000 users"

Result:
- App Service (B1 Linux) for the application
- Azure SQL Serverless for relational data
- Azure Blob Storage for static assets
- Front Door (free tier) for CDN and routing
- Key Vault for secrets
- Estimated: $40-80/month
```

### Микросервисы на AKS ($500-2000/month) { #microservices-on-aks-500-2000month }

```
Ask: "Design a microservices architecture on Azure for a SaaS platform with 50k users"

Result:
- AKS cluster with 3 node pools (system, app, jobs)
- API Management for gateway and rate limiting
- Cosmos DB for multi-model data
- Service Bus for async messaging
- Azure Monitor + Application Insights for observability
- Multi-zone deployment
```

### Бессерверный, управляемый событиями (<200 долларов США/month) { #serverless-event-driven--200month }

```
Ask: "Design an event-driven backend for processing orders"

Result:
- Azure Functions (Consumption plan) for compute
- Event Grid for event routing
- Service Bus for reliable messaging
- Cosmos DB for order data
- Application Insights for monitoring
- Estimated: $30-150/month depending on volume
```

### Пайплайн передачи данных ($300-1500/month) { #data-pipeline-300-1500month }

```
Ask: "Design a data pipeline for ingesting 10M events/day"

Result:
- Event Hubs for ingestion
- Stream Analytics or Functions for processing
- Data Lake Storage Gen2 for raw data
- Synapse Analytics for warehouse
- Power BI for dashboards
```

---

## Входные требования { #input-requirements }

Предоставьте эти детали для архитектурного проектирования:

| Требование | Описание | Пример |
|-------------|-------------|---------|
| Тип приложения | То, что ты строишь | Платформа SaaS, мобильный сервер |
| Ожидаемый масштаб | Пользователи, запросы/sec | 10 тысяч пользователей, 100 RPS |
| Бюджет | Ежемесячный лимит Azure | $500/month макс. |
| Командный контекст | Размер, опыт работы в Azure | 3 разработчика, средний уровень |
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
  "azure_experience": "intermediate",
  "compliance": ["SOC2"],
  "availability_sla": "99.9%"
}
```

---

## Анти-паттерны { #anti-patterns }

| Анти-паттерн | Почему это терпит неудачу | Сделайте это вместо этого |
|---|---|---|
| Шаблоны ARM JSON для новых проектов | Многословный, трудночитаемый, без модулей | Используйте компиляцию Bicep для ARM, более чистый синтаксис |
| Хранение секретов в настройках приложения | Секреты видны в портале, вращения нет | Используйте ссылки на хранилище ключей в настройках приложения |
| Единый большой пул узлов AKS | Не удается оптимизировать для различных рабочих нагрузок | Используйте несколько пулов узлов: система, приложение, задания |
| Общедоступные конечные точки в службах PaaS | Открытая поверхность для атаки | Используйте частные конечные точки + интеграцию с виртуальной сетью |
| Избыточная подготовка "на всякий случай" | Растрачивает бюджет на первый месяц | Начните с малого, используйте автоматическое масштабирование, правильный размер ежемесячно |
| Общие группы ресурсов для всего | Радиус поражения, кошмары RBAC | Одна группа ресурсов для каждой среды и рабочей нагрузки |
| Отсутствие стратегии пометки | Не удается отследить затраты или право собственности | Тег: среда, владелец, центр затрат, название приложения |
| Использование классических ресурсов | Устаревшие, ограниченные функции | Используйте исключительно ресурсы РУК/бицепсов |

---

## Выходные форматы { #output-formats }

### Архитектурный дизайн { #architecture-design }

- Рекомендация по образцу с обоснованием
- Диаграмма стека служб (ASCII)
- Ежемесячная смета расходов и компромиссы

### Шаблоны IaC { #iac-templates }

- **Бицепс**: Рекомендуется — от первого лица, поддержка модулей, чистый синтаксис
- **ARM JSON**: Генерируется из бицепса, когда это необходимо
- **Terraform HCL**: Совместимость с несколькими облаками с использованием поставщика azurerm

### Анализ затрат { #cost-analysis }

- Разбивка текущих расходов с рекомендациями по оптимизации
- Список приоритетных действий (высокий/medium/low) и чек-лист по внедрению

---

## Перекрестные ссылки { #cross-references }

| Скилл | Отношения |
|-------|-------------|
| `engineering-team/aws-solution-architect` | Эквивалент AWS — тот же 6-шаговый воркфлоу, разные сервисы |
| `engineering-team/gcp-cloud-architect` | Эквивалент GCP — завершает облачный трифект |
| `engineering-team/senior-devops` | Более широкая сфера применения DevOps — пайплайны, мониторинг, контейнеризация |
| `engineering/terraform-patterns` | Реализация IaC — использование для модулей Terraform, ориентированных на Azure |
| `engineering/ci-cd-pipeline-builder` | Построение пайплайна — автоматизирует действия Azure DevOps и GitHub |

---

## Справочная документация { #reference-documentation }

| Документ | Содержание |
|----------|----------|
| `references/architecture_patterns.md` | 5 шаблонов: веб-приложение, микросервисы/AKS, бессерверный, пайплайн передачи данных, мультирегиональный |
| `references/service_selection.md` | Матрицы принятия решений для вычислений, баз данных, систем хранения данных, обмена сообщениями, создания сетей |
| `references/best_practices.md` | Соглашения об именовании, маркировка, RBAC, сетевая безопасность, мониторинг, DR |
