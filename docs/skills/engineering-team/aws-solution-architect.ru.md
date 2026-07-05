---
title: "Архитектор решений AWS { #aws-solution-architect } — Агентский скилл и плагин Codex"
description: "Разрабатывайте архитектуры AWS для стартапов, используя бессерверные шаблоны и шаблоны IaC. Используйте, когда вас попросят спроектировать. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Архитектор решений AWS { #aws-solution-architect }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `aws-solution-architect`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/aws-solution-architect/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Разрабатывайте масштабируемые и экономически эффективные архитектуры AWS для стартапов с использованием шаблонов "инфраструктура как код".

---

## Воркфлоу { #workflow }

### Шаг 1: Соберите требования { #step-1-gather-requirements }

Сбор спецификаций приложений:

```
- Application type (web app, mobile backend, data pipeline, SaaS)
- Expected users and requests per second
- Budget constraints (monthly spend limit)
- Team size and AWS experience level
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
  "service_stack": ["S3", "CloudFront", "API Gateway", "Lambda", "DynamoDB", "Cognito"],
  "estimated_monthly_cost_usd": 35,
  "pros": ["Low ops overhead", "Pay-per-use", "Auto-scaling"],
  "cons": ["Cold starts", "15-min Lambda limit", "Eventual consistency"]
}
```

Выберите один из рекомендуемых шаблонов:
- **Бессерверный Веб**: S3 + CloudFront + API Gateway + Lambda + DynamoDB
- **Микросервисы, управляемые событиями**: EventBridge + Лямбда + SQS + Пошаговые функции
- **Трехуровневый**: ALB + ECS Fargate + Aurora + ElastiCache
- **Серверная часть GraphQL**: AppSync + Lambda + DynamoDB + Cognito

Видишь `references/architecture_patterns.md` для получения подробных спецификаций рисунка.

**Контрольная точка проверки:** Убедитесь, что рекомендуемый шаблон соответствует операционной зрелости команды и требованиям соответствия, прежде чем переходить к шагу 3.

### Шаг 3: Создайте шаблоны IaC { #step-3-generate-iac-templates }

Создайте инфраструктуру как код для выбранного шаблона:

```bash
# Serverless stack (CloudFormation)
python scripts/serverless_stack.py --app-name my-app --region us-east-1
```

**Пример вывода CloudFormation YAML (основные бессерверные ресурсы):**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Parameters:
  AppName:
    Type: String
    Default: my-app

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs20.x
      MemorySize: 512
      Timeout: 30
      Environment:
        Variables:
          TABLE_NAME: !Ref DataTable
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref DataTable
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY

  DataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
```

> Полные шаблоны, включая API Gateway, Cognito, роли IAM и ведение журнала CloudWatch, создаются с помощью `serverless_stack.py` а также доступен в `references/architecture_patterns.md`.

**Пример фрагмента CDK TypeScript (трехуровневый шаблон):**

```typescript
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';

const vpc = new ec2.Vpc(this, 'AppVpc', { maxAzs: 2 });

const cluster = new ecs.Cluster(this, 'AppCluster', { vpc });

const db = new rds.ServerlessCluster(this, 'AppDb', {
  engine: rds.DatabaseClusterEngine.auroraPostgres({
    version: rds.AuroraPostgresEngineVersion.VER_15_2,
  }),
  vpc,
  scaling: { minCapacity: 0.5, maxCapacity: 4 },
});
```

### Шаг 4: Ревью затрат { #step-4-review-costs }

Проанализируйте предполагаемые затраты и возможности оптимизации:

```bash
python scripts/cost_optimizer.py --resources current_setup.json --monthly-spend 2000
```

**Пример вывода:**

```json
{
  "current_monthly_usd": 2000,
  "recommendations": [
    { "action": "Right-size RDS db.r5.2xlarge → db.r5.large", "savings_usd": 420, "priority": "high" },
    { "action": "Purchase 1-yr Compute Savings Plan at 40% utilization", "savings_usd": 310, "priority": "high" },
    { "action": "Move S3 objects >90 days to Glacier Instant Retrieval", "savings_usd": 85, "priority": "medium" }
  ],
  "total_potential_savings_usd": 815
}
```

Выходные данные включают в себя:
- Ежемесячная разбивка расходов по видам услуг
- Рекомендации по правильному подбору размера
- Возможности сберегательных планов
- Потенциальная ежемесячная экономия

### Шаг 5: Деплей { #step-5-deploy }

Деплою созданной инфраструктуры:

```bash
# CloudFormation
aws cloudformation create-stack \
  --stack-name my-app-stack \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM

# CDK
cdk deploy

# Terraform
terraform init && terraform apply
```

### Шаг 6: Проверка и обработка сбоев { #step-6-validate-and-handle-failures }

Проверьте развертывание и настройте мониторинг:

```bash
# Check stack status
aws cloudformation describe-stacks --stack-name my-app-stack

