🇬🇧 Английский · 🇷🇺 [Русский](README.md)

# Скиллы Claude Code и плагины — Скиллы агента для каждого инструмента кодирования { #claude-code-skills--plugins--agent-skills-for-every-coding-tool }

**354 готовых к использованию скилла Claude Code, плагины и скиллы агентов для 13 инструментов кодирования с использованием искусственного интеллекта.**

Наиболее полная библиотека с открытым исходным кодом Claude Code скиллы и плагины для агентов — также работает с OpenAI Codex, Gemini CLI, Cursor и еще 9 агентами по кодированию. Многоразовые экспертные пакеты, охватывающие инжиниринг, DevOps, маркетинг (вкл. AEO — Оптимизация системы ответов для цитирования LLM), безопасность (предварительное использование хуков), соответствие требованиям, консультации на уровне C (вкл. финансовый директор в режиме основателя/CMO/CRO/CPO/COO/CHRO/CISO/GC/CDO/CAIO/CCO/VPE персоны + 21 /cs:* слэш-команды), производительность (захват / электронная почта / отражение), набор академических исследований (litreview/гранты / досье / патент/ учебная программа/pulse/notebooklm/deep-research + гибридный маршрутизатор) и исследовательские операции на предприятии (клинические исследования/финансовые исследования/исследование рынка/исследование продукта, версия 2.9.0).

** Работает с:** Кодом Клода · Кодексом OpenAI · Gemini CLI · OpenClaw · агентом Hermes[^hermes] · Атмосфера Мистраля[^vibe] · Курсор · Помощник · Виндсерфинг · Килограммовый код · Открытый код · Дополнение · Антигравитация

[^hermes]: агент Hermes - это ** уровень BYO-sync**: репозиторий отправляет предварительно сгенерированный `.hermes/skills/claude-skills/` дерево, но ты бежишь `python scripts/sync-hermes-skills.py` один раз локально установить в `~/.hermes/skills/`. Использует тот же самый agentskills.io SKILL.md стандартный — без преобразования формата.
[^vibe]: Mistral Vibe также является ** уровнем BYO-sync**: репозиторий отправляет предварительно сгенерированный `.vibe/skills/claude-skills/` дерево, беги `./scripts/vibe-install.sh` один раз локально установить в `~/.vibe/skills/` То же самое agentskills.io SKILL.md стандартный — без преобразования формата. Документы: <https://docs.mistral.ai/mistral-vibe/agents-skills>.

