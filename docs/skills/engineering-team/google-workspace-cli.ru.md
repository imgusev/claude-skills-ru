---
title: "Интерфейс Google Workspace CLI { #google-workspace-cli } — Агентский скилл и плагин Codex"
description: "Администрирование Google Workspace с помощью gws CLI (github.com/googleworkspace/cli ). Установите, аутентифицируйте и автоматизируйте Gmail, Диск. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Интерфейс Google Workspace CLI { #google-workspace-cli }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `google-workspace-cli`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/google-workspace-cli/skills/google-workspace-cli/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Экспертное руководство и автоматизация для администрирования Google Workspace с использованием открытого исходного кода `gws` CLI ([github.com/googleworkspace/cli](https://github.com/googleworkspace/cli), Apache-2.0). Интерфейс CLI динамически создает свою команду surface из службы обнаружения Google, поэтому он охватывает все поддерживаемые API Workspace, а также `+`-вспомогательные команды с префиксом. Этот скилл добавляет локальные инструменты Python (doctor, auth guide, каталог рецептов, аудит безопасности, анализатор выходных данных).

> **Проверка перед написанием сценария:** `gws` генерирует команды во время выполнения из документов Google по обнаружению API, а CLI предварительно обновлен до версии 1.0. Всегда подтверждайте точную поверхность команды с помощью `gws --help`, `gws <service> --help`, или `gws schema <service>.<resource>.<method>` прежде чем внедрять его в автоматизацию. Команды в этом скилле, отмеченные *(проверить)*, иллюстрируют `gws <service> <resource> <method>` шаблон и должен быть сверен с вашей установленной версией.

---

## Быстрый старт { #quick-start }

### Проверьте установку { #check-installation }

```bash
# Verify gws is installed and authenticated
python3 scripts/gws_doctor.py
```

### Отправить электронное письмо { #send-an-email }

```bash
gws gmail +send --to "team@company.com" \
  --subject "Weekly Update" --body "Here's this week's summary..."
```

### Список файлов на диске { #list-drive-files }

```bash
gws drive files list --params '{"pageSize": 20}' | python3 scripts/output_analyzer.py --select "name,mimeType,modifiedTime" --format table
```

---

## Установка { #installation }

### npm (рекомендуется; требуется Node.js 18+) { #npm-recommended-requires-nodejs-18 }

```bash
npm install -g @googleworkspace/cli
gws --version
```

### Homebrew (macOS/Linux) { #homebrew-macoslinux }

```bash
brew install googleworkspace-cli
```

### Груз (из источника) { #cargo-from-source }

```bash
cargo install --git https://github.com/googleworkspace/cli --locked
gws --version
```

### Готовые двоичные файлы { #pre-built-binaries }

