---
title: "Старший полный состав { #senior-fullstack } — Агентский скилл и плагин Codex"
description: "Набор инструментов для разработки Fullstack с проектными рамками для Next.js , стеки FastAPI, MERN и Django, анализ качества кода с оценкой. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Старший полный состав { #senior-fullstack }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `senior-fullstack`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/senior-fullstack/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Скиллы разработки Fullstack с использованием проектных лесов и инструментов анализа качества кода.

---

## Оглавление { #table-of-contents }

- [Фразы-триггеры](#trigger-phrases)
- [Инструменты](#tools)
- [Воркфлоу](#workflows)
- [Справочные руководства](#reference-guides)

---

## Фразы-триггеры { #trigger-phrases }

Используйте этот скилл, когда услышите:
- "создайте новый проект"
- "создайте Next.js приложение"
- "настройка FastAPI с помощью React"
- "анализ качества кода"
- "проверьте наличие проблем с безопасностью в кодовой базе"
- "какой стек я должен использовать"
- "настройка проекта fullstack"
- "сгенерировать шаблон проекта"

---

## Инструменты { #tools }

### Механизм принятия решений { #decision-engine }

Детерминированный выбор профиля. Учитывая четыре допущения (размер команды, частоту кадров, ориентацию на пользователя, бюджет) плюс дополнительные данные о трафике / чувствительности, ранжирует четыре встроенных профиля и возвращает соответствующий профиль с указанием уровня SLO и именованной цепочки утверждающих. Отказывается рекомендовать профиль без четырех необходимых входных данных.

**Использование:**

```bash
# See all options
python scripts/fullstack_decision_engine.py --help

# Run against a sample input
python scripts/fullstack_decision_engine.py --sample

# Pick a profile from real inputs
python scripts/fullstack_decision_engine.py \
    --team-size-12mo 8 --cadence daily --user-facing true --budget 5000 \
    --traffic-p99-rps 50 --data-sensitivity pii-only

# JSON output for downstream tools
python scripts/fullstack_decision_engine.py --sample --output json
```

Возвращает: совпадающее имя профиля, оценку, совпадающие/нарушенные ограничения, рекомендации по стеку, анти-рекомендации, уровень SLO, цепочку именованных утверждающих и ссылки на канон.

Движок кодирует ту же матрицу, по которой проходит диалоговая панель — используйте ее напрямую, когда входные данные уже известны, или через `cs-fullstack-engineer` агент для гриля "вопрос за вопросом".

---

### Строительные леса проекта { #project-scaffolder }

Генерирует структуры проекта fullstack с использованием шаблонного кода.

**Поддерживаемые шаблоны:**
- `nextjs` - Next.js 14+ с App Router, TypeScript, Tailwind CSS
- `fastapi-react` - Серверная часть FastAPI + интерфейс React + PostgreSQL
- `mern` - MongoDB, Express, React, Node.js с помощью машинописного текста
- `django-react` - Фреймворк Django REST + интерфейс React

**Использование:**

```bash
# List available templates
python scripts/project_scaffolder.py --list-templates

# Create Next.js project
python scripts/project_scaffolder.py nextjs my-app

# Create FastAPI + React project
python scripts/project_scaffolder.py fastapi-react my-api

# Create MERN stack project
python scripts/project_scaffolder.py mern my-project

# Create Django + React project
python scripts/project_scaffolder.py django-react my-app

# Specify output directory
python scripts/project_scaffolder.py nextjs my-app --output ./projects

# JSON output
python scripts/project_scaffolder.py nextjs my-app --json
```

**Параметры:**

| Параметр | Описание |
|-----------|-------------|
| `template` | Имя шаблона (nextjs, fastapi-react, mern, django-react) |
| `project_name` | Имя для нового каталога проекта |
| `--output, -o` | Выходной каталог (по умолчанию: текущий каталог) |
| `--list-templates, -l` | Перечислите все доступные шаблоны |
| `--json` | Вывод в формате JSON |

**Выходные данные включают в себя:**
- Структура проекта со всеми необходимыми файлами
- Конфигурации пакетов (package.json, requirements.txt )
- Конфигурация TypeScript
- Настройка Docker и docker-compose
- Шаблоны файлов среды
- Следующие шаги по запуску проекта

---

### Анализатор качества кода { #code-quality-analyzer }

Анализирует базы кода fullstack на предмет проблем с качеством.

**Категории анализа:**
- Уязвимости в системе безопасности (жестко закодированные секреты, риски внедрения)
- Показатели сложности кода (цикломатическая сложность, глубина вложенности)
- Исправность зависимостей (устаревшие пакеты, известные CVE)
- Оценка тестового покрытия
- Качество документации

**Использование:**

```bash
# Analyze current directory
python scripts/code_quality_analyzer.py .

# Analyze specific project
python scripts/code_quality_analyzer.py /path/to/project

# Verbose output with detailed findings
python scripts/code_quality_analyzer.py . --verbose

# JSON output
python scripts/code_quality_analyzer.py . --json

# Save report to file
python scripts/code_quality_analyzer.py . --output report.json
```

**Параметры:**

| Параметр | Описание |
|-----------|-------------|
| `project_path` | Путь к каталогу проекта (по умолчанию: текущий каталог) |
| `--verbose, -v` | Покажите подробные результаты |
| `--json` | Вывод в формате JSON |
| `--output, -o` | Написать отчет в файл |

**Выходные данные включают в себя:**
- Общий балл (0-100) с буквенной оценкой
- Проблемы безопасности по степени серьезности (критические, высокие, средние, низкие)
- Файлы высокой сложности
- Уязвимые зависимости со ссылками CVE
- Оценка тестового покрытия
- Полнота документации
- Приоритетные рекомендации

**Выборочный вывод:**

```
============================================================
CODE QUALITY ANALYSIS REPORT
============================================================

Overall Score: 75/100 (Grade: C)
Files Analyzed: 45
Total Lines: 12,500

--- SECURITY ---
  Critical: 1
  High: 2
  Medium: 5

--- COMPLEXITY ---
  Average Complexity: 8.5
  High Complexity Files: 3

--- RECOMMENDATIONS ---
1. [P0] SECURITY
   Issue: Potential hardcoded secret detected
   Action: Remove or secure sensitive data at line 42
```

---

## Воркфлоу { #workflows }

### Воркфлоу 1: Запуск нового проекта { #workflow-1-start-new-project }

1. Выберите подходящий стек на основе требований (см. Матрицу принятия решений о стеке)
2. Структура проекта строительных лесов
3. Проверка каркаса: подтвердите `package.json` (или `requirements.txt`) существует
4. Выполните первоначальную проверку качества — устраните все проблемы с P0, прежде чем продолжить
5. Настройка среды разработки

```bash
# 1. Scaffold project
python scripts/project_scaffolder.py nextjs my-saas-app

# 2. Verify scaffold succeeded
ls my-saas-app/package.json

# 3. Navigate and install
cd my-saas-app
npm install

# 4. Configure environment
cp .env.example .env.local

# 5. Run quality check
python scripts/code_quality_analyzer.py .

# 6. Start development
npm run dev
```

### Воркфлоу 2: Аудит существующей кодовой базы { #workflow-2-audit-existing-codebase }

1. Запустите анализ качества кода
2. Ревью результаты проверки безопасности — немедленно устраните все проблемы с P0 (критические)
3. Повторно запустите анализатор, чтобы подтвердить, что проблемы с P0 устранены
4. Создавайте заявки на выпуски P1/P2

```bash
# 1. Full analysis
python scripts/code_quality_analyzer.py /path/to/project --verbose

# 2. Generate detailed report
python scripts/code_quality_analyzer.py /path/to/project --json --output audit.json

# 3. After fixing P0 issues, re-run to verify
python scripts/code_quality_analyzer.py /path/to/project --verbose
```

### Воркфлоу 3: Выбор стека { #workflow-3-stack-selection }

Используйте руководство по техническому стеку, чтобы оценить варианты:

1. **Требуется SEO?** → Next.js с SSR
2. **Серверная часть с большим количеством API?** → Отдельный FastAPI или NestJS
3. ** Функции в режиме реального времени?** → Добавить слой WebSocket
4. ** Командный опыт ** → Сопоставьте стек с командными скиллами

Видишь `references/tech_stack_guide.md` для детального сравнения.

---

## Справочные руководства { #reference-guides }

### Архитектурные паттерны (`references/architecture_patterns.md`) { #architecture-patterns-referencesarchitecture_patternsmd }

- Архитектура интерфейсных компонентов (атомарный дизайн, контейнерный/презентационный)
- Шаблоны бэкенда (чистая архитектура, шаблон репозитория)
- Разработка API (соглашения REST, разработка схемы GraphQL)
- Шаблоны баз данных (объединение подключений, транзакции, реплики чтения)
- Стратегии кэширования (без кэширования, заголовки HTTP-кэша)
- Архитектура аутентификации (JWT + токены обновления, сеансы)

### Воркфлоу разработки (`references/development_workflows.md`) { #development-workflows-referencesdevelopment_workflowsmd }

- Настройка локальной разработки (Docker Compose, конфигурация среды)
- Воркфлоу Git (основанные на магистрали, обычные коммиты)
- Пайплайны CI/CD (примеры действий на GitHub)
- Стратегии тестирования (модуль, интеграция, E2E)
- Процесс ревью кода (шаблоны PR, чек-листы)
- Стратегии развертывания (сине-зеленые, канареечные, фич-флаги)
- Мониторинг и наблюдаемость (ведение журнала, метрики, проверки работоспособности)

### Руководство по техническому стеку (`references/tech_stack_guide.md`) { #tech-stack-guide-referencestech_stack_guidemd }

- Сравнение интерфейсных фреймворков (Next.js , React+Vite, Vue)
- Серверные фреймворки (Express, Fastify, NestJS, FastAPI, Django)
- Выбор базы данных (PostgreSQL, MongoDB, Redis)
- ORMs (Prisma, Drizzle, SQLAlchemy)
- Решения для аутентификации (Auth.js , Клерк, таможня JWT)
- Платформы развертывания (Vercel, Railway, AWS)
- Рекомендации по стеку в зависимости от варианта использования (MVP, SaaS, Enterprise)

---

## Краткий справочник { #quick-reference }

### Матрица принятия стековых решений { #stack-decision-matrix }

| Требование | Рекомендация |
|-------------|---------------|
| Сайт, критически важный для SEO | Next.js с SSR |
| Внутренняя дашборд | Реагировать + Завершать |
| API-первый серверный сервер | FastAPI или ускорять |
| Масштаб предприятия | NestJS + PostgreSQL |
| Быстрый прототип | Next.js Маршруты API |
| Данные, перегруженные документами | MongoDB |
| Сложные запросы | PostgreSQL |

### Общие проблемы { #common-issues }

| Проблема | Решение |
|-------|----------|
| N+1 запрос | Используйте DataLoader или ускоренную загрузку |
| Медленные сборки | Проверьте размер пакета, отложенную загрузку |
| Сложность аутентификации | Использование Auth.js или клерк |
| Ошибки типа | Включите строгий режим в tsconfig |
| Проблемы с CORS | Правильно настройте промежуточное программное обеспечение |

---

## Допущения и поддающиеся проверке критерии успеха (дисциплина Карпатии) { #assumptions-and-verifiable-success-criteria-karpathy-discipline }

Прежде чем этот скилл будет создавать, рекомендовать или модифицировать какой-либо код, необходимо выполнить следующие четыре допущения. Если какие-либо из них неизвестны, скилл останавливается и проходит по [Библиотека принудительных вопросов](#forcing-question-library-matt-pocock-grill) вместо этого.

1. ** Размер команды на сегодняшний день + численность персонала за 12 месяцев** — определяет архитектуру (монолитная / модульная / сервисная). Сэм Ньюман: "Сначала монолит".
2. **Целевой показатель частоты развертывания** — увеличивает затраты на CI/CD и инвестиции в флаги функций. * Ускорить* (Форсгрен и др., 2018).
3. ** Ориентированность на пользователя в сравнении с внутренним сайтом и маркетинговым сайтом-сайтом маркетинга** — определяет выбор стека и бюджет на 11 лет/перф.
4. ** Ежемесячный лимит бюджета на облако + SaaS ** — обеспечивает разделение между сборкой и управляемыми сервисами.

** Проверяемые критерии успеха ** (Карпатия #4) — каждая рекомендация, выдаваемая этим скиллам, должна содержать три числа, которые можно проверить с помощью машины.:

- Целевая задержка API (p50, p95, p99 в мс)
- Цель для улучшения интерфейса (LCP, INP, CLS на мобильных устройствах-4G)
- Целевой показатель времени безотказной работы / замедления

Если что—либо из этих трех не указано, рекомендация неполная - вернитесь к Q7 библиотеки принудительных вопросов.

Тот `scripts/fullstack_decision_engine.py` инструмент кодирует эти проверки: он отказывается рекомендовать профиль без всех четырех исходных данных и печатает поддающиеся проверке пороговые значения для соответствующего профиля.

---

## Профили настройки { #customization-profiles }

Четыре встроенных профиля в `profiles/` откалибруйте каждую рекомендацию:

| Профиль | Когда выбирать | Облачный потолок | Узор |
|---|---|---|---|
| `saas-startup` | < 10 англ., ориентированный на клиента, ежедневно + частота | $8 тыс./месяц | Модульный монолит на Next.js + Postgres |
| `enterprise-scale` | 50+ eng, регулируемый, per-PR с гейтами | $250 тыс./месяц | Сервисы, ограниченные доменом + команда платформы |
| `internal-tool` | ≤ 5 eng, с автоматической стенкой, < 100 DAU | 500 долларов в месяц | Сначала переустановите; уменьшите пользовательский стек, если принудительно |
| `marketing-site` | Зависимая от SEO, почти нулевая запись | 200 долларов в месяц | Статический-первый (Astro / 11ty / Следующий-статический) |

Выберите профиль с помощью:

```bash
python scripts/fullstack_decision_engine.py \
  --team-size 6 --team-size-12mo 12 \
  --cadence daily --user-facing true --budget 5000 \
  --traffic-p99-rps 45 --data-sensitivity pii-only
```

Инструмент возвращает наиболее подходящий профиль, соотношение с занявшим второе место (если оно находится в пределах 15%), рекомендацию по стеку, анти-шаблоны, которых следует избегать в этом профиле, и цепочку именованных утверждающих. **Этот инструмент никогда не одобряет автоматически.**

Чтобы добавить пользовательский профиль: скопируйте `profiles/saas-startup.json` к `profiles/<your-org>.json`, отрегулируйте `constraints` и `stack_recommendations` блокирует и запускает повторно. JSON — это поверхность настройки - никаких изменений в коде не требуется.

---

## Карта композиции { #composition-map }

Этот скилл не переопределяет область применения, которой владеют специалисты высокого уровня. Она разветвляется на них. Видишь `references/composition_map.md` для получения полной таблицы маршрутизации. Ключевые вилки:

| Беспокойство | Раскошелиться на |
|---|---|
| Ревью контракта API | `engineering/skills/api-design-reviewer/` |
| Проектирование схемы базы данных | `engineering/skills/database-designer/` |
| Надежность/ Конструкция SLO | `engineering/slo-architect/` |
| Пайплайн CI/CD | `engineering/skills/ci-cd-pipeline-builder/` |
| Профилирование производительности | `engineering/skills/performance-profiler/` |
| Ревью перед совершением Карпатии | `engineering/karpathy-coder/` |
| Предполетный архитектурный гриль | `engineering/grill-me/` |

Тот `cs-fullstack-engineer` агент (в `agents/engineering/cs-fullstack-engineer.md`) управляет этими разветвлениями с помощью `context: fork`. Вызовите его у другого агента с помощью `Agent({subagent_type: "cs-fullstack-engineer", prompt: "..."})` или с помощью слэш-команды `/cs:fullstack-review <your problem>`.

---

## Библиотека форсирующих вопросов (Мэтт Покок Грилл) { #forcing-question-library-matt-pocock-grill }

Прежде чем блокировать какое-либо решение по архитектуре или стеку, ответьте на семь форсирующих вопросов в `references/forcing_questions.md`. У каждого есть рекомендуемый ответ, цитата из канона и критерий уничтожения. Дисциплина:

1. По одному вопросу за ход. Никакого связывания.
2. Всегда рекомендуйте ответ с цитируемым каноном.
3. Отслеживайте ответы в рабочем файле (например,, `/tmp/fullstack-grill-<date>.md`).
4. Если сработает критерий уничтожения, остановитесь. Не возводите каркасы вокруг неразрешенного пробела.
5. После Q7 запустите `fullstack_decision_engine.py` с семью ответами в качестве входных данных.

Краткое изложение семи вопросов (полное содержание в справке):

1. Размер команды на сегодняшний день + численность персонала за 12 месяцев?
2. Частота развертывания для каждого PR, ежедневно, еженедельно, ежеквартально?
3. Ориентированный на клиента, внутренний инструмент или маркетинговый сайт?
4. Прогноз трафика p50 / p99 на один год?
5. Нанимать на работу в соответствии со стеком или обучать команду?
6. Год- одно ежемесячное облако + потолок SaaS?
7. Три поддающихся проверке критерия успеха с числовыми показателями?

---

## Обращение к другим агентам и скиллам { #invocation-from-other-agents-and-skills }

Этот скилл доступен любому другому агенту или скиллу с помощью трех поверхностей:

1. **Слэш-команда:** `/cs:fullstack-review <prompt>` — запускает полный гриль + механизм принятия решений + маршрутизация композиции.
2. **Агент-субагент:** `Agent({subagent_type: "cs-fullstack-engineer", prompt: "..."})` — разветвляет контекст, возвращает дайджест из ≤ 200 слов.
3. **Прямой вызов инструмента:** `python scripts/fullstack_decision_engine.py ...` — детерминированное сопоставление профилей без диалоговой решетки (используется, когда входные данные уже известны).

Видишь `agents/engineering/cs-fullstack-engineer.md` для полного контракта на вызов.
