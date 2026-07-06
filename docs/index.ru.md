---
title: Agent Skills & Plugins for Claude Code, Codex, Gemini CLI & 10 More AI Tools
description: "345 готовых к работе скиллы агента, 78 устанавливаемых плагинов и более 90 слэш—команд в 17 областях - инжиниринг, продукт, маркетинг, соответствие требованиям, финансы и исследования. Работает с Claude Code, OpenAI Codex, Gemini CLI, Cursor, агентом Hermes, Mistral Vibe, OpenClaw и еще 6 инструментами для кодирования искусственного интеллекта. Открытый исходный код, лицензия MIT, нулевые зависимости."
hide:
  - toc
  - edit
---

<style>
.md-содержимое__внутреннее > .md-набор текста > h1:первый дочерний элемент { display: none; }
</style>

<div class="hero" markdown>

<span class="hero-eyebrow">Open source · MIT · 17 domains · 13 AI tools</span>

# Скиллы агента { #agent-skills }

Дайте вашему агенту по кодированию искусственного интеллекта реальный опыт работы в предметной области. Каждый скилл представляет собой автономный пакет воркфлоу, чек-листов, инструментов Python и справочных знаний, которым ваш агент следует автономно — установите одну команду, обеспечьте лучшую работу.
{ .hero-subtitle }

