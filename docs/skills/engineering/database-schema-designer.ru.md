---
title: "Разработчик схемы базы данных { #database-schema-designer } — Агентский скилл для Codex и OpenClaw"
description: "Используется, когда пользователь запрашивает создание диаграмм ERD, нормализацию схем базы данных, проектирование связей таблиц или планирование. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Разработчик схемы базы данных { #database-schema-designer }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `database-schema-designer`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/database-schema-designer/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Уровень:** МОЩНЫЙ  
**Категория:** Инженерия  
**Домен:** Архитектура данных / Серверная часть  

---

## Обзор { #overview }

Разрабатывайте схемы реляционных баз данных на основе требований и генерируйте миграции, типы TypeScript/Python, исходные данные, политики RLS и индексы. Обрабатывает многопользовательскую работу, мягкое удаление, отслеживание аудита, управление версиями и полиморфные ассоциации.

## Основные возможности { #core-capabilities }

- **Разработка схемы** — нормализация требований в таблицах, связях, ограничениях
- **Миграционное поколение** — Морось, Призма, Типовая норма, перегонный куб
- **Генерация типов** — интерфейсы TypeScript, классы данных Python/модели Pydantic
- ** Политики RLS** — Безопасность на уровне строк для мультитенантных приложений
- **Индексная стратегия** — составные индексы, частичные индексы, охватывающие индексы
- ** Исходные данные** — реалистичная генерация тестовых данных
- **Генерация ERD** — Диаграмма русалки из схемы

---

## Когда использовать { #when-to-use }

- Разработка новой функции, для которой нужны таблицы базы данных
- Ревью схемы на предмет проблем с производительностью или нормализацией
- Добавление мультитенантности к существующей схеме
- Генерация типов TypeScript на основе схемы Prisma
- Планирование миграции схемы для кардинального изменения

---

## Процесс проектирования схемы { #schema-design-process }

### Шаг 1: Требования → Объекты { #step-1-requirements--entities }

Заданные требования:
> "Пользователи могут создавать проекты. У каждого проекта есть задачи. Задачи могут иметь ярлыки. Задачи могут быть назначены пользователям. Нам нужен полный отчет о аудите".

Извлекать объекты:
```
User, Project, Task, Label, TaskLabel (junction), TaskAssignment, AuditLog
```

### Шаг 2: Определите взаимосвязи { #step-2-identify-relationships }

```
User 1──* Project         (owner)
Project 1──* Task
Task *──* Label            (via TaskLabel)
Task *──* User            (via TaskAssignment)
User 1──* AuditLog
```

### Шаг 3: Добавьте сквозные проблемы { #step-3-add-cross-cutting-concerns }

- Многоквартирный дом: добавить `organization_id` ко всем таблицам, привязанным к клиенту
- Мягкое удаление: добавить `deleted_at TIMESTAMPTZ` вместо жесткого удаления
- Журнал аудита: добавить `created_by`, `updated_by`, `created_at`, `updated_at`
- Управление версиями: добавить `version INTEGER` для оптимистичной блокировки

---

## Пример полной схемы (SaaS для управления задачами) { #full-schema-example-task-management-saas }
→ Подробности смотрите в разделе references/full-schema-examples.md

## Политики безопасности на уровне строк (RLS) { #row-level-security-rls-policies }

```sql
-- Enable RLS
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Create app role
CREATE ROLE app_user;

-- Users can only see tasks in their organization's projects
CREATE POLICY tasks_org_isolation ON tasks
  FOR ALL TO app_user
  USING (
    project_id IN (
      SELECT p.id FROM projects p
      JOIN organization_members om ON om.organization_id = p.organization_id
      WHERE om.user_id = current_setting('app.current_user_id')::text
    )
  );

-- Soft delete: never show deleted records
CREATE POLICY tasks_no_deleted ON tasks
  FOR SELECT TO app_user
  USING (deleted_at IS NULL);

-- Only task creator or admin can delete
CREATE POLICY tasks_delete_policy ON tasks
  FOR DELETE TO app_user
  USING (
    created_by_id = current_setting('app.current_user_id')::text
    OR EXISTS (
      SELECT 1 FROM organization_members om
      JOIN projects p ON p.organization_id = om.organization_id
      WHERE p.id = tasks.project_id
        AND om.user_id = current_setting('app.current_user_id')::text
        AND om.role IN ('owner', 'admin')
    )
  );

-- Set user context (call at start of each request)
SELECT set_config('app.current_user_id', $1, true);
```

