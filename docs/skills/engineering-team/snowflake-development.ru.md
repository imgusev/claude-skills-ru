---
title: "Разработка снежинки { #snowflake-development } — Агентский скилл и плагин Codex"
description: "Используется при написании Snowflake SQL, построении пайплайнов данных с динамическими таблицами или потоками /задачами, использовании функций Cortex. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Разработка снежинки { #snowflake-development }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `snowflake-development`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/snowflake-development/skills/snowflake-development/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Разработка Snowflake SQL, пайплайнов данных, Cortex AI и Snowpark на Python. Охватывает правило префикса двоеточия, полуструктурированные данные, обновления слиянием, динамические таблицы, потоки + задачи, функции Cortex AI, спецификации агентов, настройку производительности и усиление безопасности.

> Первоначально внесенный [Джеймс Ча-Эрли](https://github.com/jamescha-earley) — усовершенствован и интегрирован командой claude-скиллы.

## Быстрый старт { #quick-start }

```bash
# Generate a MERGE upsert template
python scripts/snowflake_query_helper.py merge --target customers --source staging_customers --key customer_id --columns name,email,updated_at

# Generate a Dynamic Table template
python scripts/snowflake_query_helper.py dynamic-table --name cleaned_events --warehouse transform_wh --lag "5 minutes"

# Generate RBAC grant statements
python scripts/snowflake_query_helper.py grant --role analyst_role --database analytics --schemas public,staging --privileges SELECT,USAGE
```

---

## Лучшие практики SQL { #sql-best-practices }

### Название и стиль { #naming-and-style }

- Использование `snake_case` для всех идентификаторов. Избегайте идентификаторов в двойных кавычках - они заставляют имена, чувствительные к регистру, заключаться в постоянные кавычки.
- Используйте CTE (`WITH` предложения) над вложенными подзапросами.
- Использование `CREATE OR REPLACE` для идемпотентного DDL.
- Используйте явные списки столбцов - никогда `SELECT *` в производстве. Столбчатое хранилище Snowflake сканирует только столбцы, на которые есть ссылки, поэтому явные списки сокращают ввод-вывод.

### Хранимые процедуры - Правило префикса двоеточия { #stored-procedures----colon-prefix-rule }

В хранимых процедурах SQL (BEGIN...КОНЕЧНЫЕ блоки), переменные и параметры **должны** использовать двоеточие `:` префикс внутри инструкций SQL. Без этого Snowflake обрабатывает их как идентификаторы столбцов и выдает ошибки "недопустимый идентификатор".

```sql
-- WRONG: missing colon prefix
SELECT name INTO result FROM users WHERE id = p_id;

-- CORRECT: colon prefix on both variable and parameter
SELECT name INTO :result FROM users WHERE id = :p_id;
```

Это относится к ОБЪЯВЛЕНИЮ переменных, РАЗРЕШЕНИЮ переменных и параметрам процедуры при использовании внутри SELECT, INSERT, UPDATE, DELETE или MERGE.

### Полуструктурированные данные { #semi-structured-data }

- ВАРИАНТ, ОБЪЕКТ, МАССИВ для JSON/Avro/Parquet/ORC.
- Доступ к вложенным полям: `src:customer.name::STRING`. Всегда разыгрывайте с `::TYPE`.
- ВАРИАНТ null против SQL NULL: JSON `null` хранится в виде строки `"null"`. Используйте `STRIP_NULL_VALUE = TRUE` под нагрузкой.
- Сглаживание массивов: `SELECT f.value:name::STRING FROM my_table, LATERAL FLATTEN(input => src:items) f;`

### СЛИЯНИЕ для обновлений { #merge-for-upserts }

```sql
MERGE INTO target t USING source s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.name = s.name, t.updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN INSERT (id, name, updated_at) VALUES (s.id, s.name, CURRENT_TIMESTAMP());
```

> Видишь `references/snowflake_sql_and_pipelines.md` для более глубоких шаблонов SQL и анти-шаблонов.

---

## Пайплайны передачи данных { #data-pipelines }

### Выбираете свой подход { #choosing-your-approach }

| Подход | Когда использовать |
|----------|-------------|
| Динамические таблицы | Декларативные преобразования. ** Выбор по умолчанию.** Определите запрос, Snowflake обрабатывает обновление. |
| Потоки + задачи | Обязательный ЦКЗ. Используется для процедурной логики, вызовов хранимых процедур, сложного ветвления. |
| Снегоуборочная труба | Непрерывная загрузка файлов из облачного хранилища (S3, GCS, Azure). |

### Динамические таблицы { #dynamic-tables }

```sql
CREATE OR REPLACE DYNAMIC TABLE cleaned_events
    TARGET_LAG = '5 minutes'
    WAREHOUSE = transform_wh
    AS
    SELECT event_id, event_type, user_id, event_timestamp
    FROM raw_events
    WHERE event_type IS NOT NULL;
```

Ключевые правила:
- Набор `TARGET_LAG` постепенно: плотнее в верхней части выступа, свободнее ниже по течению.
- Инкрементные DTS не могут зависеть от DTS полного обновления.
- `SELECT *` прерывания при изменении вышестоящей схемы - используйте явные списки столбцов.
- Представления не могут располагаться между двумя динамическими таблицами в DAG.

### Потоки и задачи { #streams-and-tasks }

```sql
CREATE OR REPLACE STREAM raw_stream ON TABLE raw_events;

CREATE OR REPLACE TASK process_events
    WAREHOUSE = transform_wh
    SCHEDULE = 'USING CRON 0 */1 * * * America/Los_Angeles'
    WHEN SYSTEM$STREAM_HAS_DATA('raw_stream')
    AS INSERT INTO cleaned_events SELECT ... FROM raw_stream;

-- Tasks start SUSPENDED. You MUST resume them.
ALTER TASK process_events RESUME;
```

> Видишь `references/snowflake_sql_and_pipelines.md` для запросов отладки DT и шаблонов Snowpipe.

---

## Искусственный интеллект коры головного мозга { #cortex-ai }

### Ссылка на функцию { #function-reference }

| Функция | Цель |
|----------|---------|
| `AI_COMPLETE` | Заполнение LLM (текст, изображения, документы) |
| `AI_CLASSIFY` | Классифицировать текст по категориям (до 500 надписей) |
| `AI_FILTER` | Логический фильтр по тексту или изображениям |
| `AI_EXTRACT` | Структурированное извлечение из текста/изображений/документов |
| `AI_SENTIMENT` | Оценка настроений (от -1 до 1) |
| `AI_PARSE_DOCUMENT` | Распознавание текста или извлечение макета из документов |
| `AI_REDACT` | Удаление PII из текста |

**Устаревшие имена (не использовать):** `COMPLETE`, `CLASSIFY_TEXT`, `EXTRACT_ANSWER`, `PARSE_DOCUMENT`, `SUMMARIZE`, `TRANSLATE`, `SENTIMENT`, `EMBED_TEXT_768`.

### TO_FILE - Распространенная ошибка { #to_file----common-pitfall }

Путь к этапу и имя файла являются ** отдельными** аргументами:

```sql
-- WRONG: single combined argument
TO_FILE('@stage/file.pdf')

-- CORRECT: two arguments
TO_FILE('@db.schema.mystage', 'invoice.pdf')
```

### Агенты коры головного мозга { #cortex-agents }

Спецификации агента используют структуру JSON с ключами верхнего уровня: `models`, `instructions`, `tools`, `tool_resources`.

- Использование `$spec$` разделитель (не `$$`).
- `models` должен быть объектом, а не массивом.
- `tool_resources` является отдельным ключом верхнего уровня, не вложенным внутрь `tools`.
- Описания инструментов являются самым важным фактором качества агента.

> Видишь `references/cortex_ai_and_agents.md` для получения полных примеров спецификаций агентов и шаблонов поиска в Cortex.

---

## Питон в сноупарке { #snowpark-python }

```python
from snowflake.snowpark import Session
import os

session = Session.builder.configs({
    "account": os.environ["SNOWFLAKE_ACCOUNT"],
    "user": os.environ["SNOWFLAKE_USER"],
    "password": os.environ["SNOWFLAKE_PASSWORD"],
    "role": "my_role", "warehouse": "my_wh",
    "database": "my_db", "schema": "my_schema"
}).create()
```

- Никогда не вводите жесткие учетные данные. Используйте переменные окружения или аутентификацию пары ключей.
- Фреймы данных являются ленивыми - выполняются на `collect()` / `show()`.
- НЕ звоните `collect()` на больших фреймах данных. Обрабатывайте данные на стороне сервера с помощью операций с фреймами данных.
- Используйте ** векторизованные UDFS** (в 10-100 раз быстрее) для пакетных и ML-рабочих нагрузок.

## dbt на снежинке { #dbt-on-snowflake }

```sql
-- Dynamic table materialization (streaming/near-real-time marts):
{{ config(materialized='dynamic_table', snowflake_warehouse='transforming', target_lag='1 hour') }}

-- Incremental materialization (large fact tables):
{{ config(materialized='incremental', unique_key='event_id') }}

-- Snowflake-specific configs (combine with any materialization):
{{ config(transient=true, copy_grants=true, query_tag='team_daily') }}
```

- НЕ используйте `{{ this }}` без `{% if is_incremental() %}` охранник.
- Использование `dynamic_table` материализация для потоковых витрин или витрин, работающих почти в реальном времени.

## Производительность { #performance }

- **Ключи кластера**: Только для таблиц с несколькими ТБАЙТ. Применить к WHERE / JOIN / GROUP BY columns.
- **Поисковая оптимизация**: `ALTER TABLE t ADD SEARCH OPTIMIZATION ON EQUALITY(col);`
- ** Определение размеров склада**: Начните с малого, увеличивайте масштаб. Набор `AUTO_SUSPEND = 60`, `AUTO_RESUME = TRUE`.
- **Отдельные склады** для каждой рабочей нагрузки (загрузка, преобразование, запрос).

## Безопасность { #security }

- Следуйте RBAC с наименьшими привилегиями. Используйте роли базы данных для предоставления прав на объектном уровне.
- Регулярно проводите аудит УЧЕТНОЙ записи АДМИНИСТРАТОРА: `SHOW GRANTS OF ROLE ACCOUNTADMIN;`
- Используйте сетевые политики для включения в список разрешенных IP-адресов.
- Используйте политики маскировки для столбцов PII и политики доступа к строкам для мультитенантной изоляции.

---

## Проактивные триггеры { #proactive-triggers }

Выявляйте эти проблемы, не спрашивая, когда вы замечаете их в контексте:

- **Отсутствует префикс двоеточия ** в хранимых процедурах SQL -- немедленно отметьте, это приводит к "недопустимому идентификатору" во время выполнения.
- **`SELECT *` в динамических таблицах** -- помечать как бомбу замедленного действия для изменения схемы.
- ** Устаревшие названия функций Cortex** (`CLASSIFY_TEXT`, `SUMMARIZE`, и т.д.) -- предложите текущее `AI_*` эквиваленты.
- **Задача не возобновлена** после создания - напоминаем, что запуск задач ПРИОСТАНОВЛЕН.
- **Жестко закодированные учетные данные** в коде Snowpark - помечены как угроза безопасности.

---

## Распространенные ошибки { #common-errors }

| Ошибка | Причина | Исправить |
|-------|-------|-----|
| "Объект не существует" | Неправильный контекст базы данных/схемы или отсутствующие разрешения | Имена, полностью соответствующие требованиям (`db.schema.table`), проверять гранты |
| "Недопустимый идентификатор" в процедуре | Отсутствующий префикс двоеточия в переменной | Использование `:variable_name` внутри инструкций SQL |
| "Числовое значение не распознано" | Поле варианта не приведено | Приведенный явно: `src:field::NUMBER(10,2)` |
| Задача не запущена | Забыл возобновить работу после создания | `ALTER TASK task_name RESUME;` |
| Ошибка обновления DT | Изменение схемы в восходящем потоке или отслеживание отключено | Используйте явные столбцы, проверьте отслеживание изменений |
| Ошибка TO_FILE | Объединенный путь в качестве единственного аргумента | Разделить на два аргумента: `TO_FILE('@stage', 'file.pdf')` |

---

## Практичный воркфлоу { #practical-workflows }

### Воркфлоу 1: Построение пайплайна отчетности (30 мин) { #workflow-1-build-a-reporting-pipeline-30-min }

1. **Исходные данные этапа**: Создайте внешний этап, указывающий на S3/GCS/Azure, настройте Snowpipe для автоматического ввода
2. **Очистить с помощью динамической таблицы**: Создать DT с помощью `TARGET_LAG = '5 minutes'` который фильтрует нулевые значения, приводит типы в соответствие, дедуплицирует
3. **Агрегировать с нижестоящим DT**: Второй DT, который объединяет очищенные данные с таблицами измерений, вычисляет показатели
4. **Открыть доступ с помощью защищенного просмотра**: Создать `SECURE VIEW` для уровня инструментов BI / API
5. **Предоставить доступ**: Использовать `snowflake_query_helper.py grant` для создания инструкций RBAC

### Воркфлоу 2: Добавьте классификацию искусственного интеллекта к существующим данным { #workflow-2-add-ai-classification-to-existing-data }

1. **Определите столбец**: Найдите текстовый столбец для классификации (например, заявки в службу поддержки, ревью).
2. **Тест с помощью AI_CLASSIFY**: `SELECT AI_CLASSIFY(text_col, ['bug', 'feature', 'question']) FROM table LIMIT 10;`
3. **Создать DT обогащения**: Динамическую таблицу, которая запускается `AI_CLASSIFY` в новых строках автоматически
4. ** Отслеживайте затраты **: Cortex AI выставляет счет за каждый образец токена перед запуском на полных таблицах

### Воркфлоу 3: Отладка неисправного пайплайна { #workflow-3-debug-a-failing-pipeline }

1. **Проверьте историю задач**: `SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY()) WHERE STATE = 'FAILED' ORDER BY SCHEDULED_TIME DESC;`
2. **Проверьте обновление DT**: `SELECT * FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY('my_dt')) ORDER BY REFRESH_END_TIME DESC;`
3. **Проверьте затхлость потока**: `SHOW STREAMS; -- check stale_after column`
4. **Обратитесь к руководству по устранению неполадок**: Смотрите `references/troubleshooting.md` для исправления конкретных ошибок

---

## Анти-паттерны { #anti-patterns }

| Анти-паттерн | Почему это терпит неудачу | Лучший подход |
|---|---|---|
| `SELECT *` в динамических таблицах | Изменения схемы выше по потоку автоматически прерывают DT | Используйте явные списки столбцов |
| Отсутствующий префикс двоеточия в процедурах | Ошибка времени выполнения "Недопустимый идентификатор" | Всегда используйте `:variable_name` в блоках SQL |
| Единый склад для всех рабочих нагрузок | Конфликт между загрузкой, преобразованием и запросом | Отдельные склады для каждого типа рабочей нагрузки |
| Жестко запрограммированные учетные данные в Snowpark | Угроза безопасности, сбои в CI/CD | Использование `os.environ[]` или аутентификация пары ключей |
| `collect()` на больших фреймах данных | Извлекает весь результирующий набор в клиентскую память | Обрабатывать серверные операции с фреймами данных |
| Вложенные подзапросы вместо CTE | Нечитаемый, трудный для отладки, Snowflake лучше оптимизирует CTE | Использование `WITH` положения |
| Использование устаревших функций Cortex | `CLASSIFY_TEXT`, `SUMMARIZE` и так далее. будет удален | Использование `AI_CLASSIFY`, `AI_COMPLETE` и так далее. |
| Задачи без `WHEN SYSTEM$STREAM_HAS_DATA` | Задача выполняется по расписанию даже при отсутствии новых данных, что приводит к пустой трате кредитов | Добавьте предложение WHEN для задач, управляемых потоком |
| Идентификаторы, заключенные в двойные кавычки | Принудительно учитывает регистр имен во всех запросах | Использование `snake_case` идентификаторы без кавычек |

---

## Перекрестные ссылки { #cross-references }

| Скилл | Отношения |
|-------|-------------|
| `engineering/sql-database-assistant` | Общие шаблоны SQL — используются для баз данных, отличных от Snowflake |
| `engineering/database-designer` | Разработка схемы — используется для моделирования данных перед внедрением Snowflake |
| `engineering-team/senior-data-engineer` | Более широкая разработка данных — пайплайны, искра, воздушный поток, качество данных |
| `engineering-team/senior-data-scientist` | Аналитика и ML — использование наряду со Snowpark для разработки функций |
| `engineering-team/senior-devops` | CI/CD для развертывания Snowflake (Terraform, GitHub Actions) |

---

## Справочная документация { #reference-documentation }

| Документ | Содержание |
|----------|----------|
| `references/snowflake_sql_and_pipelines.md` | Шаблоны SQL, шаблоны СЛИЯНИЯ, динамическая отладка таблиц, Snowpipe, анти-шаблоны |
| `references/cortex_ai_and_agents.md` | Функции искусственного интеллекта Cortex, структура спецификаций агентов, поиск в Cortex, Сноупарк |
| `references/troubleshooting.md` | Ссылки на ошибки, отладочные запросы, распространенные исправления |