[Приступайте к работе](getting-started.md){ .md-button .md-button--primary }
[Просматривайте скиллы](skills/index.md){ .md-button }
[GitHub :fontawesome-brands-github:](https://github.com/alirezarezvani/claude-skills){ .md-button }

<div class="stats-strip">
  <div class="stat"><span class="stat-number">345</span><span class="stat-label">Skills</span></div>
  <div class="stat"><span class="stat-number">17</span><span class="stat-label">Domains</span></div>
  <div class="stat"><span class="stat-number">78</span><span class="stat-label">Plugins</span></div>
  <div class="stat"><span class="stat-number">570+</span><span class="stat-label">Python Tools</span></div>
  <div class="stat"><span class="stat-number">90+</span><span class="stat-label">Commands</span></div>
  <div class="stat"><span class="stat-number">13</span><span class="stat-label">AI Tools</span></div>
</div>

</div>

<div class="tools-bar" markdown>

<p class="tools-label">Works with</p>

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

## Что такое Скилл агента? { #what-is-an-agent-skill }

Скилл агента ** - это портативный набор знаний, который ваш помощник с искусственным интеллектом может загрузить по запросу. Вместо того чтобы заново объяснять свои стандарты в каждой промптов, скилл предоставляет агенту структурированный воркфлоу, которому каждый раз следует один и тот же путь - будь то ревью запроса на получение, разработка модели ценообразования или подготовка аудита ISO 27001.

Каждый скилл в этой библиотеке соответствует одной и той же простой анатомии:

```
skill-name/
├── SKILL.md          # The playbook — workflows, rules, decision frameworks
├── scripts/          # Python CLI tools (stdlib-only, no pip installs)
├── references/       # Curated domain knowledge the agent can consult
└── assets/           # Ready-to-use templates for your team
```

Никаких API-ключей, никаких внешних сервисов, никаких зависимостей между скиллами. Скопируйте папку — или установите плагин — и это сработает.

<ul class="steps">
  <li><strong>Install</strong> Add the marketplace to Claude Code, or run one sync script for Codex, Gemini CLI, Cursor, and 9 more tools.</li>
  <li><strong>Invoke</strong> Call a slash command like <code>/cs:deal-review</code>, or just mention the skill in a prompt — the agent loads the playbook.</li>
  <li><strong>Ship</strong> The agent works through the skill's checklists and tools, producing consistent, reviewable output every time.</li>
</ul>

---

## Что там внутри { #whats-inside }

<div class="grid cards" markdown>

-   :material-toolbox:{ .lg .middle } **345 Скилл**

    ---

    Готовые к производству плейбуки в 17 областях - от ревью кода и архитектуры RAG до стратегии ценообразования, дизайна клинических исследований и публикации в формате Markdown на HTML. Каждый из них поставляется с воркфлоу, инструментами Python и справочными материалами.

    [:octicons-arrow-right-24: Просматривайте скиллы](skills/index.md)

-   :material-puzzle-outline:{ .lg .middle } **78 плагинов**

    ---

    Устанавливаемые одной командой пакеты для Claude Code — установите целый домен или один скилл. Сценарии синхронизации охватывают Codex CLI, Gemini CLI, агента Hermes, Mistral Vibe и OpenClaw.

    [:octicons-arrow-right-24: Маркетплейс плагинов](plugins/index.md)

-   :material-robot:{ .lg .middle } **Более 90 агентов**

    ---

    Оркестраторы с несколькими скиллами и разными персонажами - ведущие инженеры, консультанты C-suite, исследователи-маршрутизаторы и аудиторы соответствия требованиям, которые сочетают в себе скиллы для выполнения сложной работы.

    [:octicons-arrow-right-24: Просмотр агентов](agents/index.md)

-   :material-console:{ .lg .middle } **Более 90 Слэш-команд**

    ---

    Мгновенные воркфлоу, которыми вы управляете по названию — планирование спринта, PRDS, OKR, ревью сделок, SLO-дизайн, эксперименты с хаосом и маркетинговые исследования - прямо с вашего терминала.

    [:octicons-arrow-right-24: Просмотр команд](commands/index.md)

-   :material-language-python:{ .lg .middle } **Более 570 инструментов Python**

    ---

    Детерминированные CLI—скрипты, поставляемые в комплекте с скиллами - вся стандартная библиотека, нулевая установка pip, никаких вызовов LLM. Оценка, проверка и анализ, которые выполняются везде, где работает Python.

    [:octicons-arrow-right-24: Приступаем к работе](getting-started.md)

-   :material-account-group:{ .lg .middle } ** 3 персонажа**

    ---

    Ролевая идентичность — технический директор стартапа, специалист по маркетингу роста, основатель—одиночка - с тщательно подобранными скиллами, фреймворками суждений и различными стилями общения.

    [:octicons-arrow-right-24: Знакомьтесь с персонажами](personas/index.md)

-   :material-sitemap:{ .lg .middle } **Оркестрация**

    ---

    Облегченный протокол для координации персоналий, скилл—групп и агентов в работе, которая пересекает границы домена - запуски, аудиты и стратегические спринты.

    [:octicons-arrow-right-24: Изучайте закономерности](orchestration.md)

-   :material-swap-horizontal:{ .lg .middle } **Поддержка 13 инструментов**

    ---

    Напиши один раз, беги везде. Единый сценарий преобразования адаптирует каждый скилл к родному формату Cursor, Aider, Windsurf, Kilo Code, OpenCode, Augment и Antigravity.

    [:octicons-arrow-right-24: Настройка нескольких инструментов](integrations.md)

-   :material-chat-outline:{ .lg .middle } **6 пользовательских GPT**

    ---

    Используйте скиллы агента непосредственно в ChatGPT с нулевой настройкой — основатель Solo, SEO-аудит, контент-стратегия, технический директор-консультант и многое другое.

    [:octicons-arrow-right-24: Открытые GPTS](custom-gpts.md)

</div>

---

## Скиллы в разбивке по предметной области { #skills-by-domain }

Семнадцать областей охватывают полный жизненный цикл создания продукта и управления компанией — проектирование, вывод на рынок, операции, соответствие требованиям и исследования.

<div class="grid cards" markdown>

-   :material-cog:{ .lg .middle } **Инженерное ядро**

    ---

    Архитектура, frontend, backend, fullstack, QA, DevOps, SecOps, AI/ML, разработка данных, драматургическое тестирование, самосовершенствующийся агент

    [:octicons-arrow-right-24: 51 скилл](skills/engineering-team/index.md)

-   :material-lightning-bolt:{ .lg .middle } **Инженерно —продвинутый**

    ---

    Дизайнер агентов, архитектор RAG, разработчик серверов MCP, пайплайны CI/CD, архитектор SLO, разработка хаоса, аудит безопасности, отслеживание технической задолженности

    [:octicons-arrow-right-24: 74 скилла](skills/engineering/index.md)

-   :material-bullseye-arrow:{ .lg .middle } **Продукт**

    ---

    Инструментарий менеджера по продукту, agile PO, UX-исследования, открытия, аналитика, проектирование экспериментов, SaaS-скаффолдинг, Apple HIG

    [:octicons-arrow-right-24: 17 скиллы](skills/product-team/index.md)

-   :material-bullhorn:{ .lg .middle } **Маркетинг**

    ---

    Контент, SEO, AEO, CRO, платные каналы, рост, стратегия запуска — 8 специализированных модулей со встроенными инструментами аналитики на Python

    [:octicons-arrow-right-24: 47 скилл](skills/marketing-skill/index.md)

-   :material-star-circle:{ .lg .middle } **Консультирование на уровне С**

    ---

    Полный набор консультантов (от генерального директора до главного юрисконсульта), зал заседаний в режиме учредителя, ведение журнала решений, фреймворки культуры и стратегии.

    [:octicons-arrow-right-24: 61 скилл](skills/c-level-advisor/index.md)

-   :material-shield-check:{ .lg .middle } **Регулирование и качество**

    ---

    ISO 13485, MDR 2017/745, FDA, ISO 27001, GDPR, CAPA, управление рисками, документация по качеству

    [:octicons-arrow-right-24: 18 скилл](skills/ra-qm-team/index.md)

-   :material-shield-lock:{ .lg .middle } **Соответствие требованиям ОС**

    ---

    Оркестратор аудита-подготовка к ISO 13485, ISO 27001, SOC 2, GDPR, FDA QSR, EU AI Act и готовность к ISO 42001

    [:octicons-arrow-right-24: 9 скилл](skills/compliance-os/index.md)

-   :material-clipboard-check:{ .lg .middle } **Управление проектами**

    ---

    Старший PM, scrum-мастер, эксперты Jira и Confluence, администратор Atlassian с подключенным удаленным MCP

    [:octicons-arrow-right-24: 9 скилл](skills/project-management/index.md)

-   :material-trending-up:{ .lg .middle } **Бизнес и рост**

    ---

    Успех клиентов, организация продаж, операции по получению доходов, контракты и предложения

    [:octicons-arrow-right-24: 5. скиллы](skills/business-growth/index.md)

-   :material-cog-outline:{ .lg .middle } **Бизнес-операции**

    ---

    Отображение процессов, управление поставщиками, планирование производственных мощностей, внутренняя связь, обмен знаниями, закупки

    [:octicons-arrow-right-24: 7. скиллы](skills/business-operations/index.md)

-   :material-handshake:{ .lg .middle } **Коммерческий**

    ---

    Ценовая стратегия, отдел заключения сделок, партнерские отношения, экономика каналов сбыта, коммерческая политика, реакция на запросы клиентов, прогнозирование

    [:octicons-arrow-right-24: 8 скилл](skills/commercial/index.md)

-   :material-currency-usd:{ .lg .middle } **Финансы**

    ---

    Финансовый анализ, оценка DCF, бюджетирование, прогнозирование, показатели SaaS (ARR, MRR, отток, LTV)

    [:octicons-arrow-right-24: 4 скилла](skills/finance/index.md)

-   :material-magnify:{ .lg .middle } **Исследование**

    ---

    Ревью литературы, гранты, патенты, досье организаций, учебные программы, NotebookLM автоматизация — с гибридным оркестратором

    [:octicons-arrow-right-24: 8 скилл](skills/research/index.md)

-   :material-flask:{ .lg .middle } **Исследовательские операции**

    ---

    Разработка клинических исследований, финансирование программ НИОКР, определение размера рынка и опросы, методология исследования продукта

    [:octicons-arrow-right-24: 5. скиллы](skills/research-ops/index.md)

-   :material-lightning-bolt-outline:{ .lg .middle } **Производительность**

    ---

    Сбор мозговой информации, настройка и сортировка входящих сообщений, журнал размышлений, хэндофф сессии, принятие решений, ориентированных на рынок

    [:octicons-arrow-right-24: 6. скиллы](skills/productivity/index.md)

-   :material-language-html5:{ .lg .middle } **Markdown для преобразования в HTML**

    ---

    Превратите Markdown в красивые однофайловые HTML-документы в расширенной форме, ревью кода и слайд—шоу с вашим брендом

    [:octicons-arrow-right-24: 5. скиллы](skills/markdown-html/index.md)

-   :material-web:{ .lg .middle } **Целевые страницы**

    ---

    Однофайловый генератор целевых страниц в HTML-формате с четырьмя стилями оформления и средством проверки палитры брендов

    [:octicons-arrow-right-24: 1 скилл](skills/marketing/index.md)

</div>

---

## Почему команды используют эту библиотеку { #why-teams-use-this-library }

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } **Нулевые зависимости**

    ---

    Каждый инструмент Python использует только стандартную библиотеку. Никаких установок pip, никаких ключей API, никакой конфигурации. Работает везде, где работает Python.

