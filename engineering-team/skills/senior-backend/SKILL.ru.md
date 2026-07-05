---
name: "senior-backend"
description: Разрабатывает и внедряет серверные системы, включая REST API, микросервисы, архитектуры баз данных, потоки аутентификации и усиление безопасности. Используйте, когда пользователь просит "разработать REST API", "оптимизировать запросы к базе данных", "реализовать аутентификацию", "создать микросервисы", "ревью серверного кода", "настроить GraphQL", "обработать миграцию базы данных" или "API нагрузочного тестирования". Охватывает разработку Node.js/Express/Fastify, оптимизацию PostgreSQL, безопасность API и шаблоны серверной архитектуры.
---

# Старший серверный инженер { #senior-backend-engineer }

Шаблоны разработки серверной части, дизайн API, оптимизация баз данных и методы обеспечения безопасности.

---

## Быстрый старт { #quick-start }

```bash
# Generate API routes from OpenAPI spec
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/

# Analyze database schema and generate migrations
python scripts/database_migration_tool.py --connection postgres://localhost/mydb --analyze

# Load test an API endpoint
python scripts/api_load_tester.py https://api.example.com/users --concurrency 50 --duration 30
```

---

## Обзор инструментов { #tools-overview }

### 1. Каркас API { #1-api-scaffolder }

Генерирует обработчики маршрутов API, промежуточное программное обеспечение и спецификации OpenAPI на основе определений схем.

**Входные данные:** Спецификация OpenAPI (YAML/JSON) или схема базы данных
**Выходные данные:** Обработчики маршрутов, промежуточное программное обеспечение для проверки, типы TypeScript

**Использование:**
```bash
# Generate Express routes from OpenAPI spec
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/
# Output: Generated 12 route handlers, validation middleware, and TypeScript types

# Generate from database schema
python scripts/api_scaffolder.py --from-db postgres://localhost/mydb --output src/routes/

# Generate OpenAPI spec from existing routes
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml
```

**Поддерживаемые фреймворки:**
- Express.js (`--framework express`)
- Ускорять (`--framework fastify`)
- Коа (`--framework koa`)

---

### 2. Инструмент миграции базы данных { #2-database-migration-tool }

Анализирует схемы баз данных, обнаруживает изменения и генерирует файлы миграции с поддержкой отката.

**Входные данные:** Строка подключения к базе данных или файлы схемы
** Выходные данные:** Файлы миграции, отчет о разнице схем, предложения по оптимизации

**Использование:**
```bash
# Analyze current schema and suggest optimizations
python scripts/database_migration_tool.py --connection postgres://localhost/mydb --analyze
# Output: Missing indexes, N+1 query risks, and suggested migration files

# Generate migration from schema diff
python scripts/database_migration_tool.py --connection postgres://localhost/mydb \
  --compare schema/v2.sql --output migrations/

# Dry-run a migration
python scripts/database_migration_tool.py --connection postgres://localhost/mydb \
  --migrate migrations/20240115_add_user_indexes.sql --dry-run
```

---

### 3. Тестер загрузки API { #3-api-load-tester }

Выполняет нагрузочное тестирование HTTP с настраиваемым параллелизмом, измеряя процентили задержки и пропускную способность.

**Входные данные:** URL конечной точки API и тестовая конфигурация
** Выходные данные:** Отчет о производительности с распределением задержек, частотой ошибок, показателями пропускной способности

**Использование:**
```bash
# Basic load test
python scripts/api_load_tester.py https://api.example.com/users --concurrency 50 --duration 30
# Output: Throughput (req/sec), latency percentiles (P50/P95/P99), error counts, and scaling recommendations

# Test with custom headers and body
python scripts/api_load_tester.py https://api.example.com/orders \
  --method POST \
  --header "Authorization: Bearer token123" \
  --body '{"product_id": 1, "quantity": 2}' \
  --concurrency 100 \
  --duration 60

# Compare two endpoints
python scripts/api_load_tester.py https://api.example.com/v1/users https://api.example.com/v2/users \
  --compare --concurrency 50 --duration 30
```

---

