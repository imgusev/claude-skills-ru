---
title: Cursor, Aider, Windsurf, Hermes, Mistral Vibe & 8 More AI Coding Tools
description: "Установите скиллы Claude Code и плагины агента в Hermes Агент, Mistral Vibe, Cursor, Aider, Kilo Code, Windsurf, OpenCode, Augment и Antigravity. Преобразование одной командой для 13 агентов, кодирующих искусственный интеллект."
---

# Интеграция с несколькими инструментами { #multi-tool-integrations }

Все 345 скилл в этом репозитории работают с ** 9 инструментами для кодирования искусственного интеллекта ** помимо Claude Code, Codex, Gemini CLI и OpenClaw. Агент Hermes и Mistral Vibe используют одно и то же agentskills.io SKILL.md стандартный — преобразование не требуется. Для остальных 7 инструментов сценарий преобразования адаптирует формат, ожидаемый каждым инструментом, сохраняя при этом инструкции по скиллу, воркфлоу и вспомогательные файлы.

<div class="grid cards" markdown>

-   :material-cursor-default-click:{ .lg .middle } **Курсор**

    ---

    `.mdc` файлы правил в `.cursor/rules/`

    [:octicons-arrow-right-24: Перейти к курсору](#cursor)

-   :material-code-braces:{ .lg .middle } **Помощник**

    ---

    Одинокий `CONVENTIONS.md` файл

    [:octicons-arrow-right-24: Перейти к помощнику](#aider)

-   :material-alpha-k-box:{ .lg .middle } **Код килограмма**

    ---

    Правила Markdown в `.kilocode/rules/`

    [:octicons-arrow-right-24: Перейти к коду килограмма](#kilo-code)

-   :material-surfing:{ .lg .middle } **Виндсерфинг**

    ---

    `SKILL.md` связки в `.windsurf/skills/`

    [:octicons-arrow-right-24: Перейти к виндсерфингу](#windsurf)

-   :material-console:{ .lg .middle } **Открытый код**

    ---

    `SKILL.md` связки в `.opencode/skills/`

    [:octicons-arrow-right-24: Перейти к OpenCode](#opencode)

-   :material-auto-fix:{ .lg .middle } **Увеличить**

    ---

    Файлы правил в `.augment/rules/`

    [:octicons-arrow-right-24: Перейти к дополнению](#augment)

-   :material-google:{ .lg .middle } **Антигравитация**

    ---

    `SKILL.md` связки в `~/.gemini/antigravity/skills/`

    [:octicons-arrow-right-24: Переход к антигравитации](#antigravity)

-   :material-medical-bag:{ .lg .middle } **Агент "Гермес"**

    ---

    Родной `SKILL.md` в `~/.hermes/skills/` — преобразование не требуется

    [:octicons-arrow-right-24: Перейти к агенту Гермеса](#hermes-agent)

-   :material-wave:{ .lg .middle } **Атмосфера Мистраля**

    ---

    Родной `SKILL.md` в `~/.vibe/skills/` — преобразование не требуется

    [:octicons-arrow-right-24: Окунись в атмосферу Мистраля](#mistral-vibe)

</div>

<hr class="section-divider">

## Быстрый старт { #quick-start }

### 1. Преобразовать { #1-convert }

```bash
git clone https://github.com/imgusev/claude-skills-ru.git
cd claude-skills-ru

# Convert all skills for all tools (~15 seconds)
./scripts/convert.sh --tool all

# Or convert for a specific tool only
./scripts/convert.sh --tool cursor
```

### 2. Установите { #2-install }

```bash
# Install into your project directory
./scripts/install.sh --tool cursor --target /path/to/project

# Or install globally (Antigravity)
./scripts/install.sh --tool antigravity

# Skip confirmation prompts
./scripts/install.sh --tool aider --target . --force
```

### 3. Проверьте { #3-verify }

Каждый раздел с инструментами, приведенный ниже, включает в себя шаг проверки для подтверждения загрузки скилл.

!!! tip "Regenerate after updates"
    Когда вы извлекете новые скиллы из хранилища, запустите их повторно `./scripts/convert.sh` и `./scripts/install.sh` чтобы обновить вашу локальную установку.

<hr class="section-divider">

## Как работает конверсия { #how-conversion-works }

Конвертер считывает значения каждого скилла `SKILL.md` материал для фасада (`name` и `description`) и тело Markdown, затем выводит формат, ожидаемый каждым инструментом:

| Источник | Цель | Что меняется |
|--------|--------|--------------|
| Передняя панель YAML | Лицевая панель для конкретного инструмента | Названия/значения полей адаптированы для каждого инструмента |
| Тело Markdown | Прошел через | Инструкции сохранены как есть |
| `scripts/` режиссер | Скопировано (там, где поддерживается) | Антигравитация, виндсерфинг, Открытый код |
| `references/` режиссер | Скопировано (там, где поддерживается) | Антигравитация, виндсерфинг, Открытый код |
| `templates/` режиссер | Скопировано (там, где поддерживается) | Антигравитация, виндсерфинг, Открытый код |

Инструменты, использующие плоские файлы (Cursor, Aider, Kilo Code, Augment), получают SKILL.md каталоги, поддерживающие только тело, не копируются, поскольку эти инструменты не поддерживают подкаталоги по правилу.

<hr class="section-divider">

## Курсор { #cursor }

[Курсор](https://cursor.com) использует `.mdc` файлы правил в `.cursor/rules/` с помощью frontmatter для описания, шаблонов глобусов и настроек автоматического применения.

### Формат { #format }

Каждый скилл становится отдельным `.mdc` файл:

```yaml
---
description: "What this skill does and when to activate it"
globs:
alwaysApply: false
---

# Skill instructions here...
```

- **`alwaysApply: false`** — скиллы доступны по запросу, но не всегда загружаются
- **`globs:`** — по умолчанию пусто; добавьте шаблоны файлов для автоматической активации для определенных файлов (например, `*.test.ts`)

### Установить { #install }

=== "Сценарий"

    ```bash
    ./scripts/convert.sh --tool cursor
    ./scripts/install.sh --tool cursor --target /path/to/project
    ```

=== "Руководство пользователя"

    ```bash
    mkdir -p /path/to/project/.cursor/rules
    cp integrations/cursor/rules/*.mdc /path/to/project/.cursor/rules/
    ```

### Проверить { #verify }

```bash
find .cursor/rules -name "*.mdc" | wc -l
# Expected: 156
```

Откройте панель правил курсора, чтобы просмотреть список всех доступных скиллы.

### Настройка { #customization }

После установки вы можете:

- Набор `alwaysApply: true` о скиллах, которые вы хотите использовать в каждом разговоре
- Добавить `globs: "*.py"` чтобы автоматически активировать скиллы, связанные с Python, для `.py` файлы
- Удалите скиллы вам не нужно содержать панель правил в чистоте

<hr class="section-divider">

## Помощник { #aider }

[Помощник](https://aider.chat) читает `CONVENTIONS.md` файл из корневого каталога вашего проекта. Все скиллы объединены в этот единый файл с заголовками разделов.

### Формат { #format }

```markdown
# Claude Skills — Aider Conventions
> Auto-generated from claude-skills. Do not edit manually.
> Generated: 2026-03-11

---

## copywriting
> When the user wants to write, rewrite, or improve marketing copy...

# Copywriting

You are an expert conversion copywriter...

---

## senior-architect
> Deep expertise in system architecture...

# Senior Architect
...
```

### Установить { #install }

=== "Сценарий"

    ```bash
    ./scripts/convert.sh --tool aider
    ./scripts/install.sh --tool aider --target /path/to/project
    ```

=== "Руководство пользователя"

    ```bash
    cp integrations/aider/CONVENTIONS.md /path/to/project/
    ```

### Использование { #usage }

```bash
# Aider automatically reads CONVENTIONS.md from the project root
aider

# Or explicitly point to it
aider --read CONVENTIONS.md
```

### Проверить { #verify }

```bash
wc -l CONVENTIONS.md
# Expected: ~41,000 lines (all 156 skills)

grep -c "^## " CONVENTIONS.md
# Expected: 156 (one section per skill)
```

!!! note "Large file"
    Объединенный `CONVENTIONS.md` составляет ~41 тыс. строк. Aider хорошо справляется с этим, но если вы предпочитаете файл меньшего размера, вы можете отредактировать его, чтобы сохранить только те скиллы, которые имеют отношение к вашему проекту.

<hr class="section-divider">

## Код килограмма { #kilo-code }

[Код килограмма](https://kilo.ai) считывает простые правила Markdown из `.kilocode/rules/`. Никакого специального материала для фасада не требуется.

### Формат { #format }

Каждый скилл становится чистым файлом Markdown:

```markdown
# copywriting
> When the user wants to write, rewrite, or improve marketing copy...

# Copywriting

You are an expert conversion copywriter...
```

### Установить { #install }

=== "Сценарий"

    ```bash
    ./scripts/convert.sh --tool kilocode
    ./scripts/install.sh --tool kilocode --target /path/to/project
    ```

=== "Руководство пользователя"

    ```bash
    mkdir -p /path/to/project/.kilocode/rules
    cp integrations/kilocode/rules/*.md /path/to/project/.kilocode/rules/
    ```

### Проверить { #verify }

```bash
find .kilocode/rules -name "*.md" | wc -l
# Expected: 156
```

Откройте панель правил Kilo Code (нажмите на значок ⚖), чтобы увидеть загруженные все правила.

### Правила, относящиеся к конкретному режиму { #mode-specific-rules }

Код Kilo поддерживает правила, зависящие от конкретного режима. Чтобы назначить скиллы определенным режимам:

```bash
# Move architecture skills to "architect" mode
mkdir -p .kilocode/rules-architect/
mv .kilocode/rules/senior-architect.md .kilocode/rules-architect/
mv .kilocode/rules/database-designer.md .kilocode/rules-architect/
```

<hr class="section-divider">

## Виндсерфинг { #windsurf }

[Виндсерфинг](https://windsurf.com) использует тот же самый `SKILL.md` форматируйте как код Клода — скиллы преобразуются с минимальными изменениями.

### Формат { #format }

Каждый скилл становится каталогом с `SKILL.md` плюс дополнительные вспомогательные файлы:

```
.windsurf/skills/copywriting/
├── SKILL.md           # Instructions with name/description frontmatter
├── scripts/           # Python tools (if present in source)
├── references/        # Domain knowledge (if present)
└── templates/         # Code templates (if present)
```

```yaml
---
name: "copywriting"
description: "When the user wants to write, rewrite, or improve marketing copy..."
---

# Copywriting
...
```

### Установить { #install }

=== "Сценарий"

    ```bash
    ./scripts/convert.sh --tool windsurf
    ./scripts/install.sh --tool windsurf --target /path/to/project
    ```

=== "Руководство пользователя"

    ```bash
    cp -R integrations/windsurf/skills/* /path/to/project/.windsurf/skills/
    ```

### Проверить { #verify }

```bash
find .windsurf/skills -name "SKILL.md" | wc -l
# Expected: 156
```

Скиллы автоматически отображаются в списке скилл виндсерфера. Вы также можете вызвать их с помощью `@skill-name`.

### Постепенное раскрытие { #progressive-disclosure }

В виндсерфинге используется прогрессивное раскрытие информации — по умолчанию отображаются только название и описание скилла. Полный `SKILL.md` контент загружается только тогда, когда Windowserf решает, что скилл соответствует вашему запросу, сохраняя при этом ограниченность контекстного окна.

<hr class="section-divider">

## Открытый код { #opencode }

[Открытый код](https://opencode.ai) поддерживает скиллы в `.opencode/skills/` с `SKILL.md` файлы. В нем также читается код Клода `.claude/skills/` в качестве запасного варианта.

### Формат { #format }

Каждый скилл становится каталогом с `SKILL.md`:

```yaml
---
name: "copywriting"
description: "When the user wants to write, rewrite, or improve marketing copy..."
compatibility: opencode
---

# Copywriting
...
```

Тот `compatibility: opencode` поле добавлено, чтобы помочь OpenCode идентифицировать их как нативные скиллы.

### Установить { #install }

=== "Сценарий"

    ```bash
    ./scripts/convert.sh --tool opencode
    ./scripts/install.sh --tool opencode --target /path/to/project
    ```

=== "Руководство пользователя"

    ```bash
    cp -R integrations/opencode/skills/* /path/to/project/.opencode/skills/
    ```

=== "Глобальный"

    ```bash
    # Install globally for all projects
    cp -R integrations/opencode/skills/* ~/.config/opencode/skills/
    ```

### Проверить { #verify }

```bash
find .opencode/skills -name "SKILL.md" | wc -l
# Expected: 156
```

### Совместимость с кодом Claude { #claude-code-compatibility }

OpenCode также считывает `.claude/skills/` каталоги. Если у вас уже установлены скиллы для Claude Code, OpenCode обнаружит их автоматически — преобразование не требуется.

Чтобы отключить этот резервный вариант:

```bash
export OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1
```

<hr class="section-divider">

## Увеличить { #augment }

[Увеличить](https://augmentcode.com) считывает файлы правил из `.augment/rules/` с помощью frontmatter, указывающего тип активации.

### Формат { #format }

Каждый скилл становится файлом правил Markdown:

```yaml
---
type: auto
description: "When the user wants to write, rewrite, or improve marketing copy..."
---

# Copywriting
...
```

- **`type: auto`** — Дополнение автоматически активирует правило, когда оно соответствует вашему запросу
- Другие типы: `always` (всегда загружен), `manual` (вызывается только пользователем)

### Установить { #install }

=== "Сценарий"

    ```bash
    ./scripts/convert.sh --tool augment
    ./scripts/install.sh --tool augment --target /path/to/project
    ```

=== "Руководство пользователя"

    ```bash
    mkdir -p /path/to/project/.augment/rules
    cp integrations/augment/rules/*.md /path/to/project/.augment/rules/
    ```

### Проверить { #verify }

```bash
find .augment/rules -name "*.md" | wc -l
# Expected: 156
```

### Настройка { #customization }

Изменение `type: auto` к `type: always` какие скиллы вы хотите использовать в каждом разговоре:

```bash
# Make coding standards always active
sed -i 's/type: auto/type: always/' .augment/rules/senior-architect.md
```

<hr class="section-divider">

## Антигравитация { #antigravity }

[Антигравитация](https://idx.google.com/) (Google) использует `SKILL.md` файлы в `~/.gemini/antigravity/skills/` с дополнительными полями метаданных.

### Формат { #format }

```yaml
---
name: "copywriting"
description: "When the user wants to write, rewrite, or improve marketing copy..."
risk: low
source: community
date_added: '2026-03-11'
---

# Copywriting
...
```

Дополнительные поля:

- **`risk: low`** — все скиллы предназначены только для обучения, никаких опасных операций
- **`source: community`** — определяет их как скиллы, приобретенные сообществом
- **`date_added`** — дата преобразования для отслеживания свежести

### Установить { #install }

=== "Сценарий"

    ```bash
    ./scripts/convert.sh --tool antigravity
    ./scripts/install.sh --tool antigravity
    # Installs to ~/.gemini/antigravity/skills/ by default
    ```

=== "Руководство пользователя"

    ```bash
    cp -R integrations/antigravity/* ~/.gemini/antigravity/skills/
    ```

### Проверить { #verify }

```bash
find ~/.gemini/antigravity/skills -name "SKILL.md" | wc -l
# Expected: 156
```

<hr class="section-divider">

## Агент Гермеса { #hermes-agent }

[Агент Гермеса](https://github.com/NousResearch/hermes-agent) by Nous Research - это самосовершенствующийся агент искусственного интеллекта со встроенным циклом обучения. Он использует [agentskills.io](https://agentskills.io) стандарт — **то же самое SKILL.md формат нашего репозитория использует ** — поэтому преобразование не требуется.

!!! tip "Tier: BYO-sync (pre-generated tree available since v2.7.2)"
    Начиная с версии 2.7.2, репозиторий отправляет предварительно сгенерированный `.hermes/skills/claude-skills/` дерево с **303 символическими ссылками** в **12 доменах** (включая домены производительности/маркетинга/исследований версии 2.7.0). Вам все еще нужно скопировать / символически связать это дерево в `~/.hermes/skills/` на вашем компьютере — это шаг BYO-синхронизации. Тот `sync-hermes-skills.py` скрипт обрабатывает это с помощью одной команды.

### Почему Гермес отличается от других { #why-hermes-is-different }

В отличие от других инструментов, требующих преобразования формата, Hermes считывает `SKILL.md` файлы изначально с точно таким же интерфейсом YAML (`name`, `description`, `version`, `license`), тот же макет каталога (`references/`, `templates/`, `assets/`), и то же самое `AGENTS.md` контекст проекта. Наши скиллы - это "подключи и играй".

### Шаг 1 — Установите сам агент Hermes { #step-1--install-hermes-agent-itself }

Если у вас еще не установлен агент Hermes, сначала установите его:

=== "macOS / Linux"

    ```bash
    # 1. Clone the official repo
    git clone https://github.com/NousResearch/hermes-agent.git
    cd hermes-agent

    # 2. Install dependencies (Python 3.10+)
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # 3. Configure your model provider (Nous, OpenAI, Anthropic — pick one)
    cp .env.example .env
    # Edit .env and set: NOUS_API_KEY=... OR OPENAI_API_KEY=... OR ANTHROPIC_API_KEY=...

    # 4. First run to create ~/.hermes/ config dir
    python hermes.py --version

    # 5. Verify the skills directory exists
    ls ~/.hermes/skills/  # → empty by default, ready for our claude-skills tree
    ```

=== "Windows (рекомендуется WSL2)"

    Официальная поддержка Hermes агентом ориентирована на macOS и Linux. В Windows используйте WSL2 (Ubuntu 22.04+) и следуйте описанным выше шагам для macOS/Linux. Собственная Windows поддерживается только сообществом.

=== "Докер"

    ```bash
    docker run -it --rm \
      -v $HOME/.hermes:/root/.hermes \
      -e NOUS_API_KEY=$NOUS_API_KEY \
      ghcr.io/nousresearch/hermes-agent:latest
    ```

    Тот `-v` флаг устанавливает ваш местный `~/.hermes/` таким образом, скиллы + история сохраняются во всех прогонах. Заменить `NOUS_API_KEY` с любым поставщиком, которого вы настроили.

!!! info "Don't have a Nous account?"
    Агент Hermes поддерживает несколько поставщиков LLM — Nous (по умолчанию), OpenAI, Anthropic и любую конечную точку, совместимую с OpenAI. Вам не нужна учетная запись Nous, если у вас уже есть учетные данные OpenAI или Anthropic. Видишь [Агент Hermes README](https://github.com/NousResearch/hermes-agent#configuration) для полной матрицы поставщиков.

### Шаг 2 — Установите наши скиллы в Hermes { #step-2--install-our-skills-into-hermes }

=== "Сценарий синхронизации (рекомендуется)"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    python scripts/sync-hermes-skills.py --verbose
    ```

    Это символически связывает все 303 скилла в `~/.hermes/skills/claude-skills/` где Гермес обнаруживает их автоматически. Охватывает все 12 доменов, включая дополнения версии 2.7.0 (производительность, маркетинг, исследования).

=== "Единый домен"

    ```bash
    python scripts/sync-hermes-skills.py --domain engineering --verbose
    ```

=== "Режим копирования (переносимый)"

    ```bash
    python scripts/sync-hermes-skills.py --copy --verbose
    ```

    Создает полные копии вместо символических ссылок. Используйте это в системах, где символические ссылки между файловыми системами не работают, или для совместного использования с контейнерами Docker.

=== "Руководство (любой отдельный скилл)"

    ```bash
    # Symlink
    ln -s /path/to/claude-skills/engineering/karpathy-coder ~/.hermes/skills/karpathy-coder

    # Or copy
    cp -r /path/to/claude-skills/engineering/llm-wiki ~/.hermes/skills/llm-wiki
    ```

### Используя скиллы в Hermes { #using-skills-in-hermes }

После установки скиллы доступны через стандартное приложение Hermes discovery:

```
/skills                    # Browse all installed skills (ours show up under claude-skills/)
/<skill-name>              # Invoke any skill directly as a slash command
/skills search karpathy    # Search by keyword
```

Инструмент skill_view от Hermes загружает SKILL.md вводите контент в контекст беседы, точно так же, как это делает Клод Код. Скрипты на Python в `scripts/` подкаталоги запускаются изначально, поскольку Hermes имеет полноценную среду выполнения Python.

### Что работает { #what-works }

| Особенность | Статус | Примечания |
|---------|--------|-------|
| SKILL.md загрузка | ✅ | Идентичный формат frontmatter (agentskills.io ) |
| Скрипты на Python (`scripts/`) | ✅ | Все только для stdlib, у Hermes есть среда выполнения Python |
| Ссылки / шаблоны / ресурсы | ✅ | То же соглашение о каталогах |
| `AGENTS.md` контекст проекта | ✅ | Гермес читает AGENTS.md изначально |
| Слэш-команды (`/<name>`) | ✅ | Автоматически обнаруживается из SKILL.md |
| Саб-агенты | ⚠️ | Гермес использует свой собственный `delegate_tool`, а не инструмент агента Claude Code — файлы агента .md загружаются как контекст , но механизм отправки отличается |
| Плагин Claude Code.json | ➖ | Гермес игнорирует это — не нужно, он сканирует SKILL.md непосредственно |
| Перехватчики (settings.json) | ⚠️ | Другая система зацепления — ручная проводка для конфигурации Hermes.yaml |

### Проверить { #verify }

```bash
# Check how many skills Hermes can see
find ~/.hermes/skills/claude-skills -name "SKILL.md" | wc -l
# Expected: 303 (v2.7.2+)

# Or in Hermes CLI
hermes
> /skills search claude-skills
```

### Обновление { #updating }

```bash
cd claude-skills-ru
git pull origin main
python scripts/sync-hermes-skills.py --verbose
# Existing symlinks are preserved, new skills are added
```

### Шаг 3 — Пошаговое руководство для первого запуска { #step-3--first-run-walkthrough }

Полный цикл от холодной установки до запуска вашего первого скилла:

```bash
# 1. After Steps 1 + 2 above (Hermes installed, skills synced)
hermes

# 2. Check what skills are loaded
> /skills
# → claude-skills/engineering/karpathy-coder
# → claude-skills/research/research
# → claude-skills/productivity/capture
# ... (303 total)

# 3. Invoke a skill — research orchestrator example
> /research What's the state of post-quantum cryptography in 2026?
# → Hermes loads research/research/SKILL.md, runs Q1+Q2 intake,
#   classifies via SIGNALS map, routes to research-pack specialist
#   (litreview here) or runs fallback workflow

# 4. Or browse a skill's docs without running it
> /skill_view claude-skills/engineering/karpathy-coder
# → loads SKILL.md content as context; you can ask questions about it

# 5. Search for a topic
> /skills search "test generation"
# → ranks claude-skills entries by description match
```

### Советы по настройке { #configuration-tips }

Редактировать `~/.hermes/config.yaml` (создано при первом запуске) для настройки того, как Hermes использует наши скиллы:

```yaml
# Recommended config for working with the claude-skills tree
skills:
  search_paths:
    - ~/.hermes/skills/         # Default location (our sync script lands here)
  auto_load:
    - claude-skills/engineering/karpathy-coder  # Always-loaded skills (high-impact, low-token)
    - claude-skills/engineering/grill-me        # Use sparingly — adds intake friction
  display:
    show_category: true   # Group results by claude-skills/<domain>/
    show_description: true
```

### Устранение неполадок { #troubleshooting }

??? question "`/skills` shows 0 results after running the sync script"
    Цель синхронизации может быть неправильной. Проверьте, что на самом деле делал скрипт:
    ```bash
    python scripts/sync-hermes-skills.py --target ~/.hermes/skills --verbose --dry-run
    # Should show 303 skills queued for sync. If 0, your DOMAIN_DIRS list is wrong (regression — file an issue).
    ls -la ~/.hermes/skills/claude-skills/
    # If empty, the sync didn't actually write — check for permission errors above.
    ```

??? question "Symlinks point to a path on someone else's machine"
    Вероятно, вы клонировали форк, который фиксировал символические ссылки с абсолютным путем. Повторно запустите синхронизацию из вашего собственного клона — версия 2.7.2+ генерирует относительные символические ссылки (`../../../../<domain>/...`) , которые работают на разных машинах:
    ```bash
    rm -rf ~/.hermes/skills/claude-skills/
    python scripts/sync-hermes-skills.py --verbose
    ```

??? question "Slash commands like `/research` collide with Hermes's built-ins"
    Hermes сначала решает пользовательские скиллы, так что `/research` от Клода -скиллы выигрывают. Если вместо этого вам нужен встроенный, используйте полный путь: `/skill_view hermes/research`. Чтобы полностью избежать коллизий, переименуйте с помощью символической ссылки: `ln -s ~/.hermes/skills/claude-skills/research/research ~/.hermes/skills/cs-research`.

??? question "Python tools fail with ModuleNotFoundError"
    Наши скрипты доступны только для stdlib по политике — `ModuleNotFoundError` означает, что либо (а) вы используете старый Python (нам требуется версия 3.10+), либо (б) сам скрипт нарушил политику (зафиксировал ошибку). Подтверждаю:
    ```bash
    python3 --version  # Must be ≥ 3.10
    python3 ~/.hermes/skills/claude-skills/engineering/karpathy-coder/scripts/karpathy_lint.py --help
    # Should print help text without errors
    ```

??? question "Hermes can't find SKILL.md but the file exists"
    Гермес ожидает SKILL.md в ** верхней части каталога скиллы**. Наш макет вложенного плагина (`<domain>/<plugin>/skills/<skill>/SKILL.md`) сглаживается скриптом синхронизации — символическая ссылка на `~/.hermes/skills/claude-skills/<domain>/<skill>/` указывает непосредственно на внутреннюю `skills/<skill>/` папка, так что `SKILL.md` находится на верхнем уровне после перехода по символической ссылке. Если какой-либо определенный скилл отсутствует, проверьте:
    ```bash
    ls -la ~/.hermes/skills/claude-skills/<domain>/<skill>/SKILL.md
    # If "No such file", the symlink target is broken — re-run the sync script
    ```

??? question "How do I unsync (remove our skills from Hermes)?"
    ```bash
    rm -rf ~/.hermes/skills/claude-skills/
    # Hermes's own built-in skills are unaffected (they live elsewhere in ~/.hermes/skills/)
    ```

<hr class="section-divider">

## Мистралевая атмосфера { #mistral-vibe }

[Мистралевая атмосфера](https://github.com/mistralai/mistral-vibe) является агентом для кодирования CLI Apache-2.0 с открытым исходным кодом от Mistral AI (версия 2.0, выпущена в январе 2026 года). Он использует [Стандарт скилла агента](https://docs.mistral.ai/mistral-vibe/agents-skills) — то же самое `SKILL.md` + Формат YAML frontmatter используют Claude Code и Hermes агент — так что ** преобразование не требуется **.

!!! tip "Tier: BYO-sync (pre-generated tree available)"
    Репозиторий отправляет предварительно сгенерированный `.vibe/skills/claude-skills/` дерево с **306 символическими ссылками** на **14 доменах**. Вам все еще нужно скопировать / символически связать это дерево в `~/.vibe/skills/` на вашем компьютере — это шаг BYO-синхронизации. Тот `sync-vibe-skills.py` скрипт обрабатывает это с помощью одной команды.

### Пути обнаружения { #discovery-paths }

В соответствии с [официальные документы](https://docs.mistral.ai/mistral-vibe/agents-skills), Vibe сканирует три локации на предмет наличия скилла:

| Путь | Сфера применения |
|------|-------|
| `~/.vibe/skills/` | Пользователь-глобальный (в который записывается наш скрипт синхронизации) |
| `.vibe/skills/` | Проект -местный |
| `.agents/skills/` | Стандартный путь к скиллам агента |

### Шаг 1 — Установите сам Mistral Vibe { #step-1--install-mistral-vibe-itself }

Если у вас еще не установлен Vibe, следуйте инструкциям [Быстрый запуск Vibe](https://docs.mistral.ai/mistral-vibe/introduction/quickstart):

```bash
pip install mistral-vibe
vibe --version    # Verify install
```

Vibe поддерживает обе размещенные модели Mistral (через `MISTRAL_API_KEY`) и автономные конечные точки. Увидеть [Документы Vibe CLI](https://docs.mistral.ai/mistral-vibe/terminal) для настройки поставщика.

### Шаг 2 — Установите наши скиллы в Vibe { #step-2--install-our-skills-into-vibe }

=== "Сценарий синхронизации (рекомендуется)"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/vibe-install.sh
    ```

    Это символическая ссылка на все 306 скилл, объединяющая их в `~/.vibe/skills/claude-skills/` где Vibe обнаруживает их автоматически. Охватывает все 14 доменов.

=== "Единый домен"

    ```bash
    python scripts/sync-vibe-skills.py --domain engineering --verbose
    ```

=== "Режим копирования (переносимый)"

    ```bash
    python scripts/sync-vibe-skills.py --copy --verbose
    ```

    Создает полные копии вместо символических ссылок — полезно для контейнеров Docker или общих файловых систем, где символические ссылки не проходят чисто.

=== "Пользовательская цель"

    ```bash
    python scripts/sync-vibe-skills.py --target /opt/team-vibe/skills/
    ```

    Полезно для установки в масштабах всей команды или изолированных сред.

### Используя скиллы в Vibe { #using-skills-in-vibe }

После установки скиллы становятся доступны через стандартное приложение Vibe discovery (в соответствии с [Документы о агентах Vibe и скиллах](https://docs.mistral.ai/mistral-vibe/agents-skills)):

```
/skills                    # List all installed skills
/<skill-name>              # Invoke a skill by slug as a slash command
```

Vibe также может автоматически загружать скиллы, когда ваша промпта соответствует скиллу пользователя. `description` поле — тот же самый механизм триггера, который использует Claude Code.

### Что работает { #what-works }

| Особенность | Статус | Примечания |
|---------|--------|-------|
| SKILL.md загрузка | ✅ | Идентичный YAML frontmatter (agentskills.io ) |
| Скрипты на Python (`scripts/`) | ✅ | Все они доступны только для stdlib; инструмент Vibe shell запускает их |
| Ссылки / шаблоны / ресурсы | ✅ | То же соглашение о каталогах |
| Слэш-команды (`/<name>`) | ✅ | Автоматически обнаруживается из SKILL.md |
| Саб-агенты | ⚠️ | Vibe использует свою собственную систему субагентов с конфигурациями TOML (`~/.vibe/agents/`) — агент Клод Код `.md` файлы загружаются как контекст, но отправка отличается |
| Плагин Claude Code.json | ➖ | Vibe игнорирует это — сканирует SKILL.md непосредственно |
| Перехватчики (settings.json) | ➖ | Vibe имеет собственную систему подключения; требуется ручная проводка |

### Проверить { #verify }

```bash
# Count installed skills
find ~/.vibe/skills/claude-skills -mindepth 2 -maxdepth 2 -name "SKILL.md" -o -type l | wc -l
# Expected: 306

# Inspect the manifest
cat ~/.vibe/skills/claude-skills/skills-index.json | python3 -m json.tool | head -20

# Or in the Vibe CLI
vibe
> /skills
```

### Обновление { #updating }

```bash
cd claude-skills-ru
git pull origin main
python scripts/sync-vibe-skills.py --verbose
# Existing symlinks are preserved, new skills are added
```

### Устранение неполадок { #troubleshooting }

??? question "Vibe doesn't see the synced skills"
    Убедитесь, что синхронизация выполнена и символические ссылки разрешены:
    ```bash
    ls -la ~/.vibe/skills/claude-skills/engineering/agent-designer/SKILL.md
    # Should print a valid SKILL.md, not "No such file"
    ```
    Если символические ссылки повреждены (исходное хранилище было перемещено), запустите повторно `python scripts/sync-vibe-skills.py --verbose`.

??? question "How do I unsync (remove our skills from Vibe)?"
    ```bash
    rm -rf ~/.vibe/skills/claude-skills/
    # Vibe's own built-in skills are unaffected (they live elsewhere in ~/.vibe/skills/)
    ```

<hr class="section-divider">

## Ссылка на сценарий { #script-reference }

### convert.sh { #convertsh }

```
Usage:
  ./scripts/convert.sh [--tool <name>] [--out <dir>] [--help]

Tools:
  antigravity, cursor, aider, kilocode, windsurf, opencode, augment, all

Options:
  --tool <name>   Convert for a specific tool (default: all)
  --out <dir>     Output directory (default: integrations/)
  --help          Show usage
```

**Примеры:**

```bash
# Convert all skills for all tools
./scripts/convert.sh

# Convert only for Cursor
./scripts/convert.sh --tool cursor

# Custom output directory
./scripts/convert.sh --tool windsurf --out /tmp/my-skills
```

### install.sh { #installsh }

```
Usage:
  ./scripts/install.sh --tool <name> [--target <dir>] [--force] [--help]

Options:
  --tool <name>     Required. Which tool to install for.
  --target <dir>    Project directory (default: current dir, except antigravity)
  --force           Skip overwrite confirmation
  --help            Show usage
```

**Места установки по умолчанию:**

| Инструмент | Цель по умолчанию |
|------|---------------|
| Агент Гермеса | `~/.hermes/skills/claude-skills/` |
| Антигравитация | `~/.gemini/antigravity/skills/` |
| Курсор | `<target>/.cursor/rules/` |
| Помощник | `<target>/CONVENTIONS.md` |
| Код килограмма | `<target>/.kilocode/rules/` |
| Виндсерфинг | `<target>/.windsurf/skills/` |
| Открытый код | `<target>/.opencode/skills/` |
| Увеличить | `<target>/.augment/rules/` |

<hr class="section-divider">

## Устранение неполадок { #troubleshooting }

??? question "I get 'No skills found' when running convert.sh"
    Убедитесь, что вы запускаете скрипт из корневого каталога репозитория, где расположены каталоги скилл.

??? question "Some skills show garbled descriptions"
    Это может произойти с скиллами, использующими сложные многострочные описания YAML. Повторный запуск `convert.sh` — ручки синтаксического анализатора сложены (`>`) и буквальный (`|`) Скаляры YAML.

??? question "Can I use skills from multiple tools at once?"
    Да! Вы можете установить скиллы для Cursor и Windowsf в одном проекте — они используют разные каталоги и не будут конфликтовать.

??? question "How do I update when new skills are added?"
    ```bash
    git pull origin main
    ./scripts/convert.sh --tool all
    ./scripts/install.sh --tool <your-tool> --target . --force
    ```

??? question "Can I convert only specific skills?"
    Пока не с помощью флагов CLI, но вы можете запустить `convert.sh` а затем скопируйте только те скиллы, которые вам нужны `integrations/<tool>/`.

??? question "Do supporting files (scripts, references) work in all tools?"
    Только инструменты, поддерживающие подкаталоги для каждого скилла (Hermes агент, Antigravity, Windsurf, OpenCode), получают полный пакет. Инструменты с плоским файлом (Курсор, помощник, Килограммовый код, Увеличение) позволяют SKILL.md только контент.

??? question "Does Hermes Agent need format conversion?"
    Нет, Гермес использует то же самое agentskills.io SKILL.md форматируйте как наше репозиторий. Просто беги `python scripts/sync-hermes-skills.py --verbose` чтобы символически связать скиллы с `~/.hermes/skills/`. Никакого шага преобразования не требуется.
