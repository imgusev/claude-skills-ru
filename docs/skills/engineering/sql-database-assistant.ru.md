---
title: "Помощник по работе с базами данных SQL - Скилл высокого уровня { #sql-database-assistant---powerful-tier-skill } — Агентский скилл для Codex и OpenClaw"
description: "Используйте, когда пользователь просит написать SQL-запросы, оптимизировать производительность базы данных, сгенерировать миграции, изучить схемы баз. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Помощник по работе с базами данных SQL - Скилл высокого уровня { #sql-database-assistant---powerful-tier-skill }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `sql-database-assistant`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/sql-database-assistant/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


## Обзор { #overview }

Оперативный помощник при проектировании баз данных. В то время как **database-designer** фокусируется на архитектуре схем, а **database-schema-designer** занимается моделированием ERD, этот скилл охватывает повседневную работу: написание запросов, оптимизацию производительности, генерацию миграций и преодоление разрыва между кодом приложения и ядрами баз данных.

### Основные возможности { #core-capabilities }

- ** Преобразование естественного языка в SQL** — преобразование требований в корректные, производительные запросы
- ** Исследование схемы ** — самоанализ действующих баз данных в PostgreSQL, MySQL, SQLite, SQL Server
- ** Оптимизация запросов** — ПОЯСНИТЕЛЬНЫЙ анализ, рекомендации по индексированию, обнаружение N+1, шаблоны перезаписи
- **Генерация миграции** — вверх/down сценарии, стратегии с нулевым временем простоя, планы отката
- **Интеграция ORM** — Шаблоны Prisma, Drizzle, TypeORM, SQLAlchemy и аварийные люки
- ** Поддержка нескольких баз данных ** — SQL с поддержкой диалектов и руководством по совместимости

### Инструменты { #tools }

| Сценарий | Цель |
|--------|---------|
| `scripts/query_optimizer.py` | Статический анализ SQL-запросов на предмет проблем с производительностью |
| `scripts/migration_generator.py` | Создание шаблонов файлов миграции на основе описаний изменений |
| `scripts/schema_explorer.py` | Генерировать документацию по схеме на основе запросов самоанализа |

---

## Естественный язык для SQL { #natural-language-to-sql }

### Шаблоны перевода { #translation-patterns }

При преобразовании требований в SQL следуйте этой последовательности:

1. **Идентификация сущностей** — сопоставление существительных с таблицами
2. ** Определение связей** — сопоставление глаголов с объединениями или подзапросами
3. **Определение фильтров** — сопоставление прилагательных/conditions к пунктам WHERE
4. ** Идентификация агрегаций** — сопоставьте "общее", "среднее", "количество" для ГРУППИРОВКИ ПО
5. ** Определить порядок заказа ** — сопоставить "верхний", "последний", "самый высокий" для заказа ПО + ЛИМИТУ

### Распространенные шаблоны запросов { #common-query-templates }

**Top-N для каждой группы (функция окна)**
```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
  FROM employees
) ranked WHERE rn <= 3;
```

**Текущие итоги**
```sql
SELECT date, amount,
  SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM transactions;
```

**Обнаружение зазоров**
```sql
SELECT curr.id, curr.seq_num, prev.seq_num AS prev_seq
FROM records curr
LEFT JOIN records prev ON prev.seq_num = curr.seq_num - 1
WHERE prev.id IS NULL AND curr.seq_num > 1;
```

**UPSERT (PostgreSQL)**
```sql
INSERT INTO settings (key, value, updated_at)
VALUES ('theme', 'dark', NOW())
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = EXCLUDED.updated_at;
```

**UPSERT (MySQL)**
```sql
INSERT INTO settings (key_name, value, updated_at)
VALUES ('theme', 'dark', NOW())
ON DUPLICATE KEY UPDATE value = VALUES(value), updated_at = VALUES(updated_at);
```

> Смотрите ссылки/query_patterns.md для объединений, CTE, оконных функций, операций JSON и многого другого.

