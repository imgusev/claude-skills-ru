---
title: Агентские скиллы и плагины для Claude Code, Codex, Gemini CLI и ещё 10 AI-инструментов
description: "345 готовых к использованию агентских скиллов, 78 устанавливаемых плагинов и 90+ слэш-команд в 17 доменах — инженерия, продукт, маркетинг, комплаенс, финансы и исследования. Работает с Claude Code, OpenAI Codex, Gemini CLI, Cursor, Hermes Agent, Mistral Vibe, OpenClaw и ещё 6 инструментами. Открытый исходный код, лицензия MIT, без зависимостей."
hide:
  - toc
  - edit
---

<style>
.md-content__inner > .md-typeset > h1:first-child { display: none; }
</style>

<div class="hero" markdown>

<span class="hero-eyebrow">Открытый исходный код · MIT · 17 доменов · 13 AI-инструментов</span>

# Агентские скиллы { #agent-skills }

Дайте своему AI-агенту разработки настоящую экспертизу в предметной области. Каждый скилл — самодостаточный пакет из воркфлоу, чек-листов, Python-инструментов и справочных знаний, которым агент следует автономно — установите одной командой и получайте более качественный результат.
{ .hero-subtitle }

[Начать](getting-started.md){ .md-button .md-button--primary }
[Смотреть скиллы](skills/index.md){ .md-button }
[GitHub :fontawesome-brands-github:](https://github.com/alirezarezvani/claude-skills){ .md-button }

<div class="stats-strip">
  <div class="stat"><span class="stat-number">345</span><span class="stat-label">Скиллов</span></div>
  <div class="stat"><span class="stat-number">17</span><span class="stat-label">Доменов</span></div>
  <div class="stat"><span class="stat-number">78</span><span class="stat-label">Плагинов</span></div>
  <div class="stat"><span class="stat-number">570+</span><span class="stat-label">Python-инструментов</span></div>
  <div class="stat"><span class="stat-number">90+</span><span class="stat-label">Команд</span></div>
  <div class="stat"><span class="stat-number">13</span><span class="stat-label">AI-инструментов</span></div>
</div>

</div>

<div class="tools-bar" markdown>

<p class="tools-label">Работает с</p>

<div class="tools-grid">
  <a href="guides/best-claude-code-plugins/" class="tool-badge tool-claude">Claude Code</a>
  <a href="guides/agent-skills-for-codex/" class="tool-badge tool-codex">OpenAI Codex</a>
  <a href="guides/gemini-cli-skills-guide/" class="tool-badge tool-gemini">Gemini CLI</a>
  <a href="guides/cursor-skills-guide/" class="tool-badge tool-cursor">Cursor</a>
  <a href="integrations/#hermes-agent" class="tool-badge tool-hermes">Hermes Agent</a>
  <a href="integrations/#mistral-vibe" class="tool-badge tool-vibe">Mistral Vibe</a>
  <a href="integrations/#aider" class="tool-badge tool-aider">Aider</a>
  <a href="integrations/#windsurf" class="tool-badge tool-windsurf">Windsurf</a>
  <a href="integrations/#kilo-code" class="tool-badge tool-kilo">Kilo Code</a>
  <a href="integrations/#opencode" class="tool-badge tool-opencode">OpenCode</a>
  <a href="integrations/#augment" class="tool-badge tool-augment">Augment</a>
  <a href="integrations/#antigravity" class="tool-badge tool-antigravity">Antigravity</a>
  <a href="guides/openclaw-skills-guide/" class="tool-badge tool-openclaw">OpenClaw</a>
</div>

</div>

---

## Что такое агентский скилл? { #what-is-an-agent-skill }

**Агентский скилл** — переносимый пакет экспертизы, который ваш AI-ассистент может подгрузить по требованию. Вместо повторного объяснения стандартов в каждом промпте скилл даёт агенту структурированный воркфлоу, которому он следует одинаково каждый раз — будь то ревью pull request'а, проектирование модели ценообразования или подготовка аудита ISO 27001.

Каждый скилл в этой библиотеке следует одной и той же простой анатомии:

```
skill-name/
├── SKILL.md          # The playbook — workflows, rules, decision frameworks
├── scripts/          # Python CLI tools (stdlib-only, no pip installs)
├── references/       # Curated domain knowledge the agent can consult
└── assets/           # Ready-to-use templates for your team
```

Никаких API-ключей, внешних сервисов, зависимостей между скиллами. Скопируйте папку — или установите плагин — и всё работает.

<ul class="steps">
  <li><strong>Установите</strong> Добавьте маркетплейс в Claude Code или запустите один sync-скрипт для Codex, Gemini CLI, Cursor и ещё 9 инструментов.</li>
  <li><strong>Вызовите</strong> Вызовите слэш-команду вроде <code>/cs:deal-review</code> или просто упомяните скилл в промпте — агент подгрузит плейбук.</li>
  <li><strong>Доставьте</strong> Агент проходит по чек-листам и инструментам скилла, выдавая последовательный, проверяемый результат каждый раз.</li>
</ul>

---

## Что внутри { #whats-inside }

<div class="grid cards" markdown>

-   :material-toolbox:{ .lg .middle } **345 скиллов**

    ---

    Готовые к использованию плейбуки в 17 доменах — от код-ревью и RAG-архитектуры до ценовой стратегии, дизайна клинических исследований и публикации markdown-в-HTML. Каждый поставляется с воркфлоу, Python-инструментами и справочными материалами.

    [:octicons-arrow-right-24: Смотреть скиллы](skills/index.md)

-   :material-puzzle-outline:{ .lg .middle } **78 плагинов**

    ---

    Устанавливаемые одной командой пакеты для Claude Code — установите весь домен или один скилл. Sync-скрипты покрывают Codex CLI, Gemini CLI, Hermes Agent, Mistral Vibe и OpenClaw.

    [:octicons-arrow-right-24: Маркетплейс плагинов](plugins/index.md)

-   :material-robot:{ .lg .middle } **90+ агентов**

    ---

    Мульти-скилл-оркестраторы с собственными персонами — инженерные лиды, C-suite консультанты, исследовательские роутеры и комплаенс-аудиторы, сочетающие скиллы для сложной работы.

    [:octicons-arrow-right-24: Смотреть агентов](agents/index.md)

-   :material-console:{ .lg .middle } **90+ слэш-команд**

    ---

    Мгновенные воркфлоу, которые вы запускаете по имени — планирование спринтов, PRD, OKR, ревью сделок, дизайн SLO, chaos-эксперименты и исследования рынка прямо из терминала.

    [:octicons-arrow-right-24: Смотреть команды](commands/index.md)

-   :material-language-python:{ .lg .middle } **570+ Python-инструментов**

    ---

    Детерминированные CLI-скрипты, поставляемые вместе со скиллами — только стандартная библиотека, без pip install, без вызовов LLM. Скоринг, валидация и анализ, работающие везде, где есть Python.

    [:octicons-arrow-right-24: Начало работы](getting-started.md)

-   :material-account-group:{ .lg .middle } **3 персоны**

    ---

    Ролевые идентичности — Startup CTO, Growth Marketer, Solo Founder — с подобранным набором скиллов, фреймворками суждений и характерным стилем общения.

    [:octicons-arrow-right-24: Познакомиться с персонами](personas/index.md)

-   :material-sitemap:{ .lg .middle } **Оркестрация**

    ---

    Лёгкий протокол координации персон, скиллов и агентов на работе, пересекающей границы доменов — запуски, аудиты и стратегические спринты.

    [:octicons-arrow-right-24: Изучить паттерны](orchestration.md)

-   :material-swap-horizontal:{ .lg .middle } **Поддержка 13 инструментов**

    ---

    Напишите один раз, запускайте везде. Единый скрипт конвертации адаптирует каждый скилл к нативному формату Cursor, Aider, Windsurf, Kilo Code, OpenCode, Augment и Antigravity.

    [:octicons-arrow-right-24: Настройка нескольких инструментов](integrations.md)

-   :material-chat-outline:{ .lg .middle } **6 Custom GPTs**

    ---

    Используйте агентские скиллы прямо в ChatGPT без всякой настройки — Solo Founder, SEO Audit, Content Strategy, CTO Advisor и другие.

    [:octicons-arrow-right-24: Открыть GPTs](custom-gpts.md)

</div>

---

## Скиллы по доменам { #skills-by-domain }

Семнадцать доменов покрывают весь жизненный цикл создания продукта и управления компанией — инженерия, go-to-market, операции, комплаенс и исследования.

<div class="grid cards" markdown>

-   :material-cog:{ .lg .middle } **Инженерия — базовый уровень**

    ---

    Архитектура, фронтенд, бэкенд, фуллстек, QA, DevOps, SecOps, AI/ML, инженерия данных, тестирование Playwright, self-improving agent

    [:octicons-arrow-right-24: 51 скилл](skills/engineering-team/index.md)

-   :material-lightning-bolt:{ .lg .middle } **Инженерия — продвинутый уровень**

    ---

    Agent designer, RAG architect, MCP server builder, CI/CD-пайплайны, SLO architect, chaos engineering, аудит безопасности, отслеживание техдолга

    [:octicons-arrow-right-24: 74 скилла](skills/engineering/index.md)

-   :material-bullseye-arrow:{ .lg .middle } **Продукт**

    ---

    Инструментарий product manager, agile PO, UX-исследования, дискавери, аналитика, дизайн экспериментов, SaaS-скаффолдинг, Apple HIG

    [:octicons-arrow-right-24: 17 скиллов](skills/product-team/index.md)

-   :material-bullhorn:{ .lg .middle } **Маркетинг**

    ---

    Контент, SEO, AEO, CRO, платные каналы, рост, стратегия запуска — 8 специализированных подов со встроенными Python-инструментами аналитики

    [:octicons-arrow-right-24: 47 скиллов](skills/marketing-skill/index.md)

-   :material-star-circle:{ .lg .middle } **Executive-консультирование**

    ---

    Полный набор C-suite консультантов (от CEO до General Counsel), founder-mode боардрум, журналирование решений, фреймворки культуры и стратегии

    [:octicons-arrow-right-24: 61 скилл](skills/c-level-advisor/index.md)

-   :material-shield-check:{ .lg .middle } **Регуляторика и качество**

    ---

    ISO 13485, MDR 2017/745, FDA, ISO 27001, GDPR, CAPA, управление рисками, документация качества

    [:octicons-arrow-right-24: 18 скиллов](skills/ra-qm-team/index.md)

-   :material-shield-lock:{ .lg .middle } **Compliance OS**

    ---

    Оркестратор подготовки к аудиту для готовности ISO 13485, ISO 27001, SOC 2, GDPR, FDA QSR, EU AI Act и ISO 42001

    [:octicons-arrow-right-24: 9 скиллов](skills/compliance-os/index.md)

-   :material-clipboard-check:{ .lg .middle } **Управление проектами**

    ---

    Senior PM, scrum master, эксперты Jira и Confluence, Atlassian admin со встроенным remote MCP

    [:octicons-arrow-right-24: 9 скиллов](skills/project-management/index.md)

-   :material-trending-up:{ .lg .middle } **Бизнес и рост**

    ---

    Customer success, sales engineering, revenue operations, контракты и предложения

    [:octicons-arrow-right-24: 5 скиллов](skills/business-growth/index.md)

-   :material-cog-outline:{ .lg .middle } **Бизнес-операции**

    ---

    Маппинг процессов, управление вендорами, планирование мощностей, внутренние коммуникации, knowledge ops, закупки

    [:octicons-arrow-right-24: 7 скиллов](skills/business-operations/index.md)

-   :material-handshake:{ .lg .middle } **Коммерция**

    ---

    Ценовая стратегия, deal desk, партнёрства, экономика каналов, коммерческая политика, ответы на RFP, прогнозирование

    [:octicons-arrow-right-24: 8 скиллов](skills/commercial/index.md)

-   :material-currency-usd:{ .lg .middle } **Финансы**

    ---

    Финансовый анализ, DCF-оценка, бюджетирование, прогнозирование, SaaS-метрики (ARR, MRR, отток, LTV)

    [:octicons-arrow-right-24: 4 скилла](skills/finance/index.md)

-   :material-magnify:{ .lg .middle } **Исследования**

    ---

    Обзор литературы, гранты, патенты, досье на объекты, силлабусы, автоматизация NotebookLM — с гибридным оркестратором

    [:octicons-arrow-right-24: 8 скиллов](skills/research/index.md)

-   :material-flask:{ .lg .middle } **Research Operations**

    ---

    Дизайн клинических исследований, финансы R&D-программ, оценка рынка и опросы, методология продуктовых исследований

    [:octicons-arrow-right-24: 5 скиллов](skills/research-ops/index.md)

-   :material-lightning-bolt-outline:{ .lg .middle } **Продуктивность**

    ---

    Брейн-дамп захват, настройка и триаж почты, журнал рефлексии, хэндофф сессии, принятие решений market-first

    [:octicons-arrow-right-24: 6 скиллов](skills/productivity/index.md)

-   :material-language-html5:{ .lg .middle } **Markdown в HTML**

    ---

    Превратите markdown в красивый одностраничный HTML — лонгриды, код-ревью и слайд-деки с вашим брендом

    [:octicons-arrow-right-24: 5 скиллов](skills/markdown-html/index.md)

-   :material-web:{ .lg .middle } **Лендинги**

    ---

    Генератор одностраничных HTML-лендингов с четырьмя стилями дизайна и валидатором брендовой палитры

    [:octicons-arrow-right-24: 1 скилл](skills/marketing/index.md)

</div>

---

## Почему команды используют эту библиотеку { #why-teams-use-this-library }

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } **Ноль зависимостей**

    ---

    Каждый Python-инструмент использует только стандартную библиотеку. Без pip install, без API-ключей, без конфигурации. Работает везде, где есть Python.