Скачать с [github.com/googleworkspace/cli/releases](https://github.com/googleworkspace/cli/releases) для macOS, Linux или Windows. Пользователи Nix: `nix run github:googleworkspace/cli`.

### Проверьте установку { #verify-installation }

```bash
python3 scripts/gws_doctor.py
# Checks: PATH, version, auth status, service connectivity
```

---

## Аутентификация { #authentication }

### Настройка OAuth (интерактивная) { #oauth-setup-interactive }

```bash
# Step 1: Create Google Cloud project and OAuth credentials
python3 scripts/auth_setup_guide.py --guide oauth

# Step 2: Run interactive auth setup (uses gcloud if available)
gws auth setup

# Step 3: Log in, requesting only the scopes you need
gws auth login -s drive,gmail,sheets
```

### Безголовый/CI { #headlessci }

```bash
# Generate setup instructions
python3 scripts/auth_setup_guide.py --guide service-account

# Export credentials from an interactive machine, then point the CLI at them
gws auth export --unmasked > credentials.json
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json
```

### Переменные окружения { #environment-variables }

```bash
# Generate .env template
python3 scripts/auth_setup_guide.py --generate-env
```

| Переменная | Цель |
|----------|---------|
| `GOOGLE_WORKSPACE_CLI_CLIENT_ID` | Идентификатор клиента OAuth |
| `GOOGLE_WORKSPACE_CLI_CLIENT_SECRET` | Секрет клиента OAuth |
| `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` | Путь к экспортированным учетным данным JSON |
| `GOOGLE_WORKSPACE_CLI_TOKEN` | Предварительно полученный токен OAuth |
| `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` | Переопределить расположение конфигурации по умолчанию |
| `GOOGLE_WORKSPACE_CLI_LOG` | Включить ведение журнала отладки |

### Проверка подлинности { #validate-authentication }

```bash
python3 scripts/auth_setup_guide.py --validate --json
# Tests each service endpoint
```

---

## Воркфлоу 1: Автоматизация Gmail { #workflow-1-gmail-automation }

** Цель:** Автоматизировать операции с электронной почтой — отправку, поиск, управление ярлыками и фильтрами.

### Отправить, ответить, переслать (вспомогательные команды) { #send-reply-forward-helper-commands }

```bash
# Send a new email
gws gmail +send --to "client@example.com" \
  --subject "Proposal" --body "Please find attached..."

# Reply to a message (auto-threading); check exact flags with: gws gmail +reply --help
gws gmail +reply ...

# Forward a message; check exact flags with: gws gmail +forward --help
gws gmail +forward ...

# Unread inbox summary
gws gmail +triage
```

### Поиск и проверка (команды обнаружения) { #search-and-inspect-discovery-commands }

Следуют команды обнаружения `gws <service> <resource> <method>` и принимать
параметры запроса в формате JSON через `--params` (запрос/path параметры) и `--json` (тело запроса).
Сначала проверьте точную схему любого метода:

```bash
# What does messages.list accept? (verify)
gws schema gmail.users.messages.list

# Search emails (verify against the schema above)
gws gmail users messages list --params '{"userId": "me", "q": "from:client@example.com after:2025/01/01"}' \
  | python3 scripts/output_analyzer.py --count

# List labels (verify)
gws gmail users labels list --params '{"userId": "me"}'
```

### Массовые операции { #bulk-operations }

Использование `--dry-run` во-первых, и `--page-all` для разбивки на страницы (одна строка JSON на страницу):

```bash
# Preview, then archive read emails older than 30 days (verify method schema first)
gws gmail users messages list --params '{"userId": "me", "q": "is:read older_than:30d"}' --page-all \
  | python3 scripts/output_analyzer.py --select "id" --format json
# Then feed ids to gmail users messages modify (see: gws schema gmail.users.messages.modify)
```

---

## Воркфлоу 2: Дисковод и листы { #workflow-2-drive--sheets }

** Цель:** Управлять файлами, создавать электронные таблицы, настраивать общий доступ и экспортировать данные.

### Файловые операции { #file-operations }

```bash
# List files
gws drive files list --params '{"pageSize": 50}' \
  | python3 scripts/output_analyzer.py --select "name,mimeType,size" --format table

# Upload a file (helper)
gws drive +upload ./report.pdf --name "Q1 Report"

# Create a Google Sheet
gws sheets spreadsheets create --json '{"properties": {"title": "Budget 2026"}}'

# Download/export — inspect the method first (verify)
gws schema drive.files.export
```

### Общий доступ (сначала проверьте схемы) { #sharing-verify-schemas-first }

```bash
# Inspect the permissions API surface
gws schema drive.permissions.create

# Share with user (verify against schema)
gws drive permissions create --params '{"fileId": "<FILE_ID>"}' \
  --json '{"type": "user", "role": "writer", "emailAddress": "colleague@company.com"}'

# List who has access (verify)
gws drive permissions list --params '{"fileId": "<FILE_ID>"}'
```

### Данные таблиц { #sheets-data }

```bash
# Read values (helper); check exact flags with: gws sheets +read --help
gws sheets +read ...

# Append a row (helper); check exact flags with: gws sheets +append --help
gws sheets +append ...

# Or use discovery methods (verify):
gws schema sheets.spreadsheets.values.update
gws sheets spreadsheets values get --params '{"spreadsheetId": "<SHEET_ID>", "range": "Sheet1!A1:D10"}'
```

---

## Воркфлоу 3: Календарь и встречи { #workflow-3-calendar--meetings }

** Цель:** Планировать мероприятия, находить доступное время и создавать отчеты о работе в режиме ожидания.

### Управление событиями { #event-management }

```bash
# Create an event (helper); check exact flags with: gws calendar +insert --help
gws calendar +insert ...

# Upcoming events (helper, timezone-aware)
gws calendar +agenda

# Or via discovery (verify):
gws schema calendar.events.insert
gws calendar events list --params '{"calendarId": "primary", "maxResults": 10}'
```

### Найдите свободное время { #find-available-time }

```bash
# Free/busy via the Calendar API (verify schema first)
gws schema calendar.freebusy.query
gws calendar freebusy query --json '{"timeMin": "...", "timeMax": "...", "items": [{"id": "alice@co.com"}]}'
```

### Промежуточный отчет (помощники по воркфлоу) { #standup-report-workflow-helpers }

```bash
# Today's meetings + tasks
gws workflow +standup-report \
  | python3 scripts/output_analyzer.py --format table

# Next meeting prep; check exact flags with: gws workflow +meeting-prep --help
gws workflow +meeting-prep
```

---

## Воркфлоу 4: Аудит безопасности { #workflow-4-security-audit }

**Цель:** Провести аудит конфигурации безопасности Google Workspace и сгенерировать команды для исправления.

### Провести полный аудит { #run-full-audit }

```bash
# Full audit across all services
python3 scripts/workspace_audit.py --json

# Audit specific services
python3 scripts/workspace_audit.py --services gmail,drive,calendar

# Demo mode (no gws required)
python3 scripts/workspace_audit.py --demo
```

### Проверки в рамках аудита { #audit-checks }

| Площадь | Проверьте | Риск |
|------|-------|------|
| Привод | Включен внешний общий доступ | Эксфильтрация данных |
| Gmail | Правила автоматической переадресации | Эксфильтрация данных |
| Gmail | Записи DMARC/SPF/DKIM | Подделка электронной почты |
| Календарь | Видимость общего доступа по умолчанию | Утечка информации |
| OAuth | Гранты для сторонних приложений | Несанкционированный доступ |
| Администратор | Количество суперадминистраторов | Эскалация привилегий |
| Администратор | 2-Ступенчатая проверка соблюдения | Захват учетной записи |

### Ревью и исправление { #review-and-remediate }

```bash
# Review findings
python3 scripts/workspace_audit.py --json | python3 scripts/output_analyzer.py \
  --filter "status=FAIL" --select "area,check,remediation"

# Execute remediation (example: check current Drive settings first; verify)
gws drive about get --params '{"fields": "*"}'
# Follow remediation commands from audit output (verify each against gws --help)
```

---

## Инструменты Python { #python-tools }

| Сценарий | Цель | Использование |
|--------|---------|-------|
| `gws_doctor.py` | Предполетная диагностика | `python3 scripts/gws_doctor.py [--json] [--services gmail,drive]` |
| `auth_setup_guide.py` | Управляемая настройка авторизации | `python3 scripts/auth_setup_guide.py --guide oauth` |
| `gws_recipe_runner.py` | Каталог рецептов и бегунок | `python3 scripts/gws_recipe_runner.py --list [--persona pm]` |
| `workspace_audit.py` | Безопасность/config аудит | `python3 scripts/workspace_audit.py [--json] [--demo]` |
| `output_analyzer.py` | Анализ JSON/NDJSON | `gws ... --json \| python3 scripts/output_analyzer.py --count` |

Все скрипты доступны только для stdlib, поддержка `--json` вывод и включение демонстрационного режима со встроенными образцами данных.

---

## Лучшие практики { #best-practices }

### Безопасность { #security }

1. Используйте OAuth с минимальными областями действия — запрашивайте только то, что необходимо для каждого воркфлоу
2. Храните токены в системной связке ключей, а не в обычных текстовых файлах
3. Меняйте ключи учетной записи сервиса каждые 90 дней
4. Ежеквартальный аудит грантов сторонних приложений OAuth
5. Использование `--dry-run` перед массовыми разрушительными операциями

### Автоматизация { #automation }

1. Все `gws` выходные данные структурированы в формате JSON — передайте их по каналу `output_analyzer.py` для фильтрации и агрегирования
2. Использование `gws workflow +*` помощники для многоэтапных операций вместо цепочки необработанных команд
3. Воспользуйтесь местным каталогом рецептов (`gws_recipe_runner.py`) в качестве шаблонов команд, затем сверьте каждый из них с `gws --help`
4. `--page-all` выдает по одной строке JSON на страницу (NDJSON) для потоковой передачи больших результирующих наборов
5. Использование `--dry-run` для предварительного просмотра любого запроса перед его выполнением

### Производительность { #performance }

1. Запрашивайте только необходимые поля через API `fields` параметр в `--params` (уменьшает размер полезной нагрузки)
2. Использование `pageSize` в `--params` чтобы ограничить результаты при просмотре
3. Использование `--page-all` только тогда, когда вам нужны полные наборы данных; настройтесь на `--page-limit` / `--page-delay`
4. Предпочитаю `+` помощники (одиночные оптимизированные вызовы) по сравнению с вызовами API с ручной цепочкой
5. Кэшируйте часто используемые данные (например, идентификаторы меток, идентификаторы папок) в переменных

---

## Ограничения { #limitations }

| Ограничение | Воздействие |
|------------|--------|
| Срок действия токенов OAuth истекает через 1 час | Повторная авторизация необходима для длительно выполняющихся скриптов |
| Ограничения скорости API (для каждого пользователя, для каждой услуги) | Массовые операции могут привести к 429 ошибкам |
| Требования к области применения варьируются в зависимости от услуги | Необходимо запросить правильные области во время аутентификации |
| Статус CLI до версии 1.0 | Возможны критические изменения между выпусками |
| Требуется проект Google Cloud | Бесплатно, но требует настройки в облачной консоли |
| Admin API требует прав администратора | Для некоторых проверок аудита требуется роль администратора рабочей области |

### Требуемые области по сервису { #required-scopes-by-service }

```bash
# List scopes for specific services
python3 scripts/auth_setup_guide.py --scopes gmail,drive,calendar,sheets
```

| Обслуживание | Ключевые области применения |
|---------|-----------|
| Gmail | `gmail.modify`, `gmail.send`, `gmail.labels` |
| Привод | `drive.file`, `drive.metadata.readonly` |
| Листы | `spreadsheets` |
| Календарь | `calendar`, `calendar.events` |
| Администратор | `admin.directory.user.readonly`, `admin.directory.group` |
| Задачи | `tasks` |