---

## Исследование схемы { #schema-exploration }

### Запросы к самоанализу { #introspection-queries }

**PostgreSQL — список таблиц и столбцов**
```sql
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```

**PostgreSQL — внешние ключи**
```sql
SELECT tc.table_name, kcu.column_name,
  ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

**MySQL — размеры таблиц**
```sql
SELECT table_name, table_rows,
  ROUND(data_length / 1024 / 1024, 2) AS data_mb,
  ROUND(index_length / 1024 / 1024, 2) AS index_mb
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY data_length DESC;
```

**SQLite — дамп схемы**
```sql
SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name;
```

**SQL Server — столбцы с типами**
```sql
SELECT t.name AS table_name, c.name AS column_name,
  ty.name AS data_type, c.max_length, c.is_nullable
FROM sys.columns c
JOIN sys.tables t ON c.object_id = t.object_id
JOIN sys.types ty ON c.user_type_id = ty.user_type_id
ORDER BY t.name, c.column_id;
```

### Создание документации на основе схемы { #generating-documentation-from-schema }

Использование `scripts/schema_explorer.py` для создания документации по Markdown или JSON:

```bash
python scripts/schema_explorer.py --dialect postgres --tables all --format md
python scripts/schema_explorer.py --dialect mysql --tables users,orders --format json --json
```

---

## Оптимизация запросов { #query-optimization }

### ОБЪЯСНИТЕ воркфлоу-процесс анализа { #explain-analysis-workflow }

1. **Запустите EXPLAIN ANALYZE** (PostgreSQL) или **EXPLAIN FORMAT=JSON** (MySQL)
2. ** Определите самый дорогостоящий узел** — Seq-сканирование больших таблиц, вложенный цикл с высокими оценками строк
3. **Проверка отсутствующих индексов** — последовательное сканирование отфильтрованных столбцов
4. ** Ищите ошибки оценки ** — расхождение запланированных и фактических строк указывает на устаревшую статистику
5. **Оцените порядок соединения ** — убедитесь, что наименьший результирующий набор управляет соединением

### Чек-лист рекомендаций по индексации (Index Recommendation) { #index-recommendation-checklist }

- Столбцы в предложениях WHERE с высокой избирательностью
- Столбцы в условиях соединения (внешние ключи)
- Столбцы в порядке следования в сочетании с LIMIT
- Составные индексы, соответствующие многоколоночным предикатам WHERE (сначала наиболее выборочный столбец)
- Частичные индексы для запросов с постоянными фильтрами (например, `WHERE status = 'active'`)
- Охватывающие индексы, чтобы избежать поиска в таблицах для запросов, требующих большого объема чтения

### Шаблоны перезаписи запросов { #query-rewriting-patterns }

| Анти-паттерн | Переписать |
|-------------|---------|
| `SELECT * FROM orders` | `SELECT id, status, total FROM orders` (явные столбцы) |
| `WHERE YEAR(created_at) = 2025` | `WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'` (саркастичный) |
| Коррелированный подзапрос в SELECT | ЛЕВОЕ СОЕДИНЕНИЕ с агрегацией |
| `NOT IN (SELECT ...)` с нулями | `NOT EXISTS (SELECT 1 ...)` |
| `UNION` (дедупликация), когда в этом нет необходимости | `UNION ALL` |
| `LIKE '%search%'` | Индекс полнотекстового поиска (GIN/FULLTEXT) |
| `ORDER BY RAND()` | Случайная выборка на стороне приложения или `TABLESAMPLE` |

### Обнаружение N+1 { #n1-detection }

**Симптомы:**
- Цикл приложения, выполняющий по одному запросу для каждой родительской строки
- ORM - отложенная загрузка связанных объектов внутри цикла
- Журнал запросов показывает сотни идентичных шаблонов выбора с разными идентификаторами