-   :material-shield-lock:{ .lg .middle } **Безопасность прежде всего**

    ---

    Встроенный аудитор безопасности сканирует любой скилл на вредоносный код, эксфильтрацию данных и prompt injection перед установкой.

-   :material-rocket-launch:{ .lg .middle } **Установка одной командой**

    ---

    Маркетплейс плагинов для Claude Code, sync-скрипты для Codex, Gemini, Hermes и Vibe, и конвертер ещё для семи инструментов.

-   :material-puzzle:{ .lg .middle } **Самодостаточность**

    ---

    Каждый скилл независим — без кросс-зависимостей, без конфликтов. Установите один или все; они работают изолированно.

-   :material-devices:{ .lg .middle } **Мультиплатформенность**

    ---

    Нативная поддержка 13 AI-инструментов разработки. Напишите один раз, конвертируйте в формат любого инструмента автоматически.

-   :material-check-decagram:{ .lg .middle } **Production-grade**

    ---

    Структурированные воркфлоу с контрольными точками валидации — не общие советы. Каждый скилл покрывает end-to-end процесс с именованными результатами.

</div>

---

## Быстрая установка { #quick-install }

=== "Claude Code"

    ```bash
    # Add the marketplace
    /plugin marketplace add imgusev/claude-skills-ru

    # Install any skill bundle
    /plugin install engineering-skills@claude-code-skills
    ```

