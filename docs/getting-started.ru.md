---
title: Install Agent Skills — Claude Code, Codex, Gemini CLI Setup
description: "Как установить 345 скилл агента и 78 плагинов в любой из 13 инструментов для кодирования искусственного интеллекта. Пошаговая настройка Claude Code, OpenAI Codex, Gemini CLI, агента Hermes, Mistral Vibe, OpenClaw, курсора, помощника, виндсерфинга и многого другого — в большинстве случаев занимает менее двух минут."
---

# Приступаем к работе { #getting-started }

Установка скиллы агента на большинстве платформ занимает менее двух минут. Настраивать нечего: ни ключей API, ни зависимостей, ни шага сборки. Выберите свой инструмент ниже, запустите команды, и скиллы заработают.

Новичок здесь? Читать [Что такое скилл агента?](index.md#what-is-an-agent-skill) сначала или сразу переходите к руководству по конкретному инструменту: [Код Клода](guides/best-claude-code-plugins.md), [Кодекс OpenAI](guides/agent-skills-for-codex.md), [Интерфейс Gemini CLI](guides/gemini-cli-skills-guide.md), [Курсор](guides/cursor-skills-guide.md), или [Открытый коготь](guides/openclaw-skills-guide.md).

## Установка { #installation }

Выберите свою платформу и следуйте инструкциям:

=== "Код Клода"

    <ol class="install-steps">
      <li>
        <strong>Add the marketplace</strong>
        <pre><code>/plugin marketplace add imgusev/claude-skills-ru</code></pre>
      </li>
      <li>
        <strong>Install the skills you need</strong>
        <pre><code>/plugin install engineering-skills@claude-code-skills</code></pre>
      </li>
      <li>
        <strong>Use them immediately</strong> — skills activate as slash commands or contextual expertise.
      </li>
    </ol>

=== "Кодекс OpenAI"

    ```bash
    npx agent-skills-cli add imgusev/claude-skills-ru --agent codex
    ```

    Или клонировать и устанавливать вручную:

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    ./scripts/codex-install.sh
    ```

=== "Gemini CLI"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    ./scripts/gemini-install.sh
    ```

    Или воспользуйтесь сценарием синхронизации для создания индекса скилла:

    ```bash
    python3 scripts/sync-gemini-skills.py
    ```

=== "OpenClaw"

    ```bash
    bash <(curl -s https://raw.githubusercontent.com/imgusev/claude-skills-ru/main/scripts/openclaw-install.sh)
    ```

=== "агент Гермеса"

    [Агент Гермеса](https://github.com/NousResearch/hermes-agent) использует тот же самый agentskills.io SKILL.md стандартный — преобразование формата не требуется.

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    python scripts/sync-hermes-skills.py --verbose
    ```

    Скиллы устанавливаются для `~/.hermes/skills/claude-skills/` и автоматически обнаруживаются Гермесом с помощью `/skills` или `/<skill-name>`.

    Параметры синхронизации:

    ```bash
    python scripts/sync-hermes-skills.py --domain engineering  # one domain only
    python scripts/sync-hermes-skills.py --copy                # copy instead of symlink
    python scripts/sync-hermes-skills.py --dry-run             # preview
    ```

=== "Атмосфера Мистраля"

    [Мистралевая атмосфера](https://github.com/mistralai/mistral-vibe) является агентом по кодированию CLI Apache-2.0 с открытым исходным кодом от Mistral AI. Он использует тот же самый agentskills.io SKILL.md стандартный — преобразование формата не требуется.

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/vibe-install.sh
    ```

    Скиллы устанавливаются для `~/.vibe/skills/claude-skills/` (345 скилл в 17 областях) и автоматически обнаруживаются Vibe с помощью `/skills` или `/<skill-name>`. Посмотрите на [официальные документы Vibe](https://docs.mistral.ai/mistral-vibe/agents-skills) для получения подробной информации о формате скилл.

    Параметры синхронизации:

    ```bash
    python scripts/sync-vibe-skills.py --domain engineering   # one domain only
    python scripts/sync-vibe-skills.py --copy                 # copy instead of symlink
    python scripts/sync-vibe-skills.py --dry-run              # preview
    python scripts/sync-vibe-skills.py --target /opt/team/    # custom location
    ```

=== "Курсор"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/convert.sh --tool cursor
    ./scripts/install.sh --tool cursor --target /path/to/project
    ```

=== "Помощник"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/convert.sh --tool aider
    ./scripts/install.sh --tool aider --target /path/to/project
    ```

=== "Виндсерфинг"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/convert.sh --tool windsurf
    ./scripts/install.sh --tool windsurf --target /path/to/project
    ```

=== "Код килограмма"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/convert.sh --tool kilocode
    ./scripts/install.sh --tool kilocode --target /path/to/project
    ```

=== "Открытый код"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/convert.sh --tool opencode
    ./scripts/install.sh --tool opencode --target /path/to/project
    ```

=== "Увеличить"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/convert.sh --tool augment
    ./scripts/install.sh --tool augment --target /path/to/project
    ```

=== "Антигравитация"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/convert.sh --tool antigravity
    ./scripts/install.sh --tool antigravity
    ```

=== "Руководство пользователя"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    # Copy any skill folder to ~/.claude/skills/
    ```

!!! tip "All conversion-based tools at once"
    Преобразование для каждого поддерживаемого инструмента в одной команде:
    ```bash
    ./scripts/convert.sh --tool all
    ```
    Увидеть [Интеграция с несколькими инструментами](integrations.md) страница с подробной документацией по каждому инструменту.

<hr class="section-divider">

## Доступные пакеты { #available-bundles }

Пакеты доменов позволяют установить сразу целую команду скилл-специалистов:

| Связка | Установить команду | Скиллы |
|--------|----------------|--------|
| **Инженерное ядро** | `/plugin install engineering-skills@claude-code-skills` | 51 |
| **Инженерно —продвинутый** | `/plugin install engineering-advanced-skills@claude-code-skills` | 74 |
| **Продукт** | `/plugin install product-skills@claude-code-skills` | 17 |
| **Маркетинг** | `/plugin install marketing-skills@claude-code-skills` | 47 |
| **Регулирование и качество** | `/plugin install ra-qm-skills@claude-code-skills` | 18 |
| **Соответствие требованиям ОС** | `/plugin install compliance-os@claude-code-skills` | 9 |
| **Управление проектами** | `/plugin install pm-skills@claude-code-skills` | 9 |
| **Консультирование на уровне C** | `/plugin install c-level-skills@claude-code-skills` | 61 |
| **Бизнес и рост** | `/plugin install business-growth-skills@claude-code-skills` | 5 |
| **Бизнес-операции** | `/plugin install business-operations-skills@claude-code-skills` | 7 |
| **Коммерческий** | `/plugin install commercial-skills@claude-code-skills` | 8 |
| **Финансы** | `/plugin install finance-skills@claude-code-skills` | 4 |
| **Исследовательские операции** | `/plugin install research-ops-skills@claude-code-skills` | 5 |
| **Markdown для преобразования в HTML** | `/plugin install markdown-html-skills@claude-code-skills` | 5 |

Производительность и исследовательские скиллы поставляются в виде автономных плагинов (например `capture-skill`, `pulse`, `litreview`, `grants`). Просмотрите [маркетплейс плагинов](plugins/index.md) ознакомьтесь с полным списком или установите любой отдельный скилл: `/plugin install skill-name@claude-code-skills`

<hr class="section-divider">

## Использование { #usage }

### Слэш-команды { #slash-commands }

```
/pw:generate     Generate Playwright tests
/pw:fix          Fix flaky test failures
/si:review       Review auto-memory health
/si:promote      Graduate a learning to CLAUDE.md
/cs:board        Trigger a C-suite board meeting
```

### Контекстные промпты { #contextual-prompts }

```
Using the senior-architect skill, review our microservices
architecture and identify the top 3 scalability risks.
```

```
Using the content-creator skill, write a blog post about
AI-augmented development. Optimize for SEO.
```

<hr class="section-divider">

## Инструменты Python { #python-tools }

Инструменты, входящие в комплект каждого скилла, используют только стандартную библиотеку Python — более 550 скриптов, без установки pip, все проверено с помощью `--help` тесты на дым.

```bash
# Security audit a skill before installing
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/

# Analyze brand voice
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py article.txt

# RICE prioritization
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# Generate landing page (TSX + Tailwind)
python3 product-team/landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx

# Tech debt scoring
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase
```

<hr class="section-divider">

## Безопасность { #security }

!!! warning "Always audit untrusted skills"

    Прежде чем устанавливать скиллы из сторонних источников, запустите программу security auditor:

    ```bash
    python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
    ```

    Возвращает **PASS** / **WARN** / **FAIL** с рекомендациями по исправлению. Сканирует на предмет внедрения команд, эксфильтрации данных, внедрения промптов и рисков в цепочке поставок.

<hr class="section-divider">

## Создавая свой собственный { #creating-your-own }

Каждый скилл - это папка:

```
my-skill/
  SKILL.md       # Instructions + workflows
  scripts/       # Python CLI tools (optional)
  references/    # Domain knowledge (optional)
  assets/        # Templates (optional)
```

Увидеть [Фабрика скиллы и агентов](https://github.com/alirezarezvani/claude-code-skill-factory) для получения полного руководства.

<hr class="section-divider">

## Часто задаваемые вопросы { #faq }

??? question "Do I need API keys?"
    Нет. Скиллы работают локально без каких-либо внешних вызовов API. Все инструменты Python используют только stdlib.

??? question "Can I install individual skills instead of bundles?"
    Да. Использование `/plugin install skill-name@claude-code-skills` для любого отдельного скилла.

??? question "Do skills conflict with each other?"
    Нет. Каждый скилл самодостаточен и не имеет перекрестных зависимостей.

??? question "How do I update installed skills?"
    Повторно запустите команду установки. Система плагинов извлекает последнюю версию из маркетплейса.

??? question "Will upgrading break my setup?"
    Нет. Выпуски обратно совместимы — существующие SKILL.md файлы, скрипты и ссылки продолжают работать. Новые скиллы и домены являются только дополнительными.

??? question "Does this work with Gemini CLI?"
    Да. Бежать `./scripts/gemini-install.sh` чтобы настроить скиллы для Gemini CLI. Сценарий синхронизации (`scripts/sync-gemini-skills.py`) автоматически генерирует индекс скилла.

??? question "Does this work with Cursor, Windsurf, Aider, or other tools?"
    Да. Все скиллы 345 могут быть преобразованы в собственные форматы для Cursor, Aider, Kilo Code, Windsurf, OpenCode, Augment и Antigravity. Бежать `./scripts/convert.sh --tool all` а затем установите с помощью `./scripts/install.sh --tool <name>`. Смотри [Интеграция с несколькими инструментами](integrations.md) для получения подробной информации.

??? question "Can I use Agent Skills in ChatGPT?"
    Да. У нас есть [6 Пользовательских GPT](custom-gpts.md) которые привносят скиллы агента непосредственно в ChatGPT — установка не требуется. Просто нажмите и начните общаться в чате.