**Исправления:**
- Используйте ускоренную загрузку (`include` в Призме, `joinedload` в SQLAlchemy)
- Пакетные запросы с `WHERE id IN (...)`
- Используйте шаблон DataLoader для распознавателей GraphQL

### Инструмент статического анализа { #static-analysis-tool }

```bash
python scripts/query_optimizer.py --query "SELECT * FROM orders WHERE status = 'pending'" --dialect postgres
python scripts/query_optimizer.py --query queries.sql --dialect mysql --json
```

> Смотрите ссылки/optimization_guide.md для объяснения чтения плана, типов индексов и объединения подключений.

---

## Миграционное поколение { #migration-generation }

### Схемы миграции с нулевым временем простоя { #zero-downtime-migration-patterns }

**Добавление столбца (безопасно)**
```sql
-- Up
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Down
ALTER TABLE users DROP COLUMN phone;
```

**Переименование столбца (развернуть-сжать)**
```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
-- Step 2: Backfill
UPDATE users SET full_name = name;
-- Step 3: Deploy app reading both columns
-- Step 4: Deploy app writing only new column
-- Step 5: Drop old column
ALTER TABLE users DROP COLUMN name;
```

**Добавление столбца NOT NULL (безопасная последовательность)**
```sql
-- Step 1: Add nullable
ALTER TABLE orders ADD COLUMN region VARCHAR(50);
-- Step 2: Backfill with default
UPDATE orders SET region = 'unknown' WHERE region IS NULL;
-- Step 3: Add constraint
ALTER TABLE orders ALTER COLUMN region SET NOT NULL;
ALTER TABLE orders ALTER COLUMN region SET DEFAULT 'unknown';
```

**Создание индекса (неблокирующий, PostgreSQL)**
```sql
CREATE INDEX CONCURRENTLY idx_orders_status ON orders (status);
```

### Стратегии обратного заполнения данных { #data-backfill-strategies }

- ** Пакетные обновления ** — обрабатываются порциями по 1000-10000 строк, чтобы избежать конфликта блокировок
- ** Фоновые задания** — асинхронное выполнение обратных заполнений с отслеживанием прогресса
- **Двойная запись** — запись в старый и новый столбцы во время переходного периода
- ** Запросы проверки ** — проверяйте количество строк и целостность данных после каждого пакета

### Стратегии отката { #rollback-strategies }

Каждая миграция должна иметь обратимый нисходящий сценарий. Для необратимых изменений:

1. **Резервное копирование перед выполнением** — `pg_dump` затронутые таблицы
2. **Фич-флаги** — приложение может переключаться между старыми/new схема считывает
3. **Теневые таблицы** — сохраняйте копию исходной таблицы во время окна миграции

### Инструмент для генерации миграции { #migration-generator-tool }

```bash
python scripts/migration_generator.py --change "add email_verified boolean to users" --dialect postgres --format sql
python scripts/migration_generator.py --change "rename column name to full_name in customers" --dialect mysql --format alembic --json
```

---

## Поддержка нескольких баз данных { #multi-database-support }

### Диалектные различия { #dialect-differences }

