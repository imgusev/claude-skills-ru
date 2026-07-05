---
title: "Эксперт по ревью в области PR { #pr-review-expert } — Агентский скилл для Codex и OpenClaw"
description: "Используйте, когда пользователь запрашивает ревью запросов на извлечение, анализ изменений кода, проверку на наличие проблем с безопасностью в PR или. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Эксперт по ревью в области PR { #pr-review-expert }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `pr-review-expert`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/pr-review-expert/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Уровень:** МОЩНЫЙ
**Категория:** Инженерия
**Домен:** Ревью кода / Гарантия качества

---

## Обзор { #overview }

Структурированный, систематический ревью кода для GitHub PR и GitLab MRs. Выходит за рамки требований к стилю — этот скилл
выполняет анализ радиуса поражения, сканирование системы безопасности, обнаружение критических изменений и расчет дельты покрытия тестами
. Подготавливает готовый для рецензента отчет с чек-листом из более чем 30 пунктов и приоритетными выводами.

---

## Основные возможности { #core-capabilities }

- **Анализ радиуса поражения** — отслеживание того, какие файлы, службы и последующие потребители могут быть повреждены.
- ** Проверка безопасности** — SQL-инъекция, XSS, обход аутентификации, раскрытие секретов, уязвимости зависимостей
- **Дельта тестового покрытия** — соотношение нового кода и новых тестов
- **Обнаружение критических изменений** — Контракты API, перенос схемы базы данных, ключи конфигурации
- **Привязка тикета** — убедитесь, что тикет Jira/Linear существует и соответствует области применения
- ** Влияние на производительность** — N+1 запросов, регрессия размера пакета, распределение памяти

---

## Когда использовать { #when-to-use }

- Перед объединением любых PR/MR, которые касаются разделяемых библиотек, API или схемы базы данных
- Когда PR большой (изменено более 200 строк) и нуждается в структурированном ревью
- Онбординг новых участников, чьи PR нуждаются в тщательной обратной связи
- Пути к кодам, чувствительным к безопасности (авторизация, платежи, обработка персональных данных)
- После инцидента — ревью аналогичных PR в упреждающем порядке

---

## Получение разницы { #fetching-the-diff }

### GitHub (gh CLI) { #github-gh-cli }
```bash
# View diff in terminal
gh pr diff <PR_NUMBER>

# Get PR metadata (title, body, labels, linked issues)
gh pr view <PR_NUMBER> --json title,body,labels,assignees,milestone

# List files changed
gh pr diff <PR_NUMBER> --name-only

# Check CI status
gh pr checks <PR_NUMBER>

# Download diff to file for analysis
gh pr diff <PR_NUMBER> > /tmp/pr-<PR_NUMBER>.diff
```

### GitLab (glab CLI) { #gitlab-glab-cli }
```bash
# View MR diff
glab mr diff <MR_IID>

# MR details as JSON
glab mr view <MR_IID> --output json

# List changed files
glab mr diff <MR_IID> --name-only

# Download diff
glab mr diff <MR_IID> > /tmp/mr-<MR_IID>.diff
```

---

## Воркфлоу { #workflow }

### Шаг 1 — Выборка контекста { #step-1--fetch-context }

```bash
PR=123
gh pr view $PR --json title,body,labels,milestone,assignees | jq .
gh pr diff $PR --name-only
gh pr diff $PR > /tmp/pr-$PR.diff
```

### Шаг 2 — Анализ радиуса поражения { #step-2--blast-radius-analysis }

Для каждого измененного файла определите:

1. **Прямые иждивенцы** — кто импортирует этот файл?
```bash
# Find all files importing a changed module
grep -r "from ['\"].*changed-module['\"]" src/ --include="*.ts" -l
grep -r "require(['\"].*changed-module" src/ --include="*.js" -l

# Python
grep -r "from changed_module import\|import changed_module" . --include="*.py" -l
```

2. **Границы сервиса** — распространяется ли это изменение на сервис?
```bash
# Check if changed files span multiple services (monorepo)
gh pr diff $PR --name-only | cut -d/ -f1-2 | sort -u
```