## Воркфлоу разработки серверной части { #backend-development-workflows }

### Воркфлоу разработки API { #api-design-workflow }

Используйте при разработке нового API или рефакторинге существующих конечных точек.

**Шаг 1: Определите ресурсы и операции**
```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: User Service API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: "limit"
          in: query
          schema:
            type: integer
            default: 20
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
```

**Шаг 2: Сгенерируйте строительные леса маршрута**
```bash
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/
```

**Шаг 3: Внедрение бизнес-логики**
```typescript
// src/routes/users.ts (generated, then customized)
export const createUser = async (req: Request, res: Response) => {
  const { email, name } = req.body;

  // Add business logic
  const user = await userService.create({ email, name });

  res.status(201).json(user);
};
```

**Шаг 4: Добавьте промежуточное программное обеспечение для проверки**
```bash
# Validation is auto-generated from OpenAPI schema
# src/middleware/validators.ts includes:
# - Request body validation
# - Query parameter validation
# - Path parameter validation
```

**Шаг 5: Сгенерируйте обновленную спецификацию OpenAPI**
```bash
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml
```

---

### Воркфлоу по оптимизации базы данных { #database-optimization-workflow }

Используйте, когда запросы выполняются медленно или требуется улучшить производительность базы данных.

**Шаг 1: Проанализируйте текущую производительность**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
```

**Шаг 2: Определите медленные запросы**
```sql
-- Check query execution plans
EXPLAIN ANALYZE SELECT * FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 10;

-- Look for: Seq Scan (bad), Index Scan (good)
```

**Шаг 3: Сгенерируйте миграции индексов**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --suggest-indexes --output migrations/
```

**Шаг 4: Тестовая миграция (пробный запуск)**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/add_indexes.sql --dry-run
```

**Шаг 5: Подайте заявку и подтвердите**
```bash
# Apply migration
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/add_indexes.sql

# Verify improvement
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
```

---

### Повышение безопасности воркфлоу { #security-hardening-workflow }

Используйте при подготовке API к работе или после ревью безопасности.

**Шаг 1: Ревью настройки аутентификации**
```typescript
// Verify JWT configuration
const jwtConfig = {
  secret: process.env.JWT_SECRET,  // Must be from env, never hardcoded
  expiresIn: '1h',                 // Short-lived tokens
  algorithm: 'RS256'               // Prefer asymmetric
};
```

**Шаг 2: Добавьте ограничение скорости**
```typescript
import rateLimit from 'express-rate-limit';

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                   // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', apiLimiter);
```

**Шаг 3: Проверьте все входные данные**
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional()
});

// Use in route handler
const data = CreateUserSchema.parse(req.body);
```

**Шаг 4: Нагрузочный тест с использованием шаблонов атак**
```bash
# Test rate limiting
python scripts/api_load_tester.py https://api.example.com/login \
  --concurrency 200 --duration 10 --expect-rate-limit

# Test input validation
python scripts/api_load_tester.py https://api.example.com/users \
  --method POST \
  --body '{"email": "not-an-email"}' \
  --expect-status 400
```

**Шаг 5: Ревью заголовки безопасности**
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: true,
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: true,
  hsts: { maxAge: 31536000, includeSubDomains: true },
}));
```

---

## Справочная документация { #reference-documentation }

| Файл | Содержит | Используйте, когда |
|------|----------|----------|
| `references/api_design_patterns.md` | REST против GraphQL, управление версиями, обработка ошибок, разбивка на страницы | Разработка новых API |
| `references/database_optimization_guide.md` | Стратегии индексации, оптимизация запросов, N+1 решений | Исправление медленных запросов |
| `references/backend_security_practices.md` | Топ-10 OWASP, шаблоны аутентификации, проверка входных данных | Усиление безопасности |

---

## Краткий справочник по общим шаблонам { #common-patterns-quick-reference }

### Формат ответа REST API { #rest-api-response-format }
```json
{
  "data": { "id": 1, "name": "John" },
  "meta": { "requestId": "abc-123" }
}
```

### Формат ответа об ошибке { #error-response-format }
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [{ "field": "email", "message": "must be valid email" }]
  },
  "meta": { "requestId": "abc-123" }
}
```