| Особенность | PostgreSQL | MySQL | SQLite | SQL Server |
|---------|-----------|-------|--------|------------|
| ВСТАВЛЯТЬ | `ON CONFLICT DO UPDATE` | `ON DUPLICATE KEY UPDATE` | `ON CONFLICT DO UPDATE` | `MERGE` |
| Логическое значение | Родной `BOOLEAN` | `TINYINT(1)` | `INTEGER` | `BIT` |
| Автоматическое увеличение | `SERIAL` / `GENERATED` | `AUTO_INCREMENT` | `INTEGER PRIMARY KEY` | `IDENTITY` |
| JSON | `JSONB` (проиндексировано) | `JSON` | Текст (внутренний) | `NVARCHAR(MAX)` |
| Массив | Родной `ARRAY` | Не поддерживается | Не поддерживается | Не поддерживается |
| CTE (рекурсивный) | Полная поддержка | 8.0+ | 3.8.3+ | Полная поддержка |
| Оконные функции | Полная поддержка | 8.0+ | 3.25.0+ | Полная поддержка |
| Полнотекстовый поиск | `tsvector` + ДЖИН | `FULLTEXT` индекс | Расширение FTS5 | Полнотекстовый каталог |
| ОГРАНИЧЕНИЕ/СМЕЩЕНИЕ | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` |

### Советы по совместимости { #compatibility-tips }

- **Всегда используйте параметризованные запросы** — предотвращает внедрение SQL на всех диалектах
- ** Избегайте специфичных для диалекта функций в общем коде ** — перенос в слой адаптера
- **Тестовые миграции на целевом движке** — `information_schema` варьируется в зависимости от двигателя
- **Используйте формат даты ISO** — `'YYYY-MM-DD'` работает везде
- **Идентификаторы кавычек** — используйте двойные кавычки (стандарт SQL) или обратные кавычки (MySQL)

---

## Шаблоны ORM { #orm-patterns }

### Призма { #prisma }

**Определение схемы**
```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId Int
}
```

**Миграции**: `npx prisma migrate dev --name add_user_email`
**API запросов**: `prisma.user.findMany({ where: { email: { contains: '@' } }, include: { posts: true } })`
**Аварийный люк Raw SQL**: `prisma.$queryRaw\`ВЫБЕРИТЕ * ИЗ пользователей, ГДЕ id = ${userId}\``

### Моросящий дождь { #drizzle }

**Схема-первое определение**
```typescript
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow(),
});
```

**Построитель запросов**: `db.select().from(users).where(eq(users.email, email))`
**Миграции**: `npx drizzle-kit generate:pg` затем `npx drizzle-kit push:pg`

### Типовая форма { #typeorm }

**Декораторы объектов**
```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @OneToMany(() => Post, post => post.author)
  posts: Post[];
}
```

**Шаблон хранилища**: `userRepo.find({ where: { email }, relations: ['posts'] })`
**Миграции**: `npx typeorm migration:generate -n AddUserEmail`

### SQLAlchemy { #sqlalchemy }

**Декларативные модели**
```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    posts = relationship('Post', back_populates='author')
```

**Управление сеансами**: Всегда используйте `with Session() as session:` контекстный менеджер
**Миграция перегонного куба**: `alembic revision --autogenerate -m "add user email"`

> Смотрите ссылки/orm_patterns.md для параллельных сравнений и воркфлоу миграции для каждой ORM.

---

## Целостность данных { #data-integrity }

### Стратегия ограничения { #constraint-strategy }

- **Первичные ключи** — в каждой таблице должен быть один; предпочитайте суррогатные ключи (serial/UUID)
- **Внешние ключи** — обеспечивают ссылочную целостность; явно определяют поведение при УДАЛЕНИИ
- **УНИКАЛЬНЫЕ ограничения** — для уникальности на бизнес-уровне (электронная почта, slug, ключ API)
- **ПРОВЕРКА ограничений** — проверка диапазонов, перечислений и бизнес-правил на уровне базы данных
- **NOT NULL** — значение по умолчанию NOT NULL; сделать обнуляемым только в том случае, если действительно необязательно

### Уровни изоляции транзакций { #transaction-isolation-levels }

| Уровень | Грязное чтение | Неповторяемое считывание | Призрачное чтение | Вариант использования |
|-------|-----------|-------------------|-------------|----------|
| ПРОЧИТАНО НЕЗАФИКСИРОВАННЫМ | Да | Да | Да | Никогда не рекомендовалось |
| ЧТЕНИЕ ЗАФИКСИРОВАНО | Нет | Да | Да | По умолчанию для PostgreSQL, общий OLTP |
| ПОВТОРЯЕМОЕ СЧИТЫВАНИЕ | Нет | Нет | Да (InnoDB: Нет) | Финансовые расчеты |
| СЕРИАЛИЗУЕМЫЙ | Нет | Нет | Нет | Критическая согласованность (выставление счетов, инвентаризация) |