[![Лицензия: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Скиллы](https://img.shields.io/badge/Skills-354-brightgreen?style=for-the-badge)](#skills-overview)
[![Агенты](https://img.shields.io/badge/Agents-96-blue?style=for-the-badge)](#agents)
[![Персонажи](https://img.shields.io/badge/Personas-7-purple?style=for-the-badge)](#personas)
[![Команды](https://img.shields.io/badge/Commands-102-orange?style=for-the-badge)](#commands)
[![Звезды](https://img.shields.io/github/stars/alirezarezvani/claude-skills?style=for-the-badge)](https://github.com/alirezarezvani/claude-skills/stargazers)
[![Проверка навыков подтверждена](https://img.shields.io/badge/SkillCheck-Validated-4c1?style=for-the-badge)](https://getskillcheck.com)

> ** Более 5200 звезд на GitHub ** — самая полная библиотека плагинов для скилл и агента Claude Code с открытым исходным кодом.

---

## Что такое Скиллы Claude Code и плагины для агентов? { #what-are-claude-code-skills--agent-plugins }

Скиллы Claude Code (также называемые скиллами агента или плагинами для агентов кодирования) представляют собой модульные пакеты инструкций, которые предоставляют агентам по кодированию ИИ знания в предметной области, которых у них нет "из коробки". Каждый скилл включает в себя:

- **SKILL.md ** — структурированные инструкции, воркфлоу и фреймворки для принятия решений
- **Инструменты Python** — 593 CLI-скрипта (все только для stdlib, установка без pip)
- **Справочные материалы** — 711 шаблонов, чек-листов и файлов знаний по конкретной предметной области

** Один репозиторий, тринадцать платформ.** Изначально работает как плагины Claude Code, скиллы агента Codex, скиллы Gemini CLI, скиллы агента Hermes, скиллы Mistral Vibe и преобразуется в другие инструменты с помощью `scripts/convert.sh`. Все 593 инструмента Python запускаются везде, где работает Python.

### Скиллы против агентов против персонажей { #skills-vs-agents-vs-personas }

| | Скиллы | Агенты | Персонажи |
|---|---|---|---|
| **Цель** | Как выполнить задачу | Какую задачу выполнить | Кто думает |
| **Сфера применения** | Единый домен | Единый домен | Междоменный |
| **Голос** | Нейтральный | Профессиональный | Ориентированный на личность |
| **Пример** | "Выполните следующие действия для SEO" | "Проведите аудит безопасности" | "Думай как технический директор стартапа" |

Все трое работают вместе. Видишь [Оркестрация](#orchestration) о том, как их сочетать.

---

## Быстрая установка { #quick-install }

### Gemini CLI (новый) { #gemini-cli-new }

```bash
# Clone the repository
git clone https://github.com/imgusev/claude-skills-ru.git
cd claude-skills-ru

# Run the setup script
./scripts/gemini-install.sh

# Start using skills
> activate_skill(name="senior-architect")
```

### Код Клода (рекомендуется) { #claude-code-recommended }

```bash
# Add the marketplace
/plugin marketplace add imgusev/claude-skills-ru

# Install by domain
/plugin install engineering-skills@claude-code-skills          # 24 core engineering
/plugin install engineering-advanced-skills@claude-code-skills  # 25 POWERFUL-tier
/plugin install product-skills@claude-code-skills               # 12 product skills
/plugin install marketing-skills@claude-code-skills             # 43 marketing skills
/plugin install ra-qm-skills@claude-code-skills                 # 12 regulatory/quality
/plugin install pm-skills@claude-code-skills                    # 6 project management
/plugin install c-level-skills@claude-code-skills               # 28 C-level advisory (full C-suite)
/plugin install business-growth-skills@claude-code-skills       # 4 business & growth
/plugin install finance-skills@claude-code-skills               # 2 finance (analyst + SaaS metrics)

# Or install individual skills
/plugin install skill-security-auditor@claude-code-skills       # Security scanner
/plugin install playwright-pro@claude-code-skills                  # Playwright testing toolkit
/plugin install self-improving-agent@claude-code-skills         # Auto-memory curation
/plugin install content-creator@claude-code-skills              # Single skill
```

### Кодекс OpenAI { #openai-codex }

```bash
npx agent-skills-cli add imgusev/claude-skills-ru --agent codex
# Or: git clone + ./scripts/codex-install.sh
```

### Открытый коготь { #openclaw }

```bash
bash <(curl -s https://raw.githubusercontent.com/imgusev/claude-skills-ru/main/scripts/openclaw-install.sh)
```

### Ручная установка { #manual-installation }

```bash
git clone https://github.com/imgusev/claude-skills-ru.git
# Copy any skill folder to ~/.claude/skills/ (Claude Code) or ~/.codex/skills/ (Codex)
```

---

## Поддержка нескольких инструментов (новинка) { #multi-tool-support-new }

** Преобразуйте все 345 скилл в 9 инструментов для кодирования искусственного интеллекта ** с помощью одного скрипта:

| Инструмент | Формат | Установить |
|------|--------|---------|
| **Курсор** | `.mdc` правила | `./scripts/install.sh --tool cursor --target .` |
| **Помощник** | `CONVENTIONS.md` | `./scripts/install.sh --tool aider --target .` |
| **Код килограмма** | `.kilocode/rules/` | `./scripts/install.sh --tool kilocode --target .` |
| **Виндсерфинг** | `.windsurf/skills/` | `./scripts/install.sh --tool windsurf --target .` |
| **Открытый код** | `.opencode/skills/` | `./scripts/install.sh --tool opencode --target .` |
| **Увеличить** | `.augment/rules/` | `./scripts/install.sh --tool augment --target .` |
| **Антигравитация** | `~/.gemini/antigravity/skills/` | `./scripts/install.sh --tool antigravity` |
| **Агент "Гермес"** | `~/.hermes/skills/` | `python scripts/sync-hermes-skills.py --verbose` |
| **Атмосфера Мистраля** | `~/.vibe/skills/` | `./scripts/vibe-install.sh` |

**Как это работает:**

```bash
# 1. Convert all skills to all tools (takes ~15 seconds)
./scripts/convert.sh --tool all

# 2. Install into your project (with confirmation)
./scripts/install.sh --tool cursor --target /path/to/project

# Or use --force to skip confirmation:
./scripts/install.sh --tool aider --target . --force

# 3. Verify
find .cursor/rules -name "*.mdc" | wc -l  # Should show 346
```

**Каждый инструмент получает:**
- ✅ Все 345 скилл-команд преобразованы в родной формат
- ✅ README для каждого инструмента с шагами установки/проверки/обновления
- ✅ Поддержка скриптов, ссылок, шаблонов, где это применимо
- ✅ Нулевая работа по преобразованию вручную

Бежать `./scripts/convert.sh --tool all` для локального создания выходных данных, специфичных для конкретного инструмента.

---

## Обзор скиллы { #skills-overview }

**354 скилла в 18 областях:**

| Домен | Скиллы | Основные моменты | Детали |
|--------|--------|------------|---------|
| **🔧 Инженерное ядро** | 52 | Архитектура, frontend, backend, fullstack, QA, DevOps, SecOps, AI/ML, данные, Dramager Pro (тестирование, исправление ошибок, миграции), самосовершенствующийся агент (автоматическое управление памятью), пакет безопасности, аудит a11y, ** именованный-персона-состязательный-ревью** (ревью с помощью названных инженерных концепций) | [инженерная команда/](engineering-team/) |
| **⚡ Инженерия — МОЩНАЯ** | 80 | Разработчик агентов, RAG-архитектор, разработчик баз данных, CI/CD builder, аудитор безопасности, MCP builder, AgentHub, Helm charts, Terraform, самооценка, llm-wiki, tc-tracker, агент автоматического поиска, ** портфель надежности** (feature-flags-архитектор, kubernetes-оператор, хаос-инжиниринг, slo-архитектор), гейт-корабль, руководство по безопасности перед использованием инструмента, ** скиллы Мэтта Покока** (написание скилла, пещерный человек, гриль-я, хэндофф, гриль-с-документами), ** программист с нулевыми галлюцинациями** (Обсудить→Сопоставить→Разложить→Выполнить→Проверить) | [инженерное дело/](engineering/) |
| **🎯 Продукт** | 17 | Менеджер по продукту, agile PO, стратег, исследователь UX, дизайн пользовательского интерфейса, целевые страницы, SaaS-скаффолдер, аналитика, разработчик экспериментов, discovery, коммуникатор дорожной карты, code-to-prd, эксперт Apple-hig | [команда разработчиков/](product-team/) |
| **📣 Маркетинг** | 48 | 8 модулей: Контент, SEO + AEO (`aeo` — Аудит E-E-A-T, отслеживание цитирования в 5 LLMs) + локальный (`local-seo-manager` — GBP/NAP/Map-Pack), CRO, каналы, рост, аналитика, продажи + контекстная основа + маршрутизатор оркестрации | [маркетинг-скилл/](marketing-skill/) |
| **🚀 Производительность** | 7 | `capture` (от выброса мозгов к действию), `email` сопряжение (входящие-настройка + входящие-сортировка), `reflect` (журнал), `handoff` (Вдохновленный Мэттом Пококом), `andreessen` (режим принятия решения, ориентированного на рынок), `roast` (панель идей с 5 углами обзора → ПЕРЕЙТИ/ИЗМЕНИТЬ ФОРМУ/УНИЧТОЖИТЬ) | [производительность/](productivity/) |
| **🎨 Маркетинг (высший уровень)** | 1 | `landing` — генератор однофайловых HTML-лендингов (4 стиля оформления, шаблоны GSAP, валидатор палитры брендов) | [маркетинг/](marketing/) |
| **🔬 Исследовательская (академическая)** | 9 | `research` оркестратор (гибридный маршрутизатор + резервный вариант) + 8 специалистов: `pulse`, `litreview`, `grants` (NIH), `dossier`, `patent`, `syllabus`, `notebooklm`, `deep-research` (метаисследование, основанное на строгости) | [исследование/](research/) |
| **🧪 Исследовательские операции** ✨Версия 2.9.0 | 5 | Корпоративное/кросс-функциональное исследование: оркестратор + `clinical-research` (дизайн исследования), `research-finance` (Финансирование программы НИОКР), `market-research` (определение размера/опрос/сегментация), `product-research` (исследование пользователей) — каждый с онбордингом + кастомизацией + мостом автоматического поиска по выбору | [исследовательские операции/](research-ops/) |
| **📋 Управление проектами** | 9 | Старший PM, scrum-мастер, Jira, Confluence, администратор Atlassian, шаблоны + в комплекте Atlassian Remote MCP | [управление проектами/](project-management/) |
| **🏥 Регулирование и контроль качества** | 19 | ISO 13505, MDR 2017/745, FDA, ISO 27001, GDPR, SOC 2, CAPA, управление рисками, квитанции о принятии решений агентом (квитанции о действиях, подписанные PQ) | [ra-qm-команда/](ra-qm-team/) |
| **🛡️ Соответствие требованиям ОС** | 9 | Операционная система соответствия требованиям — средства контроля, доказательства, аудит -воркфлоу готовности | [соответствие требованиям-ос/](compliance-os/) |
| **💼 Консультация на уровне C** | 68 | Полный набор C-suite (генеральный директор/технический директор/финансовый директор по финансам/CMO/CRO/CPO/COO/CHRO/CISO/GC/CDO/CAIO/CCO/VPE) + агенты в режиме учредителя + оркестрация + заседания правления + культура и сотрудничество | [советник c-уровня/](c-level-advisor/) |
| **📈 Бизнес и рост** | 5 | Успех клиентов, инженер по продажам, управление доходами, контракты и предложения, инструментарий BizDev | [рост бизнеса/](business-growth/) |
| **🏭 Бизнес - операции** | 7 | Оркестратор + картограф процессов, управление поставщиками, планирование производственных мощностей, внутренняя связь, управление знаниями, оптимизатор закупок | [бизнес-операции/](business-operations/) |
| **🤝 Коммерческий** | 8 | Оркестратор + стратег по ценообразованию, отдел заключения сделок, архитектор партнерских отношений, экономика каналов, коммерческая политика, ответчик на запросы, коммерческий прогнозист | [коммерческий/](commercial/) |
| **finance Финансы** | 4 | Финансовый аналитик (DCF, бюджетирование, прогнозирование), тренер по показателям SaaS, консультант по бизнес-инвестициям | [финансы/](finance/) |
| **Библиотека циклов🔄** | 1 | `loop-library` — обнаружение, нахождение, аудит/ремонт, адаптация и проектирование ограниченных циклов AI-агента; считывает текущий каталог из signals.forwardfuture.ai во время выполнения (дословно передано из [Вперед-Будущее/цикл-библиотека](https://github.com/Forward-Future/loop-library)) | [цикл-библиотека/](loop-library/) |
| **📄 Markdown → HTML** | 5 | `markdown-html-orchestrator` (маршрутизатор doctype) + `design-system` (Фирменные токены WCAG-AA) + `md-document` (удлиненная форма) + `md-review` (ревью кода 2-col) + `md-slides` (однофайловая колода) — конвертер Markdown в интерактивныйHTML | [Markdown-HTML/](markdown-html/) |

---

## Персонажи { #personas }

Предварительно настроенные идентификаторы агентов с заданными скиллами, воркфлоу и различными стилями общения. Персонажи выходят за рамки "используй эти скиллы" — они определяют, как агент мыслит, расставляет приоритеты и общается.

| Персона | Домен | Лучше всего подходит для |
|---------|--------|----------|
| [**Технический директор стартапа**](agents/personas/startup-cto.md) | Проектирование + Стратегия | Архитектурные решения, выбор технологического пакета, формирование команды, техническая экспертиза |
| [**Специалист по маркетингу роста**](agents/personas/growth-marketer.md) | Маркетинг + Рост | Рост, основанный на контенте, стратегия запуска, оптимизация каналов, начальный маркетинг |
| [**Основатель-одиночка**](agents/personas/solo-founder.md) | Междоменный | Стартапы одного человека, побочные проекты, создание MVP, ношение всех шляп |

**Использование:**
```bash
# Claude Code
cp agents/personas/startup-cto.md ~/.claude/agents/

# Any tool
./scripts/convert.sh --tool cursor  # Converts personas too
```

Видишь [агенты/персонажи/](agents/personas/) для получения подробной информации. Создайте свой собственный с помощью [TEMPLATE.md](agents/personas/TEMPLATE.md).

---

## Оркестрация { #orchestration }

Облегченный протокол для координации персоналий, скилл-групп и агентов в работе, которая пересекает границы домена. Никакого фреймворка не требуется.

** Четыре паттерна:**

| Узор | Что | Когда |
|---------|------|------|
| **Одиночный спринт** | Меняйте персонажей на разных этапах проекта | Сайд-проекты, MVP, сольные основатели |
| **Глубокое погружение в домен** | Одна персона + несколько сложенных скиллы | Ревью архитектуры, аудит соответствия |
| **Хэндофф с несколькими агентами** | Персонажи ревью к результатам работы друг друга | Решения с высокими ставками, готовность к запуску |
| **Цепочка скилла** | Последовательные скиллы, персона не требуется | Пайплайны контента, повторяемые чек-листы |

**Пример: 6-недельный запуск продукта**
```
Week 1-2: startup-cto + aws-solution-architect + senior-frontend → Build
Week 3-4: growth-marketer + launch-strategy + copywriting + seo-audit → Prepare
Week 5-6: solo-founder + email-sequence + analytics-tracking → Ship and iterate
```

Видишь [оркестрация/ОРКЕСТРАЦИЯ.md](orchestration/ORCHESTRATION.md) для получения полного протокола и примеров.

---

## МОЩНЫЙ уровень { #powerful-tier }

25 продвинутых скилл с глубокими производственными возможностями:

| Скилл | Что он делает |
|-------|-------------|
| **агент-дизайнер** | Оркестрация с несколькими агентами, схемы инструментов, оценка производительности |
| **агент-воркфлоу-дизайнер** | Шаблоны последовательного, параллельного, маршрутизатора, оркестратора и вычислителя |
| **тряпичный архитектор** | Конструктор пайплайнов RAG, оптимизатор фрагментации, оценщик поиска |
| **конструктор баз данных** | Анализатор схем, генерация ERD, оптимизатор индексов, генератор миграции |
| **база данных-схема-конструктор** | Требования → миграции, типы, исходные данные, политики RLS |
| **миграция-архитектор** | Планировщик миграции, средство проверки совместимости, генератор отката |
| **скилл-аудитор по безопасности** | Security Гейт безопасности — сканируйте скиллы на наличие вредоносного кода перед установкой |
| **ci-cd-пайплайн-конструктор** | Анализировать стек → генерировать действия GitHub / конфигурации GitLab CI |
| **mcp-конструктор серверов** | Создавайте серверы MCP на основе спецификаций OpenAPI |
| **pr-ревью-эксперт** | Анализ радиуса поражения, сканирование системы безопасности, дельта охвата |
| **api-разработчик-рецензент** | Линтер REST API, детектор критических изменений, система показателей проектирования |
| **api-набор тестов-конструктор** | Сканировать маршруты API → генерировать полные наборы тестов |
| **аудитор зависимостей** | Многоязычный сканер, соответствие лицензиям, планировщик обновлений |
| **наблюдаемость-дизайнер** | Конструктор SLO, оптимизатор оповещений, генератор дашбордов |
| **профилировщик производительности** | Профилирование Node/Python/Go, анализ пакетов, нагрузочное тестирование |
| **монорепо-навигатор** | Управление рабочим пространством Turborepo/Nx/pnpm и анализ воздействия |
| **журнал изменений-генератор** | Обычные фиксации → структурированные журналы изменений |
| **кодовая база- онбординг** | Автоматическое создание документов для онбординга на основе анализа кодовой базы |
| **рансбук-генератор** | Кодовая база → операционные рансбуки с командами |
| **git-worktree-менеджер** | Параллельный разработчик с изоляцией портов, синхронизацией env |
| **env-секреты-менеджер** | .управление env, обнаружение утечек, воркфлоу ротации |
| **инцидент - командир** | Плейбук для реагирования на инциденты, классификатор серьезности, генератор PIR |
| **технология отслеживания долгов** | Сканер долговой базы кода, определение приоритетов, дашборд тенденций |
| **интервью-системный дизайнер** | Разработчик цикла интервью, банк вопросов, калибратор |

---

## 🔒 Скилл аудитора безопасности { #-skill-security-auditor }

Новое в версии 2.0.0 — аудит любого скилла на предмет угроз безопасности перед установкой:

```bash
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
```

Проверяет наличие: внедрения команд, выполнения кода, эксфильтрации данных, внедрения промптов, рисков цепочки поставок зависимостей, эскалации привилегий. Возвращает **PASS / WARN / FAIL** с инструкциями по исправлению.

**Нулевые зависимости.** Работает везде, где запущен Python.

---

## Недавно улучшенные скиллы { #recently-enhanced-skills }

Улучшено качество производства, добавленное для:

- `engineering/git-worktree-manager` — жизненный цикл рабочего дерева + сценарии автоматизации очистки
- `engineering/mcp-server-builder` — OpenAPI -> Каркас MCP + средство проверки манифеста
- `engineering/changelog-generator` — генератор заметок о выпуске + обычный линтер фиксации
- `engineering/ci-cd-pipeline-builder` — детектор стека + генератор пайплайна
- `marketing-skill/prompt-engineer-toolkit` — промпт A/B тестер + промпт версии/менеджер различий

Каждый из них теперь поставляется с `scripts/`, извлеченный `references/`, и ориентированный на использование `README.md`.

---

## Примеры использования { #usage-examples }

### Ревью архитектуры { #architecture-review }
```
Using the senior-architect skill, review our microservices architecture
and identify the top 3 scalability risks.
```

### Создание контента { #content-creation }
```
Using the content-creator skill, write a blog post about AI-augmented
development. Optimize for SEO targeting "Claude Code tutorial".
```

### Аудит соответствия требованиям { #compliance-audit }
```
Using the mdr-745-specialist skill, review our technical documentation
for MDR Annex II compliance gaps.
```

---

## Инструменты анализа Python { #python-analysis-tools }

580 инструментов CLI поставляются вместе с скиллами (все проверены, только для stdlib):

```bash
# SaaS health check
python3 finance/saas-metrics-coach/scripts/metrics_calculator.py --mrr 80000 --customers 200 --churned 3 --json

# Brand voice analysis
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py article.txt

# Tech debt scoring
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase

# RICE prioritization
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# Security audit
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/

# Landing page (TSX + Tailwind)
python3 product-team/landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx
```

---

## Связанные проекты { #related-projects }

| Проект | Описание |
|---------|-------------|
| [**Фабрика по скиллам и агентам Claude Code**](https://github.com/alirezarezvani/claude-code-skills-agents-factory) | Методология для формирования скиллы в масштабе |
| [**Клод Код Трезор**](https://github.com/alirezarezvani/claude-code-tresor) | Набор инструментов для повышения производительности с более чем 60 шаблонами промптов |
| [** Скиллы менеджера по продукту**](https://github.com/Digidai/product-manager-skills) | Старший PM—агент с 6 областями знаний, 12 шаблонами, более чем 30 фреймворками - поиск, стратегия, доставка, показатели SaaS, карьерный коучинг, разработка продуктов с использованием искусственного интеллекта |
| [**самый высокий рейтинг**](https://github.com/nowork-studio/toprank) | 9 Скилл по SEO и Google Ads для Claude Code — подключает Google Search Console, PageSpeed Insights и Google Ads API; отправляет мета-теги, разметку схемы и исправления ставок по ключевым словам в source или CMS. Массачусетский технологический институт, 107 звезд |

---

## Часто задаваемые вопросы { #faq }

**Как мне установить плагины Claude Code?**
Добавьте маркетплейс с `/plugin marketplace add imgusev/claude-skills-ru`, затем установите любой пакет для скилла с `/plugin install <name>@claude-code-skills`.

**Работают ли эти скиллы с OpenAI Codex / Cursor / Windsurf / Aider / Mistral Vibe?**
Да. Скиллы изначально работают с 13 инструментами: Claude Code, OpenAI Codex, Gemini CLI, OpenClaw, Hermes агент, Mistral Vibe, Курсор, Помощник, Виндсерфинг, Kilo Code, OpenCode, Augment и Антигравитация. Агент Hermes и Mistral Vibe используют одно и то же agentskills.io SKILL.md стандартный запуск `python scripts/sync-hermes-skills.py` или `./scripts/vibe-install.sh` для установки. Для других инструментов запустите `./scripts/convert.sh --tool all` затем `./scripts/install.sh --tool <name>`. Смотри [Интеграция с несколькими инструментами](https://alirezarezvani.github.io/claude-skills/integrations/) для получения подробной информации.

** Приведет ли обновление к нарушению моей установки?**
Нет. Мы следуем семантическому управлению версиями и поддерживаем обратную совместимость в выпусках исправлений. Существующие аргументы скрипта, пути к исходным текстам плагина и SKILL.md структуры никогда не изменяются в версиях исправлений. Увидеть [СПИСОК ИЗМЕНЕНИЙ](CHANGELOG.md) для получения подробной информации о каждом выпуске.

**Свободны ли инструменты Python от зависимостей?**
Да. Все 593 инструмента Python CLI используют только стандартную библиотеку — установка pip не требуется. Каждый скрипт проверяется на запуск с помощью `--help`.

**Как мне создать свой собственный скилл Claude Code?**
Каждый скилл представляет собой папку с `SKILL.md` (передняя панель + инструкции), необязательно `scripts/`, `references/`, и `assets/`. Посмотрите на [Фабрика скиллы и агентов](https://github.com/alirezarezvani/claude-code-skills-agents-factory) для получения пошагового руководства.

---

## Способствующий { #contributing }

Мы приветствуем вклады! Видишь [CONTRIBUTING.md](CONTRIBUTING.md) для получения рекомендаций.

**Быстрые идеи:**
- Добавляйте новые скиллы в недостаточно обслуживаемых областях
- Улучшите существующие инструменты Python
- Добавить тестовое покрытие для скриптов
- Переводить скиллы для неанглоязычных рынков

---

## Создание сайта Docs (сопровождающие) { #building-the-docs-site-maintainers }

Этот форк добавляет двуязычный сайт документации (en /ru) поверх вышестоящего контента — `SKILL.ru.md` файлы находятся прямо рядом с каждым английским `SKILL.md`. Настройка и запуск:

```bash
# 1. Create the venv (uv, Python 3.12+) and install dependencies
uv venv
uv pip install -r requirements-docs.txt -r requirements-dev.txt

# 2. Regenerate docs/ pages from SKILL.md / agents / commands sources
.venv/bin/python scripts/generate-docs.py

# 3. Build (or serve) the bilingual site — mkdocs-static-i18n builds both
#    'en' (site/) and 'ru' (site/ru/) from the same mkdocs.yml
.venv/bin/mkdocs build      # or: .venv/bin/mkdocs serve
```

Сам пайплайн перевода (интеграция с Yandex Translate, проверка структурной целостности) является внутренним инструментом и не является частью этого опубликованного репозитория.

---

## Сопровождающие и атрибуция { #maintainers--attribution }

**Сопровождающий RU:** [Илья Гусев](https://imgusev.ru) — [imgusev.ru](https://imgusev.ru) · [@imgusev](https://t.me/imgusev) в Telegram · [github.com/imgusev](https://github.com/imgusev).

Это русский перевод/адаптация [алирезарезвани/Клод-скиллы](https://github.com/alirezarezvani/claude-skills), лицензия Массачусетского технологического института, © Алиреза Резвани. Видишь [ЛИЦЕНЗИЯ](LICENSE) и [ОБРАТИТЕ ВНИМАНИЕ](NOTICE) для полной атрибуции.

---

## Лицензия { #license }

Массачусетский технологический институт [ЛИЦЕНЗИЯ](LICENSE) для получения подробной информации. Смотрите также [ОБРАТИТЕ ВНИМАНИЕ](NOTICE) для указания авторства перевода на русский язык.

---

## Звездная история { #star-history }

[![Диаграмма звездной истории](https://api.star-history.com/svg?repos=alirezarezvani/claude-skills&type=Date)](https://star-history.com/#alirezarezvani/claude-skills&Date)

---

**Построенный [Алиреза Резвани](https://alirezarezvani.com)** · [Средний](https://alirezarezvani.medium.com) · [Твиттер](https://twitter.com/nginitycloud)