3. **Общие контракты** — типы, интерфейсы, схемы
```bash
gh pr diff $PR --name-only | grep -E "types/|interfaces/|schemas/|models/"
```

**Степень тяжести радиуса поражения:**
- КРИТИЧЕСКИ ВАЖНАЯ разделяемая библиотека, модель базы данных, промежуточное программное обеспечение для аутентификации, контракт API
- ВЫСОКИЙ уровень обслуживания, используемый >3 другими пользователями, общая конфигурация, переменные env
- СРЕДСТВО — однократное внутреннее изменение сервиса, служебная функция
- Компонент с низким уровнем пользовательского интерфейса, тестовый файл, документы

### Шаг 3 — Проверка безопасности { #step-3--security-scan }

```bash
DIFF=/tmp/pr-$PR.diff

# SQL Injection — raw query string interpolation
grep -n "query\|execute\|raw(" $DIFF | grep -E '\$\{|f"|%s|format\('

# Hardcoded secrets
grep -nE "(password|secret|api_key|token|private_key)\s*=\s*['\"][^'\"]{8,}" $DIFF

# AWS key pattern
grep -nE "AKIA[0-9A-Z]{16}" $DIFF

# JWT secret in code
grep -nE "jwt\.sign\(.*['\"][^'\"]{20,}['\"]" $DIFF

# XSS vectors
grep -n "dangerouslySetInnerHTML\|innerHTML\s*=" $DIFF

# Auth bypass patterns
grep -n "bypass\|skip.*auth\|noauth\|TODO.*auth" $DIFF

# Insecure hash algorithms
grep -nE "md5\(|sha1\(|createHash\(['\"]md5|createHash\(['\"]sha1" $DIFF

# eval / exec
grep -nE "\beval\(|\bexec\(|\bsubprocess\.call\(" $DIFF

# Prototype pollution
grep -n "__proto__\|constructor\[" $DIFF

# Path traversal risk
grep -nE "path\.join\(.*req\.|readFile\(.*req\." $DIFF
```

### Шаг 4 — Дельта тестового покрытия { #step-4--test-coverage-delta }

```bash
# Count source vs test files changed
CHANGED_SRC=$(gh pr diff $PR --name-only | grep -vE "\.test\.|\.spec\.|__tests__")
CHANGED_TESTS=$(gh pr diff $PR --name-only | grep -E "\.test\.|\.spec\.|__tests__")

echo "Source files changed: $(echo "$CHANGED_SRC" | wc -w)"
echo "Test files changed:   $(echo "$CHANGED_TESTS" | wc -w)"

# Lines of new logic vs new test lines
LOGIC_LINES=$(grep "^+" /tmp/pr-$PR.diff | grep -v "^+++" | wc -l)
echo "New lines added: $LOGIC_LINES"

# Run coverage locally
npm test -- --coverage --changedSince=main 2>/dev/null | tail -20
pytest --cov --cov-report=term-missing 2>/dev/null | tail -20
```

**Правила дельты покрытия:**
- Новая функция без тестов → флаг
- Удаленные тесты без удаленного кода → флаг
- Снижение охвата >5% → слияние блоков
- Пути авторизации/платежей → требуется 100% покрытие

### Шаг 5 — Обнаружение критических изменений { #step-5--breaking-change-detection }

#### Изменения в контракте API { #api-contract-changes }
```bash
# OpenAPI/Swagger spec changes
grep -n "openapi\|swagger" /tmp/pr-$PR.diff | head -20

# REST route removals or renames
grep "^-" /tmp/pr-$PR.diff | grep -E "router\.(get|post|put|delete|patch)\("

# GraphQL schema removals
grep "^-" /tmp/pr-$PR.diff | grep -E "^-\s*(type |field |Query |Mutation )"

# TypeScript interface removals
grep "^-" /tmp/pr-$PR.diff | grep -E "^-\s*(export\s+)?(interface|type) "
```