### Предотвращение тупиковой ситуации { #deadlock-prevention }

1. **Последовательный порядок блокировок** — всегда получайте блокировки в одной и той же таблице/row порядок
2. ** Короткие транзакции** — минимизируют время между первой блокировкой и фиксацией
3. **Рекомендательные блокировки** — используйте `pg_advisory_lock()` для координации на уровне приложений
4. ** Логика повторных попыток ** — отлавливать ошибки взаимоблокировки и повторять попытку с экспоненциальным откатом

---

## Резервное копирование и восстановление { #backup--restore }

### PostgreSQL { #postgresql }
```bash
# Full backup
pg_dump -Fc --no-owner dbname > backup.dump
# Restore
pg_restore -d dbname --clean --no-owner backup.dump
# Point-in-time recovery: configure WAL archiving + restore_command
```

### MySQL { #mysql }
```bash
# Full backup
mysqldump --single-transaction --routines --triggers dbname > backup.sql
# Restore
mysql dbname < backup.sql
# Binary log for PITR: mysqlbinlog --start-datetime="2025-01-01 00:00:00" binlog.000001
```

### SQLite { #sqlite }
```bash
# Backup (safe with concurrent reads)
sqlite3 dbname ".backup backup.db"
```

### Лучшие практики резервного копирования { #backup-best-practices }
- **Автоматизировать** — таймер cron или systemd, никогда - только вручную
- **Тестовое восстановление** — непроверенные резервные копии не являются резервными копиями
- **Копии за пределами сайта** — S3, GCS или отдельный регион
- ** Политика хранения** — ежедневно в течение 7 дней, еженедельно в течение 4 недель, ежемесячно в течение 12 месяцев
- ** Отслеживайте размер и продолжительность резервной копии ** — внезапные изменения сигнализируют о проблемах

---

## Анти-паттерны { #anti-patterns }

| Анти-паттерн | Проблема | Исправить |
|-------------|---------|-----|
| `SELECT *` | Переносит ненужные данные, прерывает работу при изменении схемы | Явный список столбцов |
| Отсутствующие индексы в столбцах FK | Медленные объединения и каскадные удаления | Добавьте индексы ко всем внешним ключам |
| N+1 запрос | 1 + N обращений к базе данных в оба конца | Быстрая загрузка или пакетные запросы |
| Неявное принуждение к типу | `WHERE id = '123'` предотвращает использование индекса | Сопоставлять типы в предикатах |
| Нет объединения подключений | Отводящие соединения под нагрузкой | PgBouncer, ProxySQL или ORM-пул |
| Неограниченные запросы | Отсутствие ОГРАНИЧЕНИЙ приводит к возврату миллионов строк | Всегда разбивайте на страницы |
| Хранение денег в свободном обращении | Ошибки округления | Использование `DECIMAL(19,4)` или целые центы |
| Таблицы богов | Одна таблица с более чем 50 столбцами | Нормализуйте или используйте вертикальное разбиение на разделы |
| Мягкое удаление везде | Усложняет каждый запрос с помощью `WHERE deleted_at IS NULL` | Архивные таблицы или поиск событий |
| Объединение необработанных строк | SQL-инъекция | Параметризованные запросы всегда |

---

## Перекрестные ссылки { #cross-references }

| Скилл | Отношения |
|-------|-------------|
| **разработчик базы данных** | Архитектура схемы, анализ нормализации, генерация ERD |
| **база данных-схема-конструктор** | Визуальное ERD-моделирование, отображение взаимосвязей |
| **миграция-архитектор** | Сложная многоэтапная оркестрация миграции |
| **api-разработчик-рецензент** | Обеспечение соответствия конечных точек API шаблонам запросов |
| **наблюдаемость-платформа** | Мониторинг производительности запросов, оповещения о медленных запросах |