-   :material-shield-lock:{ .lg .middle } **Безопасность превыше всего**

    ---

    Встроенный аудитор безопасности проверяет любой скилл на наличие вредоносного кода, утечки данных и внедрения промптов перед его установкой.

-   :material-rocket-launch:{ .lg .middle } **Установка одной командой**

    ---

    Плагин маркетплейс для Claude Code, скрипты синхронизации для Codex, Gemini, Hermes и Vibe, а также конвертер для еще семи инструментов.

-   :material-puzzle:{ .lg .middle } **Автономный**

    ---

    Каждый скилл независим — никаких перекрестных зависимостей, никаких конфликтов. Установите один или все; они работают изолированно.

-   :material-devices:{ .lg .middle } **Мультиплатформенность**

    ---

    Встроенная поддержка 13 инструментов для кодирования с использованием искусственного интеллекта. Напишите один раз, автоматически преобразуйте в формат любого инструмента.

-   :material-check-decagram:{ .lg .middle } **Производственный сорт**

    ---

    Структурированные воркфлоу с контрольными точками проверки — не общий совет. Каждый скилл охватывает сквозной процесс с именованными конечными результатами.

</div>

---

## Быстрая установка { #quick-install }

=== "Код Клода"

    ```bash
    # Add the marketplace
    /plugin marketplace add imgusev/claude-skills-ru

    # Install any skill bundle
    /plugin install engineering-skills@claude-code-skills
    ```