#### Изменения схемы базы данных { #db-schema-changes }
```bash
# Migration files added
gh pr diff $PR --name-only | grep -E "migrations?/|alembic/|knex/"

# Destructive operations
grep -E "DROP TABLE|DROP COLUMN|ALTER.*NOT NULL|TRUNCATE" /tmp/pr-$PR.diff

# Index removals (perf regression risk)
grep "DROP INDEX\|remove_index" /tmp/pr-$PR.diff
```

#### Изменения в конфигурации / Env Var { #config--env-var-changes }
```bash
# New env vars referenced in code (might be missing in prod)
grep "^+" /tmp/pr-$PR.diff | grep -oE "process\.env\.[A-Z_]+" | sort -u

# Removed env vars (could break running instances)
grep "^-" /tmp/pr-$PR.diff | grep -oE "process\.env\.[A-Z_]+" | sort -u
```

### Шаг 6 — Влияние на производительность { #step-6--performance-impact }

```bash
# N+1 query patterns (DB calls inside loops)
grep -n "\.find\|\.findOne\|\.query\|db\." /tmp/pr-$PR.diff | grep "^+" | head -20
# Then check surrounding context for forEach/map/for loops

# Heavy new dependencies
grep "^+" /tmp/pr-$PR.diff | grep -E '"[a-z@].*":\s*"[0-9^~]' | head -20

# Unbounded loops
grep -n "while (true\|while(true" /tmp/pr-$PR.diff | grep "^+"

# Missing await (accidentally sequential promises)
grep -n "await.*await" /tmp/pr-$PR.diff | grep "^+" | head -10

# Large in-memory allocations
grep -n "new Array([0-9]\{4,\}\|Buffer\.alloc" /tmp/pr-$PR.diff | grep "^+"
```

---

## Проверка привязки к билету { #ticket-linking-verification }

```bash
# Extract ticket references from PR body
gh pr view $PR --json body | jq -r '.body' | \
  grep -oE "(PROJ-[0-9]+|[A-Z]+-[0-9]+|https://linear\.app/[^)\"]+)" | sort -u

# Verify Jira ticket exists (requires JIRA_API_TOKEN to be SET in the environment).
# Credentials are fed to curl via a config read from stdin (-K -) so the token
# never appears in argv — `ps aux` / /proc/*/cmdline can't see it, and nothing
# secret lands in shell history. Never paste the raw token on the command line.
TICKET="PROJ-123"
: "${JIRA_API_TOKEN:?JIRA_API_TOKEN must be set}"
curl -s -K - "https://your-org.atlassian.net/rest/api/3/issue/$TICKET" <<EOF | \
  jq '{key, summary: .fields.summary, status: .fields.status.name}'
user = "user@company.com:$JIRA_API_TOKEN"
EOF

# Linear ticket — same pattern: the Authorization header goes through the
# stdin config, not a -H flag, to keep the key out of the process list.
LINEAR_ID="abc-123"
: "${LINEAR_API_KEY:?LINEAR_API_KEY must be set}"
curl -s -K - -H "Content-Type: application/json" \
  --data "{\"query\": \"{ issue(id: \\\"$LINEAR_ID\\\") { title state { name } } }\"}" \
  https://api.linear.app/graphql <<EOF | jq .
header = "Authorization: $LINEAR_API_KEY"
EOF
```

> ** Примечание по безопасности:** при повторном использовании Jira предпочитайте `~/.netrc` запись
> (`machine your-org.atlassian.net login user@company.com password <token>`,
> `chmod 600 ~/.netrc`) и позвонить `curl -s --netrc …` — никаких секретных материалов в
> команда вообще.

---

## Полный Чек-лист для ревью (более 30 пунктов) { #complete-review-checklist-30-items }

