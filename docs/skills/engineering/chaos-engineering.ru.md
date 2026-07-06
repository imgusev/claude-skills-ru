---
title: "Инженерия хаоса { #chaos-engineering } — Агентский скилл для Codex и OpenClaw"
description: "Используйте при планировании, запуске или изучении результатов экспериментов по разработке хаоса. Триггеры для 'эксперимента с хаосом', 'внедрения. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Инженерия хаоса { #chaos-engineering }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `chaos-engineering`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/chaos-engineering/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Проектируйте эксперименты, которые выявляют реальные слабые места в производственных системах, не приводя к перебоям в работе. Большинство попыток "инженерии хаоса" пропускают измерение в установившемся режиме, не определяют критериев прерывания и не имеют ограничения по радиусу взрыва. Этот скилл обеспечивает дисциплину, которая делает эксперименты с хаосом безопасными и полезными.

## Когда использовать { #when-to-use }

- Планирование эксперимента с хаосом (что нарушить, где, когда, как прервать)
- Расчет радиуса поражения перед проведением эксперимента
- Ревью существующего плана эксперимента по обеспечению безопасности
- Выбор инструмента chaos (Chaos Toolkit / Chaos Mesh / Лакмусовая бумажка / Gremlin / AWS FIS)
- Написание посмертного эксперимента с хаосом
- Выполнение упражнения в игровой день

## Когда не следует использовать { #when-not-to-use }

- Общее реагирование на инциденты (использование `incident-response`)
- Поиск угроз / красная команда (использовать `red-team`, `threat-detection`)
- Нагрузочное тестирование производительности (другая цель — хаос связан с режимами сбоев, а не с производительностью)
- Производственная отладка (хаос обнаруживает слабые места превентивно, а не постфактум)

## Основной принцип: хаос без критериев отмены - это сбой в работе { #core-principle-chaos-without-abort-criteria-is-an-outage }

4 принципа создания хаоса (Netflix, 2016):

1. ** Постройте гипотезу о стационарном поведении. ** Не "что ломается?" но "X сохраняется; будет ли он по-прежнему сохраняться при ошибке Y?"
2. ** Варьируйте события реального мира.** Ввод реалистичных сбоев: уничтожение узлов, замедление работы сетей, потеря кэша, ограничение зависимостей.
3. **Проводите эксперименты на производстве.** Промежуточный этап никогда не имеет одинаковых режимов сбоя. Начните с малого.
4. ** Автоматизируйте эксперименты для их непрерывного проведения. ** Одноразовый хаос - это пресс-релиз; непрерывный хаос - это инженерия.

Добавьте пятое: ** Заранее определите критерии прерывания.** Эксперимент с хаосом без критериев прерывания - это сбой под другим названием.

## Быстрый старт { #quick-start }

```bash
SKILL=engineering/chaos-engineering/skills/chaos-engineering

# 1. Design an experiment
python "$SKILL/scripts/experiment_designer.py" --target "checkout-svc" --hypothesis "p99 latency stays <500ms" --attack latency --duration-min 15

# 2. Calculate blast radius
python "$SKILL/scripts/blast_radius_calculator.py" --traffic-share 0.05 --user-pop 1000000 --duration-min 15

# 3. Generate postmortem after the experiment
python "$SKILL/scripts/experiment_postmortem.py" --plan experiment.json --result-log results.txt
```

## 3 инструмента Python { #the-3-python-tools }

Все только для stdlib. Бегать с `--help`.

### `experiment_designer.py` { #experiment_designerpy }

Генерирует структурированный план эксперимента на основе входных данных. Обеспечивает соблюдение требуемых разделов (гипотеза, показатель устойчивого состояния, радиус поражения, критерии прерывания, откат).

```bash
python scripts/experiment_designer.py \
  --target "checkout-svc" \
  --hypothesis "p99 latency stays <500ms when payment-svc is slow" \
  --attack latency \
  --magnitude "+200ms" \
  --duration-min 15 \
  --blast-radius "5% of US traffic" \
  --abort-if "p99 > 1000ms OR error_rate > baseline + 1pp"
```

Выводит план Markdown с указанием: гипотезы, стационарного состояния, атаки, величины, продолжительности, радиуса поражения, критериев прерывания, процедуры отката, дашбордов мониторинга и обучающего вопроса.

### `blast_radius_calculator.py` { #blast_radius_calculatorpy }