---

## Генерация исходных данных { #seed-data-generation }

```typescript
// db/seed.ts
import { faker } from '@faker-js/faker'
import { db } from './client'
import { organizations, users, projects, tasks } from './schema'
import { createId } from '@paralleldrive/cuid2'
import { hashPassword } from '../src/lib/auth'

async function seed() {
  console.log('Seeding database...')

  // Create org
  const [org] = await db.insert(organizations).values({
    id: createId(),
    name: "acme-corp",
    slug: 'acme',
    plan: 'growth',
  }).returning()

  // Create users
  const adminUser = await db.insert(users).values({
    id: createId(),
    email: 'admin@acme.com',
    name: "alice-admin",
    passwordHash: await hashPassword('password123'),
  }).returning().then(r => r[0])

  // Create projects
  const projectsData = Array.from({ length: 3 }, () => ({
    id: createId(),
    organizationId: org.id,
    ownerId: adminUser.id,
    name: "fakercompanycatchphrase"
    description: faker.lorem.paragraph(),
    status: 'active' as const,
  }))

  const createdProjects = await db.insert(projects).values(projectsData).returning()

  // Create tasks for each project
  for (const project of createdProjects) {
    const tasksData = Array.from({ length: faker.number.int({ min: 5, max: 20 }) }, (_, i) => ({
      id: createId(),
      projectId: project.id,
      title: faker.hacker.phrase(),
      description: faker.lorem.sentences(2),
      status: faker.helpers.arrayElement(['todo', 'in_progress', 'done'] as const),
      priority: faker.helpers.arrayElement(['low', 'medium', 'high'] as const),
      position: i * 1000,
      createdById: adminUser.id,
      updatedById: adminUser.id,
    }))

    await db.insert(tasks).values(tasksData)
  }

  console.log(`✅ Seeded: 1 org, ${projectsData.length} projects, tasks`)
}

seed().catch(console.error).finally(() => process.exit(0))
```

---

## Поколение ERD (Русалка) { #erd-generation-mermaid }

```
erDiagram
    Organization ||--o{ OrganizationMember : has
    Organization ||--o{ Project : owns
    User ||--o{ OrganizationMember : joins
    User ||--o{ Task : "created by"
    Project ||--o{ Task : contains
    Task ||--o{ TaskAssignment : has
    Task ||--o{ TaskLabel : has
    Task ||--o{ Comment : has
    Task ||--o{ Attachment : has
    Label ||--o{ TaskLabel : "applied to"
    User ||--o{ TaskAssignment : assigned

    Organization {
        string id PK
        string name
        string slug
        string plan
    }

    Task {
        string id PK
        string project_id FK
        string title
        string status
        string priority
        timestamp due_date
        timestamp deleted_at
        int version
    }
```

Генерировать из Prisma:
```bash
npx prisma-erd-generator
# or: npx @dbml/cli prisma2dbml -i schema.prisma | npx dbml-to-mermaid
```

---

## Распространенные подводные камни { #common-pitfalls }

- **Мягкое удаление без индекса** — `WHERE deleted_at IS NULL` без индекса = полное сканирование
- **Отсутствующие составные индексы** — `WHERE org_id = ? AND status = ?` нужен составной индекс
- **Изменяемые суррогатные ключи ** — никогда не используйте email или slug в качестве PK; используйте UUID/CUID
- **Не может быть обнулено без значения по умолчанию** — для добавления столбца NOT NULL в существующую таблицу требуется план по умолчанию или миграции
- ** Нет оптимистической блокировки** — одновременные обновления перезаписывают друг друга; добавить `version` колонна
- **RLS не протестирован** — всегда тестируйте RLS с ролью, не являющейся суперпользователем

---

## Лучшие практики { #best-practices }

1. ** Временные метки повсюду** — `created_at`, `updated_at` на каждом столе
2. **Мягкое удаление для проверяемых данных** — `deleted_at` вместо УДАЛЕНИЯ
3. **Журнал аудита соответствия требованиям ** — журнал до/после JSON для регулируемых доменов
4. **UUID или CUID как PKS** — избегайте последовательной утечки целых чисел
5. **Индексировать внешние ключи** — каждый столбец FK должен иметь индекс
6. **Частичные индексы** — использовать `WHERE deleted_at IS NULL` только для активных запросов
7. ** RLS поверх фильтрации на уровне приложения ** - база данных обеспечивает соблюдение условий аренды, а не только кода приложения