=== "OpenAI Codex"

    ```bash
    npx agent-skills-cli add imgusev/claude-skills-ru --agent codex
    ```

=== "Gemini CLI"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills && ./scripts/gemini-install.sh
    ```

=== "Hermes Agent"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills
    python scripts/sync-hermes-skills.py --verbose
    # Skills appear in /skills and /<skill-name> automatically
    ```

=== "Mistral Vibe"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills
    ./scripts/vibe-install.sh
    # Skills install to ~/.vibe/skills/claude-skills/; same SKILL.md standard
    ```

=== "Cursor / Windsurf / Aider"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills
    ./scripts/convert.sh --tool cursor    # or windsurf, aider
    ./scripts/install.sh --tool cursor --target /path/to/project
    ```

[Полное руководство по установке](getting-started.md){ .md-button .md-button--primary }
[Настройка нескольких инструментов](integrations.md){ .md-button }

---

## Руководства { #guides }

Пошаговые инструкции по конкретным инструментам, чтобы получить максимум от библиотеки:

- **[Лучшие плагины и скиллы Claude Code](guides/best-claude-code-plugins.md)** — 20 плагинов для начала, по сценариям использования
- **[Агентские скиллы для OpenAI Codex CLI](guides/agent-skills-for-codex.md)** — установка и вызов скиллов в Codex
- **[Руководство по скиллам и плагинам Gemini CLI](guides/gemini-cli-skills-guide.md)** — настройка, индексирование и использование для Gemini CLI
- **[Руководство по скиллам и правилам Cursor](guides/cursor-skills-guide.md)** — конвертация скиллов в формат правил Cursor
- **[Руководство по скиллам OpenClaw](guides/openclaw-skills-guide.md)** — однострочная установка для рабочих пространств OpenClaw

---

**RU-мейнтейнер:** Ilya Gusev — [imgusev.ru](https://imgusev.ru) · [@imgusev](https://t.me/imgusev) · [github.com/imgusev](https://github.com/imgusev). Основано на [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (MIT).
