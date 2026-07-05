🇬🇧 [English](README.md) · 🇷🇺 Русский

# Claude Code Skills & Plugins — агентские скиллы для любого кодинг-инструмента

**354 готовых к использованию скилла, плагина и агентских скилла Claude Code для 13 AI-инструментов разработки.**

Самая полная библиотека скиллов и плагинов агентов Claude Code с открытым исходным кодом — также работает с OpenAI Codex, Gemini CLI, Cursor и ещё 9 кодинг-агентами. Переиспользуемые пакеты экспертизы, покрывающие инженерию, DevOps, маркетинг (в т.ч. AEO — Answer Engine Optimization для цитирования LLM), безопасность (хуки PreToolUse), комплаенс, executive-консультирование (в т.ч. персоны founder-mode CFO/CMO/CRO/CPO/COO/CHRO/CISO/GC/CDO/CAIO/CCO/VPE + 21 слэш-команда `/cs:*`), продуктивность (capture/email/reflect), академический исследовательский стек (litreview/grants/dossier/patent/syllabus/pulse/notebooklm/deep-research + гибридный роутер) и корпоративные Research Operations (clinical-research/research-finance/market-research/product-research, v2.9.0).

**Работает с:** Claude Code · OpenAI Codex · Gemini CLI · OpenClaw · Hermes Agent[^hermes] · Mistral Vibe[^vibe] · Cursor · Aider · Windsurf · Kilo Code · OpenCode · Augment · Antigravity