```markdown
## Code Review Checklist

### Scope & Context
- [ ] PR title accurately describes the change
- [ ] PR description explains WHY, not just WHAT
- [ ] Linked Jira/Linear ticket exists and matches scope
- [ ] No unrelated changes (scope creep)
- [ ] Breaking changes documented in PR body

### Blast Radius
- [ ] Identified all files importing changed modules
- [ ] Cross-service dependencies checked
- [ ] Shared types/interfaces/schemas reviewed for breakage
- [ ] New env vars documented in .env.example
- [ ] DB migrations are reversible (have down() / rollback)

### Security
- [ ] No hardcoded secrets or API keys
- [ ] SQL queries use parameterized inputs (no string interpolation)
- [ ] User inputs validated/sanitized before use
- [ ] Auth/authorization checks on all new endpoints
- [ ] No XSS vectors (innerHTML, dangerouslySetInnerHTML)
- [ ] New dependencies checked for known CVEs
- [ ] No sensitive data in logs (PII, tokens, passwords)
- [ ] File uploads validated (type, size, content-type)
- [ ] CORS configured correctly for new endpoints

### Testing
- [ ] New public functions have unit tests
- [ ] Edge cases covered (empty, null, max values)
- [ ] Error paths tested (not just happy path)
- [ ] Integration tests for API endpoint changes
- [ ] No tests deleted without clear reason
- [ ] Test names clearly describe what they verify

### Breaking Changes
- [ ] No API endpoints removed without deprecation notice
- [ ] No required fields added to existing API responses
- [ ] No DB columns removed without two-phase migration plan
- [ ] No env vars removed that may be set in production
- [ ] Backward-compatible for external API consumers

### Performance
- [ ] No N+1 query patterns introduced
- [ ] DB indexes added for new query patterns
- [ ] No unbounded loops on potentially large datasets
- [ ] No heavy new dependencies without justification
- [ ] Async operations correctly awaited
- [ ] Caching considered for expensive repeated operations

### Code Quality
- [ ] No dead code or unused imports
- [ ] Error handling present (no bare empty catch blocks)
- [ ] Consistent with existing patterns and conventions
- [ ] Complex logic has explanatory comments
- [ ] No unresolved TODOs (or tracked in ticket)
```

---

## Выходной формат { #output-format }

Структурируйте свой комментарий к ревью следующим образом:

```
## PR Review: [PR Title] (#NUMBER)

Blast Radius: HIGH — changes lib/auth used by 5 services
Security: 1 finding (medium severity)
Tests: Coverage delta +2%
Breaking Changes: None detected

--- MUST FIX (Blocking) ---

1. SQL Injection risk in src/db/users.ts:42
   Raw string interpolation in WHERE clause.
   Fix: db.query("SELECT * WHERE id = $1", [userId])

--- SHOULD FIX (Non-blocking) ---

2. Missing auth check on POST /api/admin/reset
   No role verification before destructive operation.

--- SUGGESTIONS ---

3. N+1 pattern in src/services/reports.ts:88
   findUser() called inside results.map() — batch with findManyUsers(ids)

--- LOOKS GOOD ---
- Test coverage for new auth flow is thorough
- DB migration has proper down() rollback method
- Error handling consistent with rest of codebase
```

---

## Распространенные подводные камни { #common-pitfalls }

- ** Ревью стиля по существу ** — позвольте компоновщику обрабатывать стиль; сосредоточьтесь на логике, безопасности, корректности
- **Отсутствует радиус поражения** — изменение 5 строк в общей утилите может нарушить работу 20 служб
- ** Утверждение непроверенных счастливых путей ** — всегда проверяйте, что пути ошибок имеют покрытие
- **Игнорирование риска миграции** — Для добавлений NOT NULL требуется миграция по умолчанию или двухэтапная миграция
- ** Косвенное раскрытие секретов ** — секреты в сообщениях об ошибках / журналах, а не только жестко закодированные значения
- ** Пропуск больших PR** — если PR слишком велик для правильной ревью, попросите разделить его

---

## Лучшие практики { #best-practices }

1. Прочтите связанный тикет, прежде чем просматривать код — контекст предотвращает ложные срабатывания
2. Проверьте статус CI перед ревью — не ревью код, который не удалось собрать
3. Отдавайте предпочтение радиусу поражения и безопасности, а не стилю
4. Воспроизведение локально для нетривиальной аутентификации или изменения производительности
5. Четко обозначьте каждый комментарий: "nit:", "обязательно:", "вопрос:", "предложение:"
6. Объедините все комментарии в один раунд ревью — не просачивайте обратную связь
7. Отмечайте хорошие образцы поведения, а не только проблемы — похвала за конкретные действия улучшает культуру