=== "Кодекс OpenAI"

    ```bash
    npx agent-skills-cli add imgusev/claude-skills-ru --agent codex
    ```

=== "Gemini CLI"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru && ./scripts/gemini-install.sh
    ```

=== "агент Гермеса"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    python scripts/sync-hermes-skills.py --verbose
    # Skills appear in /skills and /<skill-name> automatically
    ```

=== "Атмосфера Мистраля"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/vibe-install.sh
    # Skills install to ~/.vibe/skills/claude-skills/; same SKILL.md standard
    ```

=== "Курсор / Виндсерфинг / Помощник"

    ```bash
    git clone https://github.com/imgusev/claude-skills-ru.git
    cd claude-skills-ru
    ./scripts/convert.sh --tool cursor    # or windsurf, aider
    ./scripts/install.sh --tool cursor --target /path/to/project
    ```

[Полное руководство по установке](getting-started.md){ .md-button .md-button--primary }
[Настройка нескольких инструментов](integrations.md){ .md-button }

---

## Направляющие { #guides }

Пошаговые инструкции по использованию конкретных инструментов для получения максимальной отдачи от библиотеки:

- **[Лучшие плагины и скиллы Claude Code](guides/best-claude-code-plugins.md)** — 20 плагинов для начала, в зависимости от варианта использования
- **[Скиллы агента для OpenAI Codex CLI](guides/agent-skills-for-codex.md)** — установите и активируйте скиллы в Codex
- **[Руководство по скиллам и плагинам Gemini CLI](guides/gemini-cli-skills-guide.md)** — настройка, индексирование и использование для Gemini CLI
- **[Руководство по скиллам и правилам для агента курсора](guides/cursor-skills-guide.md)** — преобразовать скиллы в формат правил курсора
- **[Руководство по скиллам OpenClaw](guides/openclaw-skills-guide.md)** — однострочная установка для рабочих пространств OpenClaw

---

**Сопровождающий RU:** Илья Гусев — [imgusev.ru](https://imgusev.ru) · [@imgusev](https://t.me/imgusev) · [github.com/imgusev](https://github.com/imgusev). Основанный на [алирезарезвани/Клод-скиллы](https://github.com/alirezarezvani/claude-skills) (Массачусетский технологический институт).