# Set up CloudWatch alarms
aws cloudwatch put-metric-alarm --alarm-name high-errors ...
```

**Если создание стека завершается неудачей:**

1. Проверьте причину сбоя:
   ```bash
   aws cloudformation describe-stack-events \
     --stack-name my-app-stack \
     --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]'
   ```
2. Ревью журналы CloudWatch на предмет лямбда-ошибок или ошибок ECS.
3. Исправьте шаблон или конфигурацию ресурса.
4. Удалите сбойный стек перед повторной попыткой:
   ```bash
   aws cloudformation delete-stack --stack-name my-app-stack
   # Wait for deletion
   aws cloudformation wait stack-delete-complete --stack-name my-app-stack
   # Redeploy
   aws cloudformation create-stack ...
   ```

**Распространенные причины сбоев:**
- Ошибки разрешения IAM → проверка `--capabilities CAPABILITY_IAM` и политики ролевого доверия
- Превышен лимит ресурсов → запросить увеличение квоты через консоль служебных квот
- Недопустимый синтаксис шаблона → выполнить `aws cloudformation validate-template --template-body file://template.yaml` перед деплою

---

## Инструменты { #tools }

### architecture_designer.py { #architecture_designerpy }

Генерирует архитектурные шаблоны на основе требований.

```bash
python scripts/architecture_designer.py --input requirements.json --output design.json
```

** Ввод:** JSON с указанием типа приложения, масштаба, бюджета, требований к соответствию
** Выходные данные:** Рекомендуемый шаблон, набор услуг, оценка затрат, плюсы/минусы

### serverless_stack.py { #serverless_stackpy }

Создает бессерверные шаблоны облачной информации.

```bash
python scripts/serverless_stack.py --app-name my-app --region us-east-1
```

**Результат:** Готовый к производству YAML CloudFormation с:
- API-шлюз + Лямбда
- Таблица DynamoDB
- Пул пользователей Cognito
- Роли IAM с наименьшими привилегиями
- Ведение журнала CloudWatch

### cost_optimizer.py { #cost_optimizerpy }

Анализирует затраты и рекомендует меры по оптимизации.

```bash
python scripts/cost_optimizer.py --resources inventory.json --monthly-spend 5000
```

**Результат:** Рекомендации для:
- Удаление незанятых ресурсов
- Правильный размер экземпляра
- Покупка зарезервированных мощностей
- Переходы между уровнями хранения
- Альтернативы шлюзу NAT

---

## Быстрый старт { #quick-start }

### Архитектура MVP (<100 долларов в месяц) { #mvp-architecture--100month }

```
Ask: "Design a serverless MVP backend for a mobile app with 1000 users"

Result:
- Lambda + API Gateway for API
- DynamoDB pay-per-request for data
- Cognito for authentication
- S3 + CloudFront for static assets
- Estimated: $20-50/month
```

### Масштабируемая архитектура (500-2000 долларов в месяц) { #scaling-architecture-500-2000month }

```
Ask: "Design a scalable architecture for a SaaS platform with 50k users"

Result:
- ECS Fargate for containerized API
- Aurora Serverless for relational data
- ElastiCache for session caching
- CloudFront for CDN
- CodePipeline for CI/CD
- Multi-AZ deployment
```

### Оптимизация затрат { #cost-optimization }

```
Ask: "Optimize my AWS setup to reduce costs by 30%. Current spend: $3000/month"

Provide: Current resource inventory (EC2, RDS, S3, etc.)

Result:
- Idle resource identification
- Right-sizing recommendations
- Savings Plans analysis
- Storage lifecycle policies
- Target savings: $900/month
```

### Поколение IaC { #iac-generation }

```
Ask: "Generate CloudFormation for a three-tier web app with auto-scaling"

Result:
- VPC with public/private subnets
- ALB with HTTPS
- ECS Fargate with auto-scaling
- Aurora with read replicas
- Security groups and IAM roles
```

---

## Входные требования { #input-requirements }

Предоставьте эти детали для архитектурного проектирования:

| Требование | Описание | Пример |
|-------------|-------------|---------|
| Тип приложения | То, что ты строишь | Платформа SaaS, мобильный сервер |
| Ожидаемый масштаб | Пользователи, запросы в секунду | 10 тысяч пользователей, 100 RPS |
| Бюджет | Ежемесячный лимит AWS | максимум 500 долларов в месяц |
| Командный контекст | Размер, опыт работы с AWS | 3 разработчика, средний уровень |
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
  "aws_experience": "intermediate",
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

- **CloudFormation YAML**: готовые к производству шаблоны SAM/CFN
- **CDK TypeScript**: Типобезопасный инфраструктурный код
- **Terraform HCL**: конфигурации, совместимые с несколькими облаками

### Анализ затрат { #cost-analysis }

- Разбивка текущих расходов с рекомендациями по оптимизации
- Список приоритетных действий (высокий/средний/низкий уровень) и чек-лист для реализации.

---

## Справочная документация { #reference-documentation }

| Документ | Содержание |
|----------|----------|
| `references/architecture_patterns.md` | 6 шаблонов: бессерверный, микросервисы, трехуровневый, обработка данных, GraphQL, мультирегиональный |
| `references/service_selection.md` | Матрицы принятия решений для вычислений, баз данных, хранилища, обмена сообщениями |
| `references/best_practices.md` | Бессерверный дизайн, оптимизация затрат, усиление безопасности, масштабируемость |
