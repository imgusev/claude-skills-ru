---
title: "Агент автоматического поиска { #autoresearch-agent } — Агентский скилл для Codex и OpenClaw"
description: "Автономный экспериментальный цикл, который оптимизирует любой файл по измеряемому показателю. Вдохновленный авторским исследованием Карпати. Агент. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Агент автоматического поиска { #autoresearch-agent }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `autoresearch-agent`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/autoresearch-agent/skills/autoresearch-agent/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> Ты спишь. Агент экспериментирует. Вы просыпаетесь с результатами.

Автономный экспериментальный цикл, вдохновленный [Авторское исследование Карпатии](https://github.com/karpathy/autoresearch). агент редактирует один файл, запускает фиксированную оценку, сохраняет улучшения, отбрасывает сбои и выполняет цикл до бесконечности.

Ни одной догадки — пятьдесят взвешенных попыток, сложение.

---

## Слэш-команды { #slash-commands }

| Команда | Что он делает |
|---------|-------------|
| `/ar:setup` | Проведите новый эксперимент в интерактивном режиме |
| `/ar:run` | Выполните одну итерацию эксперимента |
| `/ar:loop` | Запуск автономного цикла с настраиваемым интервалом (10 м, 1 час, ежедневно, еженедельно, ежемесячно) |
| `/ar:status` | Показать дашборд и результаты |
| `/ar:resume` | Возобновите приостановленный эксперимент |

---

## Когда активируется этот Скилл { #when-this-skill-activates }

Распознать эти шаблоны у пользователя:

- "Сделай это быстрее / меньше / лучше"
- "Оптимизировать [файл] для [метрика]"
- "Улучшить мой [заголовки / копия / промпты]"
- "Проводите эксперименты в одночасье"
- "Я хочу получить [метрика] от X до Y"
- Любой запрос, включающий: оптимизацию, бенчмарк, улучшение, цикл экспериментов, автоматический поиск

Если пользователь описывает целевой файл + способ измерения успеха → применяется этот скилл.

---

## Настройка { #setup }

### Первый раз — Проведите эксперимент { #first-time--create-the-experiment }

Запустите сценарий установки. Пользователь сам решает, где проводить эксперименты:

** Уровень проекта ** (внутри репозитория, отслеживается git, доступен для совместного использования с командой):
```bash
python scripts/setup_experiment.py \
  --domain engineering \
  --name api-speed \
  --target src/api/search.py \
  --eval "pytest bench.py --tb=no -q" \
  --metric p50_ms \
  --direction lower \
  --scope project
```

**Пользовательский уровень** (персональный, в `~/.autoresearch/`):
```bash
python scripts/setup_experiment.py \
  --domain marketing \
  --name medium-ctr \
  --target content/titles.md \
  --eval "python evaluate.py" \
  --metric ctr_score \
  --direction higher \
  --evaluator llm_judge_content \
  --scope user
```

Тот `--scope` флаг определяет, где `.autoresearch/` жизни:
- `project` (по умолчанию) → `.autoresearch/` в корне репозитория. Определения экспериментов отслеживаются с помощью git. Результаты игнорируются.
- `user` → `~/.autoresearch/` в домашнем каталоге. Все является личным.

### Какая установка создает { #what-setup-creates }

```
.autoresearch/
├── config.yaml                        ← Global settings
├── .gitignore                         ← Ignores results.tsv, *.log
└── {domain}/{experiment-name}/
    ├── program.md                     ← Objectives, constraints, strategy
    ├── config.cfg                     ← Target, eval cmd, metric, direction
    ├── results.tsv                    ← Experiment log (gitignored)
    └── evaluate.py                    ← Evaluation script (if --evaluator used)
```

**столбцы results.tsv:** `commit | metric | status | description`
- `commit` — короткий git-хэш
- `metric` — плавающее значение или "N/A" для сбоев
- `status` — продолжай | отбросить | крушение
- `description` — что изменилось или почему он разбился

### Домены { #domains }

| Домен | Варианты использования |
|--------|-----------|
| `engineering` | Скорость кода, память, размер пакета, частота прохождения теста, время сборки |
| `marketing` | Заголовки, копирование в социальных сетях, темы электронных писем, копирование рекламы, вовлечение |
| `content` | Структура статьи, SEO-описания, читаемость, CTR |
| `prompts` | Системные промпты, звуковой сигнал чат-бота, инструкции агента |
| `custom` | Что-нибудь еще с поддающейся измерению метрикой |

### Если `program.md` Уже существует { #if-programmd-already-exists }

Пользователь, возможно, написал свой собственный `program.md`. Если вы нашли его в каталоге экспериментов, прочтите его. Это переопределяет шаблон. Просите только о том, чего не хватает.

---

## Протокол агента { #agent-protocol }

Вы - цикл. Скрипты выполняют настройку и оценку — вы выполняете творческую работу.

### Перед началом работы { #before-starting }
1. Читать `.autoresearch/{domain}/{name}/config.cfg` чтобы получить:
   - `target` — файл, который вы редактируете
   - `evaluate_cmd` — команда, которая измеряет ваши изменения
   - `metric` — название метрики для поиска в выходных данных eval
   - `metric_direction` — лучше "ниже" или "выше"
   - `time_budget_minutes` — максимальное время на оценку
2. Читать `program.md` о стратегии, ограничениях и о том, что вы можете/cannot изменение
3. Читать `results.tsv` для истории экспериментов (столбцы: фиксация, метрика, статус, описание)
4. Проверьте ветку эксперимента: `git checkout autoresearch/{domain}/{name}`

### Каждая итерация { #each-iteration }
1. Результаты ревью.tsv — что сработало? Что потерпело неудачу? Что еще не было испробовано?
2. Решите внести ОДНО изменение в целевой файл. Одна переменная для каждого эксперимента.
3. Отредактируйте целевой файл
4. Совершить: `git add {target} && git commit -m "experiment: {description}"`
5. Оценивать: `python scripts/run_experiment.py --experiment {domain}/{name} --single`
6. Считайте выходные данные — они печатают "СОХРАНИТЬ", "ОТБРОСИТЬ" или "АВАРИЙНЫЙ сбой" со значением метрики
7. Перейдите к шагу 1

### Что обрабатывает скрипт (вы этого не делаете) { #what-the-script-handles-you-dont }
- Запуск команды eval с тайм-аутом
- Анализ метрики из выходных данных eval
- По сравнению с предыдущими лучшими
- Отмена фиксации при сбое (`git reset --hard HEAD~1`)
- Запись результата в results.tsv

### Начинаем эксперимент { #starting-an-experiment }

```bash
# Single iteration (the agent calls this repeatedly)
python scripts/run_experiment.py --experiment engineering/api-speed --single

# Dry run (test setup before starting)
python scripts/run_experiment.py --experiment engineering/api-speed --dry-run
```

### Стратегия эскалации { #strategy-escalation }
- Прогоны 1-5: Низко висящие фрукты (очевидные улучшения, простая оптимизация)
- Этапы 6-15: Систематическое исследование (изменяйте по одному параметру за раз)
- Прогоны 16-30: Структурные изменения (замена алгоритмов, сдвиги архитектуры)
- Пробеги 30+: Радикальные эксперименты (совершенно разные подходы)
- Если никаких улучшений в 20+ запусках не происходит: обновите program.md Стратегический раздел

### Самосовершенствование { #self-improvement }
После каждых 10 экспериментов ревью results.tsv на предмет закономерностей. Обновите раздел
стратегии в program.md с тем, что вы узнали (например, "изменения в кэшировании
постоянно улучшаются на 5-10%", "попытки рефакторинга никогда не улучшают показатель").
Будущие итерации извлекут выгоду из этих накопленных знаний.

### Остановка { #stopping }
- Выполняется до тех пор, пока пользователь не прервет его, не будет достигнут предел контекста или не будет достигнута цель в program.md выполняется
- Перед остановкой: убедитесь в актуальности результатов.tsv
- При ограничении контекста: следующая сессия может возобновиться — results.tsv и git log сохраняются

### Правила { #rules }

- ** Одно изменение за эксперимент.** Не меняйте 5 вещей сразу. Вы не узнаете, что сработало.
- **Критерий простоты.** Небольшое улучшение, которое добавляет уродливую сложность, того не стоит. Равная производительность при более простом коде - это выигрыш. Удаление кода, который дает те же результаты, является наилучшим результатом.
- **Никогда не изменяйте программу оценки.** `evaluate.py` это основная истина. Изменение этого параметра делает недействительными все сравнения. Трудно остановиться, если вы поймаете себя на этом.
- **Тайм-аут.** Если запуск превышает временной бюджет в 2,5 раза, остановите его и обработайте как сбой.
- ** Обработка аварийных ситуаций.** Если это опечатка или отсутствует импорт, исправьте и запустите повторно. Если идея в корне нарушена, вернитесь назад, зарегистрируйте "сбой", двигайтесь дальше. 5 последовательных сбоев → пауза и оповещение.
- **Никаких новых зависимостей.** Используйте только то, что уже доступно в проекте.

---

## Оценщики { #evaluators }

Готовые к использованию оценочные скрипты. Скопировано в каталог эксперимента во время настройки с помощью `--evaluator`.

### Бесплатные оценщики (без затрат на API) { #free-evaluators-no-api-cost }

| Оценщик | Метрика | Вариант использования |
|-----------|--------|----------|
| `benchmark_speed` | `p50_ms` (ниже) | Время выполнения функции/API |
| `benchmark_size` | `size_bytes` (ниже) | Размер файла, пакета, изображения Docker |
| `test_pass_rate` | `pass_rate` (выше) | Процент прохождения набора тестов |
| `build_speed` | `build_seconds` (ниже) | Строить/compile/Время сборки Docker |
| `memory_usage` | `peak_mb` (ниже) | Максимальный объем памяти во время выполнения |

### Оценщики LLM Judge (использует вашу подписку) { #llm-judge-evaluators-uses-your-subscription }

| Оценщик | Метрика | Вариант использования |
|-----------|--------|----------|
| `llm_judge_content` | `ctr_score` 0-10 (выше) | Заголовки, заглавия, описания |
| `llm_judge_prompt` | `quality_score` 0-100 (выше) | Системные промпты, инструкции агента |
| `llm_judge_copy` | `engagement_score` 0-10 (выше) | Посты в социальных сетях, копия рекламы, электронные письма |

Судьи LLM вызывают инструмент CLI, который уже запущен пользователем (Claude, Codex, Gemini). Оценочная промпта заблокирована внутри `evaluate.py` — агент не может его изменить. Это не позволяет агенту использовать свой собственный оценщик.

Существующая подписка пользователя покрывает стоимость:
- Максимальный код Claude → неограниченное количество вызовов Claude для оценки
- Codex CLI (ChatGPT Pro) → неограниченное количество вызовов Codex
- Gemini CLI (бесплатный уровень) → бесплатные ознакомительные звонки

### Пользовательские оценщики { #custom-evaluators }

Если встроенный оценщик не подходит, пользователь пишет свой собственный `evaluate.py`. Единственное требование: он должен печатать `metric_name: value` к стандартному выходу.

```python
#!/usr/bin/env python3
# My custom evaluator — DO NOT MODIFY after experiment starts
import subprocess
result = subprocess.run(["my-benchmark", "--json"], capture_output=True, text=True)
# Parse and output
print(f"my_metric: {parse_score(result.stdout)}")
```

---

## Просмотр результатов { #viewing-results }

```bash
# Single experiment
python scripts/log_results.py --experiment engineering/api-speed

# All experiments in a domain
python scripts/log_results.py --domain engineering

# Cross-experiment dashboard
python scripts/log_results.py --dashboard

# Export formats
python scripts/log_results.py --experiment engineering/api-speed --format csv --output results.csv
python scripts/log_results.py --experiment engineering/api-speed --format markdown --output results.md
python scripts/log_results.py --dashboard --format markdown --output dashboard.md
```

### Вывод на Дашборд { #dashboard-output }

```
DOMAIN          EXPERIMENT          RUNS  KEPT  BEST         Δ FROM START  STATUS
engineering     api-speed            47    14   185ms        -76.9%        active
engineering     bundle-size          23     8   412KB        -58.3%        paused
marketing       medium-ctr           31    11   8.4/10       +68.0%        active
prompts         support-tone         15     6   82/100       +46.4%        done
```

### Форматы экспорта { #export-formats }

- **TSV** — по умолчанию, разделенный табуляцией (совместим с электронными таблицами)
- **CSV** — через запятую, с правильными кавычками
- **Markdown** — отформатированная таблица, читаемая в GitHub/docs

---

## Проактивные триггеры { #proactive-triggers }

Отмечайте их, не спрашивая:

- **Ни одна команда оценки не работает** → Протестируйте ее перед запуском цикла. Запустите один раз, проверьте выходные данные.
- **Целевой файл отсутствует в git** → `git init && git add . && git commit -m 'initial'` первый.
- ** Направление метрики неясно ** → Спросите: ниже или выше лучше? Необходимо знать, прежде чем начинать.
- **Слишком короткий временной бюджет ** → Если вычисление занимает больше времени, чем предусмотрено бюджетом, каждый запуск завершается сбоем.
- **агент, изменяющий evaluate.py ** → Жесткая остановка. Это делает недействительными все сравнения.
- **5 сбоев подряд** → Приостановите цикл. Предупредите пользователя. Не продолжайте циклы сжигания.
- **Никаких улучшений за более чем 20 запусков ** → Предлагаю изменить стратегию в program.md или попробовать другой подход.

---

## Установка { #installation }

### Однострочник (любой инструмент) { #one-liner-any-tool }
```bash
git clone https://github.com/imgusev/claude-skills-ru.git
cp -r claude-skills-ru/engineering/autoresearch-agent ~/.claude/skills/
```

### Установка с несколькими инструментами { #multi-tool-install }
```bash
./scripts/convert.sh --skill autoresearch-agent --tool codex|gemini|cursor|windsurf|openclaw
```

### Открытый коготь { #openclaw }
```bash
clawhub install cs-autoresearch-agent
```

---

## Связанные скиллы { #related-skills }

- **самосовершенствующийся-агент** - улучшает собственную память агента/rules со временем. НЕ для структурированных циклов экспериментов.
- **старший инженер ml** — архитектурные решения ML. Дополняющий — используется для первоначального проектирования, затем выполняется автоматический поиск для оптимизации.
- **tdd-руководство** — разработка на основе тестирования. Дополнительные тесты могут быть функцией оценки.
- **скилл-безопасность-аудитор** — аудит скилла перед публикацией. НЕ для циклов оптимизации.