Вычисляет радиус поражения запланированного эксперимента. Учитывая долю трафика + количество пользователей + продолжительность, вычисляются ожидаемые затронутые пользователи, ожидаемый расход бюджета на ошибки и оценка риска.

```bash
python scripts/blast_radius_calculator.py \
  --traffic-share 0.05 \
  --user-pop 1000000 \
  --duration-min 15 \
  --baseline-availability 0.999 \
  --expected-impact-availability 0.95
```

Результаты:
- Ожидаемые затронутые пользователи
- Израсходованный бюджет ошибок (в минутах бюджета ошибок)
- Оценка риска: ЗЕЛЕНЫЙ / ЖЕЛТЫЙ / КРАСНЫЙ
- Рекомендация: ПРОДОЛЖИТЬ / СОКРАТИТЬ / ПРЕРВАТЬ

ЗЕЛЕНЫЙ = погрешность бюджета <1%; ЖЕЛТЫЙ = 1-10%; КРАСНЫЙ = >10%.

### `experiment_postmortem.py` { #experiment_postmortempy }

Создает структурированное вскрытие на основе плана эксперимента + результатов. Улавливает распространенные способы посмертной неудачи: не записывается обучение, не предпринимаются последующие действия, язык с обвинениями.

```bash
python scripts/experiment_postmortem.py --plan experiment.json --result-log results.txt
```

Выводит Markdown с: резюме, гипотеза (подтвердилась ли она/refuted?), что мы узнали, что нас удивило, последующие действия с владельцами и ссылка на следующий эксперимент.

## 7 типов атак (таксономия) { #the-7-attack-types-taxonomy }

Разные атаки выявляют разные слабые места. Видишь `references/attack_taxonomy.md` для получения полной информации.

| Атака | Что он проверяет | Оснастка |
|---|---|---|
| **Задержка** | Тайм-ауты, повторные попытки, автоматические выключатели | tc, Сетка хаоса `NetworkChaos` |
| **Ошибка** | Обработка ошибок, резервные пути | Сетка хаоса `HTTPChaos`, Токсипрокси |
| **Ресурс** (процессор, память, диск) | Обработка насыщенности, автоматическое масштабирование | Сетка хаоса `StressChaos`, подчеркивающий |
| **Сетевой раздел** | Разделение мозга, консенсус, отработка отказа | Сетка хаоса `NetworkChaos` перегородка |
| **Сбой зависимости** | Изящная деградация, запасной вариант | Устранение неисправности сервисной сетки |
| **Время** | Перекос часов, проблемы с NTP | libfaketime, хаотическая сетка `TimeChaos` |
| **Инфраструктура** (уничтожить экземпляр) | Автоматическое восстановление, отработка отказа | AWS FIS, Обезьяна хаоса |

Выберите атаку, которая соответствует гипотезе. "Что произойдет, если X будет работать медленно?" → задержка. "Что произойдет, если X потеряет сеть?" → раздел.

## Устройство для выбора оснастки { #tooling-chooser }

| Инструмент | Лучше всего подходит для | Ценообразование | Стопка |
|---|---|---|---|
| **Набор инструментов хаоса** | Легкие, не зависящие от языка эксперименты с JSON | OSS | Любой |
| **Сетка хаоса** | Kubernetes-нативный, расширенный CRDS, внутри кластера | OSS | Kubernetes |
| **Лакмусовая бумажка** | Kubernetes, интегрированная с Argo, большая библиотека | OSS + Предприятие | Kubernetes |
| ** Гремлин** | Корпоративный SaaS, мультиоблачный, аудит | Оплаченный | Любой |
| **AWS FIS** | AWS-нативный, интегрированный с IAM, EC2/ECS/EKS | Платный (AWS) | AWS |
| **Пользовательский** | Нишевые потребности, единое облако, низкий бюджет | Нет | Любой |

Правила принятия решений:
- стек только для k8s + OSS → Chaos Mesh или Litmus (у Litmus большая библиотека экспериментов)
- Мульти-облако + OSS → Набор инструментов Chaos
- AWS-тяжелые + простые потребности → AWS FIS
- Предприятие + аудит/compliance → Гремлин

Видишь `references/tooling_landscape.md` для поиска компромиссов.

## Воркфлоу { #workflows }

### Воркфлоу 1: Спроектируйте и запустите один эксперимент { #workflow-1-design-and-run-a-single-experiment }