### Коды состояния HTTP { #http-status-codes }
| Код | Вариант использования |
|------|----------|
| 200 | Успех (ПОЛУЧИТЬ, УСТАНОВИТЬ, ИСПРАВЛЯТЬ) |
| 201 | Создано (СООБЩЕНИЕ) |
| 204 | Нет содержимого (УДАЛИТЬ) |
| 400 | Ошибка проверки |
| 401 | Требуется аутентификация |
| 403 | В разрешении отказано |
| 404 | Ресурс не найден |
| 429 | Превышен лимит скорости |
| 500 | Внутренняя ошибка сервера |

### Стратегия индексирования базы данных { #database-index-strategy }
```sql
-- Single column (equality lookups)
CREATE INDEX idx_users_email ON users(email);

-- Composite (multi-column queries)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial (filtered queries)
CREATE INDEX idx_orders_active ON orders(created_at) WHERE status = 'active';

-- Covering (avoid table lookup)
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);
```

---

## Общие команды { #common-commands }

```bash
# API Development
python scripts/api_scaffolder.py openapi.yaml --framework express
python scripts/api_scaffolder.py src/routes/ --generate-spec

# Database Operations
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
python scripts/database_migration_tool.py --connection $DATABASE_URL --migrate file.sql

# Performance Testing
python scripts/api_load_tester.py https://api.example.com/endpoint --concurrency 50
python scripts/api_load_tester.py https://api.example.com/endpoint --compare baseline.json
```

---

## Допущения и поддающиеся проверке критерии успеха (дисциплина Карпатии) { #assumptions-and-verifiable-success-criteria-karpathy-discipline }