[^hermes]: Hermes Agent — уровень **BYO-sync**: в репозитории уже лежит сгенерированное дерево `.hermes/skills/claude-skills/`, но чтобы установить его в `~/.hermes/skills/`, один раз локально запускаете `python scripts/sync-hermes-skills.py`. Использует тот же стандарт agentskills.io SKILL.md — без конвертации формата.
[^vibe]: Mistral Vibe тоже уровень **BYO-sync**: в репозитории уже лежит сгенерированное дерево `.vibe/skills/claude-skills/`, для установки в `~/.vibe/skills/` один раз локально запустите `./scripts/vibe-install.sh`. Тот же стандарт agentskills.io SKILL.md — без конвертации формата. Документация: <https://docs.mistral.ai/mistral-vibe/agents-skills>.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-354-brightgreen?style=for-the-badge)](#обзор-скиллов)
[![Agents](https://img.shields.io/badge/Agents-96-blue?style=for-the-badge)](#агенты)
[![Personas](https://img.shields.io/badge/Personas-7-purple?style=for-the-badge)](#персоны)
[![Commands](https://img.shields.io/badge/Commands-102-orange?style=for-the-badge)](#команды)
[![Stars](https://img.shields.io/github/stars/alirezarezvani/claude-skills?style=for-the-badge)](https://github.com/alirezarezvani/claude-skills/stargazers)
[![SkillCheck Validated](https://img.shields.io/badge/SkillCheck-Validated-4c1?style=for-the-badge)](https://getskillcheck.com)

> **5 200+ звёзд на GitHub** — самая полная библиотека скиллов и плагинов агентов Claude Code с открытым исходным кодом.

---

## Что такое скиллы и плагины Claude Code?

Скиллы Claude Code (также называемые агентскими скиллами или плагинами агентов кодинга) — это модульные пакеты инструкций, дающие AI-агентам разработки экспертизу в предметной области, которой у них нет «из коробки». Каждый скилл включает:

- **SKILL.md** — структурированные инструкции, воркфлоу и фреймворки принятия решений
- **Python-инструменты** — 593 CLI-скрипта (только stdlib, без установки пакетов)
- **Справочные материалы** — 711 шаблонов, чек-листов и файлов с доменными знаниями

**Один репозиторий, тринадцать платформ.** Работает нативно как плагины Claude Code, агентские скиллы Codex, скиллы Gemini CLI, скиллы Hermes Agent, скиллы Mistral Vibe, и конвертируется в другие инструменты через `scripts/convert.sh`. Все 593 Python-инструмента работают везде, где есть Python.

### Скиллы vs Агенты vs Персоны

| | Скиллы | Агенты | Персоны |
|---|---|---|---|
| **Назначение** | Как выполнить задачу | Какую задачу выполнить | Кто мыслит |
| **Область** | Один домен | Один домен | Кросс-доменно |
| **Голос** | Нейтральный | Профессиональный | С характером |
| **Пример** | «Следуй этим шагам для SEO» | «Проведи аудит безопасности» | «Мысли как CTO стартапа» |

Все три работают вместе. См. [Оркестрация](#оркестрация) — как их сочетать.

---

## Быстрая установка

### Gemini CLI (новое)

```bash
# Клонируем репозиторий
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Запускаем скрипт настройки
./scripts/gemini-install.sh

# Начинаем использовать скиллы
> activate_skill(name="senior-architect")
```

### Claude Code (рекомендуется)

```bash
# Добавляем маркетплейс
/plugin marketplace add alirezarezvani/claude-skills

# Устанавливаем по доменам
/plugin install engineering-skills@claude-code-skills          # 24 базовых инженерных
/plugin install engineering-advanced-skills@claude-code-skills  # 25 уровня POWERFUL
/plugin install product-skills@claude-code-skills               # 12 продуктовых
/plugin install marketing-skills@claude-code-skills             # 43 маркетинговых
/plugin install ra-qm-skills@claude-code-skills                 # 12 регуляторика/качество
/plugin install pm-skills@claude-code-skills                    # 6 управление проектами
/plugin install c-level-skills@claude-code-skills               # 28 executive-консультирование (весь C-suite)
/plugin install business-growth-skills@claude-code-skills       # 4 бизнес и рост
/plugin install finance-skills@claude-code-skills               # 2 финансы (аналитик + SaaS-метрики)

# Или устанавливаем отдельные скиллы
/plugin install skill-security-auditor@claude-code-skills       # Сканер безопасности
/plugin install playwright-pro@claude-code-skills                  # Набор инструментов Playwright
/plugin install self-improving-agent@claude-code-skills         # Автокурирование памяти
/plugin install content-creator@claude-code-skills              # Отдельный скилл
```

### OpenAI Codex

```bash
npx agent-skills-cli add alirezarezvani/claude-skills --agent codex
# Или: git clone + ./scripts/codex-install.sh
```

### OpenClaw

```bash
bash <(curl -s https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/scripts/openclaw-install.sh)
```

### Установка вручную

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
# Скопируйте любую папку скилла в ~/.claude/skills/ (Claude Code) или ~/.codex/skills/ (Codex)
```

---

## Поддержка нескольких инструментов (новое)

**Конвертируйте все 345 скиллов в 9 AI-инструментов разработки** одним скриптом:

| Инструмент | Формат | Установка |
|------|--------|---------|
| **Cursor** | правила `.mdc` | `./scripts/install.sh --tool cursor --target .` |
| **Aider** | `CONVENTIONS.md` | `./scripts/install.sh --tool aider --target .` |
| **Kilo Code** | `.kilocode/rules/` | `./scripts/install.sh --tool kilocode --target .` |
| **Windsurf** | `.windsurf/skills/` | `./scripts/install.sh --tool windsurf --target .` |
| **OpenCode** | `.opencode/skills/` | `./scripts/install.sh --tool opencode --target .` |
| **Augment** | `.augment/rules/` | `./scripts/install.sh --tool augment --target .` |
| **Antigravity** | `~/.gemini/antigravity/skills/` | `./scripts/install.sh --tool antigravity` |
| **Hermes Agent** | `~/.hermes/skills/` | `python scripts/sync-hermes-skills.py --verbose` |
| **Mistral Vibe** | `~/.vibe/skills/` | `./scripts/vibe-install.sh` |

**Как это работает:**

```bash
# 1. Конвертируем все скиллы во все инструменты (займёт ~15 секунд)
./scripts/convert.sh --tool all

# 2. Устанавливаем в свой проект (с подтверждением)
./scripts/install.sh --tool cursor --target /path/to/project

# Или используем --force, чтобы пропустить подтверждение:
./scripts/install.sh --tool aider --target . --force

# 3. Проверяем
find .cursor/rules -name "*.mdc" | wc -l  # Должно показать 346
```

**Каждый инструмент получает:**
- ✅ Все 345 скиллов, конвертированных в нативный формат
- ✅ README под каждый инструмент с шагами установки/проверки/обновления
- ✅ Поддержку скриптов, справочных материалов, шаблонов, где применимо
- ✅ Ноль ручной работы по конвертации

Запустите `./scripts/convert.sh --tool all`, чтобы сгенерировать выходные файлы под конкретные инструменты локально.

---

## Обзор скиллов

**354 скилла в 18 доменах:**

| Домен | Скиллов | Основное | Подробности |
|--------|--------|------------|---------|
| **🔧 Инженерия — базовый уровень** | 52 | Архитектура, фронтенд, бэкенд, фуллстек, QA, DevOps, SecOps, AI/ML, данные, Playwright Pro (генерация тестов, фикс нестабильных, миграции), self-improving agent (автокурирование памяти), пакет безопасности, аудит a11y, **named-persona-adversarial-review** (ревью через именованные инженерные философии) | [engineering-team/](engineering-team/) |
| **⚡ Инженерия — уровень POWERFUL** | 80 | Agent designer, RAG architect, database designer, CI/CD builder, security auditor, MCP builder, AgentHub, Helm-чарты, Terraform, self-eval, llm-wiki, tc-tracker, autoresearch-agent, **портфель надёжности** (feature-flags-architect, kubernetes-operator, chaos-engineering, slo-architect), ship-gate, PreToolUse-хук security-guidance, **скиллы Matt Pocock** (write-a-skill, caveman, grill-me, handoff, grill-with-docs), **zero-hallucination-coder** (Discuss→Map→Decompose→Execute→Verify) | [engineering/](engineering/) |
| **🎯 Продукт** | 17 | Product manager, agile PO, стратег, UX-исследователь, UI-дизайн, лендинги, SaaS-скаффолдер, аналитика, дизайнер экспериментов, дискавери, roadmap communicator, code-to-prd, apple-hig-expert | [product-team/](product-team/) |
| **📣 Маркетинг** | 48 | 8 подов: Content, SEO + AEO (`aeo` — E-E-A-T аудит, отслеживание цитирования в 5 LLM) + локальный (`local-seo-manager` — GBP/NAP/Map-Pack), CRO, Channels, Growth, Intelligence, Sales + фундамент контекста + роутер оркестрации | [marketing-skill/](marketing-skill/) |
| **🚀 Продуктивность** | 7 | `capture` (brain-dump-to-action), пара `email` (inbox-setup + inbox-triage), `reflect` (журнал), `handoff` (вдохновлён Matt Pocock), `andreessen` (режим market-first решений), `roast` (панель идей с 5 углов → GO/RESHAPE/KILL) | [productivity/](productivity/) |
| **🎨 Маркетинг (верхний уровень)** | 1 | `landing` — генератор одностраничных HTML-лендингов (4 стиля дизайна, паттерны GSAP, валидатор брендовой палитры) | [marketing/](marketing/) |
| **🔬 Исследования (академические)** | 9 | Оркестратор `research` (гибридный роутер + фолбэк) + 8 специалистов: `pulse`, `litreview`, `grants` (NIH), `dossier`, `patent`, `syllabus`, `notebooklm`, `deep-research` (rigor-first мета-исследования) | [research/](research/) |
| **🧪 Research Operations** ✨v2.9.0 | 5 | Корпоративные/кросс-функциональные исследования: оркестратор + `clinical-research` (дизайн исследований), `research-finance` (финансы R&D-программ), `market-research` (оценка рынка/опросы/сегментация), `product-research` (пользовательские исследования) — у каждого есть онбординг + кастомизация + опциональный мост к autoresearch | [research-ops/](research-ops/) |
| **📋 Управление проектами** | 9 | Senior PM, scrum master, Jira, Confluence, Atlassian admin, шаблоны + встроенный Atlassian Remote MCP | [project-management/](project-management/) |
| **🏥 Регуляторика и качество** | 19 | ISO 13485, MDR 2017/745, FDA, ISO 27001, GDPR, SOC 2, CAPA, управление рисками, agent-decision-receipts (PQ-подписанные квитанции действий) | [ra-qm-team/](ra-qm-team/) |
| **🛡️ Compliance OS** | 9 | Операционная система комплаенса — контроли, доказательства, воркфлоу готовности к аудиту | [compliance-os/](compliance-os/) |
| **💼 Executive-консультирование** | 68 | Весь C-suite (CEO/CTO/CFO/CMO/CRO/CPO/COO/CHRO/CISO/GC/CDO/CAIO/CCO/VPE) + агенты founder-mode + оркестрация + совет директоров + культура и сотрудничество | [c-level-advisor/](c-level-advisor/) |
| **📈 Бизнес и рост** | 5 | Customer success, sales engineer, revenue ops, контракты и предложения, инструментарий BizDev | [business-growth/](business-growth/) |
| **🏭 Бизнес-операции** | 7 | Оркестратор + process-mapper, vendor-management, capacity-planner, internal-comms, knowledge-ops, procurement-optimizer | [business-operations/](business-operations/) |
| **🤝 Коммерция** | 8 | Оркестратор + pricing-strategist, deal-desk, partnerships-architect, channel-economics, commercial-policy, rfp-responder, commercial-forecaster | [commercial/](commercial/) |
| **💰 Финансы** | 4 | Финансовый аналитик (DCF, бюджетирование, прогнозирование), SaaS metrics coach, консультант по бизнес-инвестициям | [finance/](finance/) |
| **🔄 Loop Library** | 1 | `loop-library` — находит, ищет, аудирует/чинит, адаптирует и проектирует ограниченные циклы AI-агентов; читает живой каталог с signals.forwardfuture.ai во время выполнения (вендорится дословно из [Forward-Future/loop-library](https://github.com/Forward-Future/loop-library)) | [loop-library/](loop-library/) |
| **📄 Markdown → HTML** | 5 | `markdown-html-orchestrator` (роутер по типу документа) + `design-system` (брендовые токены WCAG-AA) + `md-document` (лонгрид) + `md-review` (код-ревью в 2 колонки) + `md-slides` (слайд-дек одним файлом) — конвертер markdown в интерактивный HTML | [markdown-html/](markdown-html/) |

---

## Персоны

Готовые идентичности агентов с подобранным набором скиллов, воркфлоу и характерным стилем общения. Персоны — это больше, чем «используй эти скиллы»: они определяют, как агент мыслит, расставляет приоритеты и общается.

| Персона | Домен | Для чего лучше всего |
|---------|--------|----------|
| [**Startup CTO**](agents/personas/startup-cto.md) | Инженерия + стратегия | Архитектурные решения, выбор стека, найм команды, техническая due diligence |
| [**Growth Marketer**](agents/personas/growth-marketer.md) | Маркетинг + рост | Рост через контент, стратегия запуска, оптимизация каналов, бутстрап-маркетинг |
| [**Solo Founder**](agents/personas/solo-founder.md) | Кросс-домен | Стартапы одного человека, сайд-проекты, сборка MVP, все роли сразу |

**Использование:**
```bash
# Claude Code
cp agents/personas/startup-cto.md ~/.claude/agents/

# Любой инструмент
./scripts/convert.sh --tool cursor  # Конвертирует и персоны тоже
```

Подробности — в [agents/personas/](agents/personas/). Создайте свою по [TEMPLATE.md](agents/personas/TEMPLATE.md).

---

## Оркестрация

Лёгкий протокол координации персон, скиллов и агентов на работе, пересекающей границы доменов. Фреймворк не нужен.

**Четыре паттерна:**

| Паттерн | Что | Когда |
|---------|------|------|
| **Solo Sprint** | Смена персон по фазам проекта | Сайд-проекты, MVP, соло-фаундеры |
| **Domain Deep-Dive** | Одна персона + несколько стековых скиллов | Архитектурные ревью, комплаенс-аудиты |
| **Multi-Agent Handoff** | Персоны ревьюят результат друг друга | Решения с высокой ценой ошибки, готовность к запуску |
| **Skill Chain** | Последовательные скиллы без персоны | Контентные пайплайны, повторяемые чек-листы |

**Пример: запуск продукта за 6 недель**
```
Неделя 1-2: startup-cto + aws-solution-architect + senior-frontend → Строим
Неделя 3-4: growth-marketer + launch-strategy + copywriting + seo-audit → Готовим
Неделя 5-6: solo-founder + email-sequence + analytics-tracking → Запускаем и итерируем
```

Полный протокол и примеры — в [orchestration/ORCHESTRATION.md](orchestration/ORCHESTRATION.md).

---

## Уровень POWERFUL

25 продвинутых скиллов с глубокими, production-grade возможностями:

| Скилл | Что делает |
|-------|-------------|
| **agent-designer** | Оркестрация мультиагентов, схемы инструментов, оценка производительности |
| **agent-workflow-designer** | Паттерны sequential, parallel, router, orchestrator, evaluator |
| **rag-architect** | Сборщик RAG-пайплайна, оптимизатор чанкинга, оценщик ретрива |
| **database-designer** | Анализатор схемы, генерация ERD, оптимизатор индексов, генератор миграций |
| **database-schema-designer** | Требования → миграции, типы, seed-данные, политики RLS |
| **migration-architect** | Планировщик миграций, проверка совместимости, генератор отката |
| **skill-security-auditor** | 🔒 Гейт безопасности — сканирует скиллы на вредоносный код перед установкой |
| **ci-cd-pipeline-builder** | Анализ стека → генерация конфигов GitHub Actions / GitLab CI |
| **mcp-server-builder** | Сборка MCP-серверов из спецификаций OpenAPI |
| **pr-review-expert** | Анализ радиуса поражения, скан безопасности, дельта покрытия |
| **api-design-reviewer** | Линтер REST API, детектор breaking changes, скоркарта дизайна |
| **api-test-suite-builder** | Сканирует API-роуты → генерирует полные наборы тестов |
| **dependency-auditor** | Мультиязычный сканер, соответствие лицензий, планировщик апгрейдов |
| **observability-designer** | Дизайнер SLO, оптимизатор алертов, генератор дашбордов |
| **performance-profiler** | Профилирование Node/Python/Go, анализ бандла, нагрузочное тестирование |
| **monorepo-navigator** | Управление воркспейсами Turborepo/Nx/pnpm и анализ влияния |
| **changelog-generator** | Conventional commits → структурированные чейнджлоги |
| **codebase-onboarding** | Автогенерация онбординг-документации по анализу кодовой базы |
| **runbook-generator** | Кодовая база → операционные рансбуки с командами |
| **git-worktree-manager** | Параллельная разработка с изоляцией портов, синхронизацией env |
| **env-secrets-manager** | Управление .env, обнаружение утечек, воркфлоу ротации |
| **incident-commander** | Плейбук реагирования на инциденты, классификатор серьёзности, генератор PIR |
| **tech-debt-tracker** | Сканер техдолга кодовой базы, приоритизатор, дашборд трендов |
| **interview-system-designer** | Дизайнер интервью-цикла, банк вопросов, калибратор |

---

## 🔒 Skill Security Auditor

Новое в v2.0.0 — аудит любого скилла на риски безопасности перед установкой:

```bash
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
```

Сканирует: инъекции команд, выполнение кода, эксфильтрацию данных, prompt injection, риски supply chain зависимостей, эскалацию привилегий. Возвращает **PASS / WARN / FAIL** с рекомендациями по устранению.

**Ноль зависимостей.** Работает везде, где есть Python.

---

## Недавно улучшенные скиллы

Добавлены production-grade улучшения для:

- `engineering/git-worktree-manager` — скрипты жизненного цикла worktree + автоматизация очистки
- `engineering/mcp-server-builder` — скаффолд OpenAPI -> MCP + валидатор манифеста
- `engineering/changelog-generator` — генератор release notes + линтер conventional commit
- `engineering/ci-cd-pipeline-builder` — детектор стека + генератор пайплайна
- `marketing-skill/prompt-engineer-toolkit` — A/B-тестер промптов + менеджер версий/диффов промптов

Каждый теперь поставляется с `scripts/`, вынесенными `references/` и `README.md`, ориентированным на использование.

---

## Примеры использования

### Ревью архитектуры
```
Используя скилл senior-architect, проверь нашу микросервисную архитектуру
и определи топ-3 риска масштабируемости.
```

### Создание контента
```
Используя скилл content-creator, напиши статью в блог об AI-augmented
разработке. Оптимизируй под SEO с фокусом на "Claude Code tutorial".
```

### Аудит комплаенса
```
Используя скилл mdr-745-specialist, проверь нашу техническую документацию
на пробелы соответствия MDR Annex II.
```

---

## Python-инструменты анализа

580 CLI-инструментов поставляются вместе со скиллами (все проверены, только stdlib):

```bash
# Проверка здоровья SaaS
python3 finance/saas-metrics-coach/scripts/metrics_calculator.py --mrr 80000 --customers 200 --churned 3 --json

# Анализ голоса бренда
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py article.txt

# Оценка техдолга
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase

# Приоритизация RICE
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# Аудит безопасности
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/

# Лендинг (TSX + Tailwind)
python3 product-team/landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx
```

---

## Похожие проекты

| Проект | Описание |
|---------|-------------|
| [**Claude Code Skills & Agents Factory**](https://github.com/alirezarezvani/claude-code-skills-agents-factory) | Методология для создания скиллов в масштабе |
| [**Claude Code Tresor**](https://github.com/alirezarezvani/claude-code-tresor) | Набор инструментов продуктивности с 60+ шаблонами промптов |
| [**Product Manager Skills**](https://github.com/Digidai/product-manager-skills) | Senior PM-агент с 6 доменами знаний, 12 шаблонами, 30+ фреймворками — дискавери, стратегия, поставка, SaaS-метрики, карьерный коучинг, AI product craft |
| [**toprank**](https://github.com/nowork-studio/toprank) | 9 SEO- и Google Ads-скиллов для Claude Code — подключает Google Search Console, PageSpeed Insights и Google Ads API; отправляет фиксы мета-тегов, schema markup и ставок по ключевым словам в исходный код или CMS. MIT, 107 звёзд |

---

## FAQ

**Как установить плагины Claude Code?**
Добавьте маркетплейс командой `/plugin marketplace add alirezarezvani/claude-skills`, затем установите любой пакет скиллов через `/plugin install <name>@claude-code-skills`.

**Работают ли эти скиллы с OpenAI Codex / Cursor / Windsurf / Aider / Mistral Vibe?**
Да. Скиллы работают нативно с 13 инструментами: Claude Code, OpenAI Codex, Gemini CLI, OpenClaw, Hermes Agent, Mistral Vibe, Cursor, Aider, Windsurf, Kilo Code, OpenCode, Augment и Antigravity. Hermes Agent и Mistral Vibe оба используют тот же стандарт agentskills.io SKILL.md — запустите `python scripts/sync-hermes-skills.py` или `./scripts/vibe-install.sh` для установки. Для остальных инструментов запустите `./scripts/convert.sh --tool all`, затем `./scripts/install.sh --tool <name>`. Подробности — в [Multi-Tool Integrations](https://alirezarezvani.github.io/claude-skills/integrations/).

**Сломает ли обновление мою установку?**
Нет. Мы следуем семантическому версионированию и сохраняем обратную совместимость в рамках патч-релизов. Аргументы скриптов, пути источников плагинов и структуры SKILL.md никогда не меняются в патч-версиях. Подробности по каждому релизу — в [CHANGELOG](CHANGELOG.md).

**Python-инструменты свободны от зависимостей?**
Да. Все 593 Python CLI-инструмента используют только стандартную библиотеку — установка пакетов не требуется. Каждый скрипт проверен на запуск с `--help`.

**Как создать свой скилл Claude Code?**
Каждый скилл — это папка с `SKILL.md` (frontmatter + инструкции), опционально `scripts/`, `references/` и `assets/`. Пошаговое руководство — в [Skills & Agents Factory](https://github.com/alirezarezvani/claude-code-skills-agents-factory).

---

## Участие в разработке

Мы рады вкладу сообщества! Инструкции — в [CONTRIBUTING.md](CONTRIBUTING.md).

**Быстрые идеи:**
- Добавить новые скиллы в недообслуженных доменах
- Улучшить существующие Python-инструменты
- Добавить тестовое покрытие для скриптов
- Перевести скиллы для неанглоязычных рынков

---

## Сборка сайта документации и переводов (для мейнтейнеров)

Этот форк добавляет двуязычный (en/ru) сайт документации поверх оригинального контента. Установка и запуск:

```bash
# 1. Создаём venv (uv, Python 3.12+) и ставим зависимости
uv venv
uv pip install -r requirements-docs.txt -r requirements-dev.txt

# 2. Перегенерируем страницы docs/ из источников SKILL.md / agents / commands
.venv/bin/python scripts/generate-docs.py

# 3. Собираем (или запускаем локально) двуязычный сайт — mkdocs-static-i18n
#    собирает обе версии ('en' в site/, 'ru' в site/ru/) из одного mkdocs.yml
.venv/bin/mkdocs build      # или: .venv/bin/mkdocs serve

# 4. Переводим ещё контента на русский (пишет <stem>.ru.md рядом с
#    английским оригиналом — оригинал никогда не трогается). Нужны
#    YANDEX_TRANSLATE_API_KEY / YANDEX_FOLDER_ID (см. .env.example).
.venv/bin/python scripts/translate.py --domain markdown-html --dry-run
.venv/bin/python scripts/translate.py --domain markdown-html

# 5. Гейт качества — линтер, форматтер, тесты, структурная целостность
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -q
.venv/bin/python scripts/check_translation_integrity.py
.venv/bin/python scripts/check_dual_publish.py
```

Перед публикацией этого форка замените плейсхолдеры `<GH_USER>/<REPO>` в `mkdocs.yml`, `scripts/generate-docs.py` (`GITHUB_BASE`) и `docs/overrides/main.html` на реальные имя пользователя/организации и репозитория GitHub.

---

## Лицензия

MIT — подробности в [LICENSE](LICENSE).

---

## История звёзд

[![Star History Chart](https://api.star-history.com/svg?repos=alirezarezvani/claude-skills&type=Date)](https://star-history.com/#alirezarezvani/claude-skills&Date)

---

**Создано [Alireza Rezvani](https://alirezarezvani.com)** · [Medium](https://alirezarezvani.medium.com) · [Twitter](https://twitter.com/nginitycloud)

---

## Об этом переводе

Русский перевод контента claude-skills подготовлен независимо от оригинального автора. Оригинал распространяется по лицензии MIT, © 2025 Alireza Rezvani — см. [LICENSE](LICENSE), copyright не меняется. Исходный репозиторий: <https://github.com/alirezarezvani/claude-skills>.

Перевод недеструктивен: английские `SKILL.md`/`README.md` и все остальные оригинальные файлы остаются нетронутыми; русские версии лежат рядом с суффиксом `.ru.md` (например `SKILL.ru.md`). Сайт документации собирается двуязычным через `mkdocs-static-i18n` — переключатель языка в шапке сайта.

**Перед публикацией форка:** замените плейсхолдеры `<GH_USER>/<REPO>` в `mkdocs.yml`, `scripts/generate-docs.py` (`GITHUB_BASE`) и `docs/overrides/main.html` на реальные имя пользователя/организации и репозитория GitHub, под которыми размещён этот форк.