```
1. State a hypothesis: "When [fault], steady-state metric X stays within Y."
2. Identify the steady-state metric — must be measurable BEFORE the experiment.
3. Run blast_radius_calculator.py — confirm GREEN before proceeding.
4. Run experiment_designer.py to produce the plan.
5. Get a peer review of the plan; confirm abort criteria are concrete.
6. Notify the on-call team in #incidents (or whatever channel).
7. Run the experiment with monitoring open.
8. If abort criteria are hit, abort immediately; record what happened.
9. Run experiment_postmortem.py to capture learnings.
10. File follow-up actions; link to next experiment.
```

### Воркфлоу 2: Упражнение игрового дня { #workflow-2-game-day-exercise }

```
1. Pick a scenario (e.g., "primary database fails over").
2. Identify all dependent services that should keep working.
3. Build a multi-experiment plan covering each layer.
4. Schedule with stakeholders; on-call coverage required.
5. Run with a facilitator who manages the scenario.
6. Capture observations in a shared doc as they happen.
7. Single combined postmortem covering all observations.
8. Track follow-up actions in a board with owners.
```

### Воркфлоу 3: Непрерывный хаос (игровые дни → ежедневно) { #workflow-3-continuous-chaos-game-days--daily }

```
1. Start: weekly Game Day in staging.
2. Move to: weekly Game Day in production with limited blast radius.
3. Mature to: continuous chaos via scheduled experiments (Litmus chaos schedule, Gremlin scenarios).
4. Wire to deployment: every prod deploy triggers a baseline chaos sweep.
5. Track: experiments per week, weaknesses discovered, MTTR trend.
```

## Композиция с другими скиллами { #composition-with-other-skills }

Этот скилл явно сочетается с двумя другими в этой библиотеке:

| Скилл | Композиция |
|---|---|
| `feature-flags-architect` | Определены Kill Switch, здесь есть триггеры прерывания |
| `kubernetes-operator` | Операторы являются обычными объектами хаоса (проверка согласованности при сбое) |
| `incident-response` | Эксперименты с хаосом, которые приводят к эскалации, становятся инцидентами |

## Анти-паттерны { #anti-patterns }

- ** Никакой гипотезы** — "Давайте все разрушим" - это саботаж, а не инженерия
- **Нет показателя устойчивого состояния ** — без базовой линии вы не можете определить, нарушился ли X
- ** Радиус поражения не ограничен** — полномасштабный эксперимент без ограничений = отключение
- **Нет критериев прерывания** — смотрите выше; это обязательно
- **Нет покрытия по вызову ** — хаос без мониторинга - это неконтролируемое производство
- ** Хаос только в промежуточной стадии ** — в промежуточной стадии никогда не бывает режимов сбоя prod
- **Хаос в dev** — бесполезен; у dev режимы сбоя отличаются от prod
- ** Одноразовый хаос** - единичный эксперимент — это пресс-релиз; обучение требует повторения
- ** Вскрытие с обвинениями** - фиксируйте причины, а не обвинения; в противном случае команды прекратят создавать хаос.

## Ссылки { #references }

- `references/chaos_principles.md` — 4 принципа, история, когда начинать
- `references/experiment_design.md` — структура гипотезы, показатели устойчивого состояния, критерии прерывания
- `references/attack_taxonomy.md` — 7 типов атак с примерами и инструментами
- `references/tooling_landscape.md` — Набор инструментов хаоса / Сетка / Лакмусовая бумажка / Гремлин / FIS / СДЕЛАЙ сам

## Слэш-команда { #slash-command }

`/chaos-experiment` — мастер интерактивного проектирования экспериментов, который запускает все 3 инструмента.

## Шаблоны активов { #asset-templates }

- `assets/experiment_template.md` — шаблон плана заполнения
- `assets/postmortem_template.md` — структурированный посмертный шаблон

## Поддающийся проверке успех { #verifiable-success }

Команда, использующая этот скилл, должна достичь:

- В 100% экспериментов с хаосом есть письменная гипотеза, критерии прерывания и расчет радиуса взрыва
- Радиус поражения для любого отдельного эксперимента никогда не превышает 10% от допустимой погрешности
- Среднее время между экспериментами с хаосом <14 дней (непрерывное, а не разовое)
- Каждый эксперимент приводит к выполнению ≥1 последующего действия, которое отправляется
- Эксперимент "Хаос без эскалации" не приводит к инциденту, влияющему на клиента, в течение следующих 90 дней