Прежде чем этот скилл сформирует каркас, порекомендует шаблон или изменит схему, необходимо выполнить следующие четыре допущения. Если какие-либо из них неизвестны, скилл останавливается и проходит по [Библиотека принудительных вопросов](#forcing-question-library-matt-pocock-grill) вместо этого.

1. **Соотношение чтения/записи + однолетний p99 QPS** — управляет базой данных, кэшем, очередью и выбором разделов. Клеппманн, *DDIA* (2017).
2. ** Модель аренды** — однопользовательская, совместно используемая мультитенантная, изолированная мультитенантная. Управляет шаблоном доступа к данным.
3. **Уровень конфиденциальности данных** — общедоступный / внутренний / PII / PHI / PCI. Управляет уровнем соответствия требованиям.
4. **SLO + именованная ошибка - бюджетный потребитель** — Канон Google SRE Workbook. Отсутствие SLO = отсутствие расстановки приоритетов в работе по обеспечению надежности.

**Поддающиеся проверке критерии успеха** (Карпатия №4) — каждая рекомендация, которую выдает этот скилл, должна включать:

- Целевые значения задержки (p50, p95, p99 в мс)
- Время безотказной работы / цель SLO
- RPO + RTO

Если какой—либо из этих трех параметров не указан, рекомендация является неполной - вернитесь к Q7 библиотеки принудительных вопросов.

Тот `scripts/backend_decision_engine.py` инструмент кодирует эти проверки: он отказывается рекомендовать профиль без соотношения чтение/запись + QPS + срок аренды + чувствительность к данным + предпочтение шаблона.

---

## Профили настройки { #customization-profiles }

Четыре встроенных профиля в `profiles/` откалибруйте каждую рекомендацию:

| Профиль | Когда выбирать | Узор | Минимальный уровень задержки (p99) |
|---|---|---|---|
| `node-express` | Команда TS, < 15 лет, английский, SaaS, ориентированный на клиента | Модульный монолит на Postgres | 600 мс |
| `fastapi-python` | Команда Python, < 20 человек, английский, ML-смежный | Модульный монолит на Postgres (асинхронный) | 500 мс |
| `django-monolith` | Контент-тяжелый CRUD + администратор, < 25 англ. | Модульный монолит на Postgres | 800 мс |
| `go-or-rust-microservice` | Извлеченный сервис, ≥ 30 англоязычных, команда платформы, QPS ≥ 1000 | Извлеченный сервис | 200 мс |

Выберите профиль с помощью:

```bash
python scripts/backend_decision_engine.py \
  --team-size 8 --qps-p99 50 --read-write-ratio 20 \
  --tenancy shared-multi-tenant --data-sensitivity pii \
  --pattern modular-monolith --language-preference typescript
```

Инструмент возвращает наиболее подходящий профиль, компромисс, занявший второе место (если он находится в пределах 15%), выбор стека, анти-шаблоны, именованные утверждающие и уровень SLO. **Этот инструмент никогда не одобряет автоматически.**

Чтобы добавить пользовательский профиль: скопируйте `profiles/node-express.json` к `profiles/<your-org>.json` и настраивать `constraints` + `success_thresholds` + `named_approver_chain`.

---

## Карта композиции { #composition-map }

Этот скилл не переопределяет область применения, которой владеют специалисты высокого уровня. Она разветвляется на них. Видишь `references/composition_map.md` для получения полной таблицы маршрутизации. Ключевые вилки:

| Беспокойство | Раскошелиться на |
|---|---|
| Риск нарушения контракта API /его изменения | `engineering/skills/api-design-reviewer/` |
| Разработка схемы + ERD + индексация | `engineering/skills/database-designer/` |
| Миграция схемы с нулевым временем простоя | `engineering/skills/migration-architect/` |
| SLO + SLI + ошибка-бюджет | `engineering/slo-architect/` |
| Наблюдаемость / золотые сигналы | `engineering/skills/observability-designer/` |
| Пайплайн CI/CD | `engineering/skills/ci-cd-pipeline-builder/` |
| Модель безопасности / угроз | `engineering-team/skills/senior-security/`, `adversarial-reviewer` |
| Доказательства соответствия (HIPAA /ISO 27001) | `ra-qm-team/` |
| Ревью перед совершением Карпатии | `engineering/karpathy-coder/` |
| Предполетный архитектурный гриль | `engineering/grill-me/` |

Тот `cs-backend-engineer` агент управляет этими разветвлениями с помощью `context: fork`. Вызовите его у другого агента с помощью `Agent({subagent_type: "cs-backend-engineer", prompt: "..."})` или через `/cs:backend-review <your problem>`.

---

## Библиотека форсирующих вопросов (Мэтт Покок Грилл) { #forcing-question-library-matt-pocock-grill }

Прежде чем заблокировать какое-либо серверное решение, ответьте на семь форсирующих вопросов в `references/forcing_questions.md` Дисциплина:

1. По одному вопросу за ход. Никакого связывания.
2. Всегда рекомендуйте ответ с цитируемым каноном.
3. Отслеживайте ответы в `/tmp/backend-grill-<date>.md`.
4. Если сработает критерий уничтожения, остановитесь. Не возводите каркасы вокруг неразрешенного пробела.
5. После Q7 запустите `backend_decision_engine.py` с семью ответами.

Краткое содержание:

1. Соотношение чтения/записи + прогноз p99 QPS?
2. Модель аренды — одиночная / общая / изолированная?
3. Синхронизация / асинхронность / управляемая событиями — по умолчанию + исключения?
4. Уровень чувствительности данных — PII/ PHI/ PCI?
5. Монолит / модульный монолит / микросервисы — обоснование размера команды?
6. RPO + RTO?
7. SLO + именованная ошибка - бюджетный потребитель?

---

## Обращение к другим агентам и скиллам { #invocation-from-other-agents-and-skills }

Три поверхности:

1. **Слэш-команда:** `/cs:backend-review <prompt>` — полный гриль + механизм принятия решений + маршрутизация состава.
2. **Агент-субагент:** `Agent({subagent_type: "cs-backend-engineer", prompt: "..."})` — разветвляет контекст, возвращает дайджест из ≤ 200 слов.
3. **Прямой вызов инструмента:** `python scripts/backend_decision_engine.py ...` — детерминированное совпадение профилей, когда известны входные данные.

Видишь `agents/engineering/cs-backend-engineer.md` для полного контракта на вызов.
