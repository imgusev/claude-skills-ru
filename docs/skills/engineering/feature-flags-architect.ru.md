---
title: "Архитектор фич-флагов { #feature-flags-architect } — Агентский скилл для Codex и OpenClaw"
description: "Используйте при добавлении, удалении или аудите фич-флагов. Триггеры для 'добавить флаг', 'отправить за флагом', 'план раскатки', 'kill switch'. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Архитектор фич-флагов { #feature-flags-architect }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `feature-flags-architect`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/feature-flags-architect/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Сквозная дисциплина для фич-флагов: классифицируйте их, отправляйте, расширяйте и удаляйте. Большинство команд относятся к флагам как к ненужным `if`-заявления; этот скилл рассматривает их как контролируемый жизненный цикл с измеримым долгом.

## Когда использовать { #when-to-use }

- Добавляем новый флаг и нуждаемся в плане раскатки
- Аудит кодовой базы на наличие устаревших или потерянных флагов
- Выбор поставщика флагов (LaunchDarkly против GrowthBook, Statsig против Unleash, Flipt против build-your-own)
- Разработка пути отключения для рискованного запуска
- Погашение основного долга перед замораживанием выпуска
- Ревью о том, должна ли функция вообще поставляться за флагом

## Основной принцип: флаги - это жизненный цикл, а не объект `if` { #core-principle-flags-are-a-lifecycle-not-an-if }

```
request → design → ship → ramp → cleanup → archive
```

Флаги, которые пропускают очистку, становятся долгами: мертвые ветви, устаревшие значения по умолчанию, непроверенные пути к коду, неограниченный радиус поражения. Три сценария в этом скилле обеспечивают выполнение жизненного цикла.

## Быстрый старт { #quick-start }

```bash
# 1. Audit the repo for flag debt
python scripts/flag_debt_scanner.py --repo . --max-age-days 90

# 2. Plan a progressive rollout for a new flag
python scripts/rollout_planner.py --population 100000 --target-percent 100 --duration-days 14 --strategy ring

# 3. Verify every flag has a documented kill switch
python scripts/kill_switch_audit.py --repo . --flag-doc docs/feature-flags.md
```

## 4 типа флагов (таксономия) { #the-4-flag-types-taxonomy }

Разные типы флагов имеют разную продолжительность жизни и право собственности. Неправильная классификация приводит к возникновению долга.

| Тип | Цель | Типичный срок службы | Владелец | Триггер очистки |
|---|---|---|---|---|
| **Освобождение** | Скрыть незавершенные элементы в процессе производства | дни–недели | Англ. | достигнута 100%-ная раскатка |
| **Эксперимент** | Варианты теста A/B | недели | Продукт/Маркетинг | Тест завершен; выбран победитель |
| **Оперативный** | Автоматические выключатели, переключатели perf, kill Switch | месяцы–годы | Английский/SRE | Заменено автоматическим масштабированием/удалением функций |
| **Разрешение** | Права для каждого пользователя/учетной записи/плана | годы (постоянные) | Продукт | План/роль удалены |

В списке наблюдения для проверки долгов должны быть только флаги выпуска и эксперимента. Флаги работы и разрешения по своей конструкции являются долговечными. Видишь `references/flag_taxonomy.md` для дерева решений.

## 3 инструмента Python { #the-3-python-tools }

Все три доступны только для stdlib. Бегать с `--help`.

### `flag_debt_scanner.py` { #flag_debt_scannerpy }

Находит флаги старше, чем `--max-age-days` с низким уровнем использования, предлагая кандидатов для очистки.

```bash
python scripts/flag_debt_scanner.py --repo . --max-age-days 90 --format text
python scripts/flag_debt_scanner.py --repo . --max-age-days 60 --format json > debt.json
```

**Эвристика обнаружения:**
1. Прогулка `--repo` для ссылок на код, соответствующих общим шаблонам вызова флагов:
   - `flag("...")`, `isFlagEnabled("...")`, `featureFlag("...")`, `getFlag("...")`
   - `client.variation("...", ...)`, `unleash.isEnabled("...")`, `growthbook.feature("...")`
2. Для каждого уникального идентификатора флага найдите самую старую фиксацию, которая его ввела (`git log --diff-filter=A -S <name>`).
3. Помечать как ДОЛГ, если он введен > `--max-age-days` назад И использованный в ≤`--min-uses` места.

Выводит имя флага, возраст в днях, ссылки на файлы, предлагаемое действие. Режим JSON удобен для CI.

### `rollout_planner.py` { #rollout_plannerpy }

Формирует график поэтапного раскатки на основе численности населения, целевого процента, продолжительности и стратегии.

```bash
python scripts/rollout_planner.py --population 100000 --target-percent 100 --duration-days 14 --strategy ring
python scripts/rollout_planner.py --population 50000 --target-percent 25 --duration-days 7 --strategy linear
python scripts/rollout_planner.py --population 1000000 --target-percent 100 --duration-days 30 --strategy log
```

**Стратегии:**
- `ring`: 1% → 5% → 25% → 50% → 100%, равномерно распределенные. По умолчанию для рискованных запусков.
- `linear`: постоянная ставка в день. Значение по умолчанию для группы среднего риска.
- `log`: быстрое начало, медленный хвост. По умолчанию для уверенных запусков с низким уровнем риска.
- `cohort`: по названной когорте (внутренняя → бета-версия → бесплатная → платная → все).

Выводит таблицу Markdown с указанием даты, процента, ожидаемого количества пользователей, критериев отмены и шага проверки для каждого этапа.

### `kill_switch_audit.py` { #kill_switch_auditpy }

Сопоставьте обнаруженные в коде флаги с документацией, чтобы убедиться, что для каждого из них записан путь к kill switch.

```bash
python scripts/kill_switch_audit.py --repo . --flag-doc docs/feature-flags.md
python scripts/kill_switch_audit.py --repo . --flag-doc runbooks/flags.md --format json
```

**Что он проверяет:**
1. Каждый обнаруженный кодом флаг имеет запись в `--flag-doc`
2. В каждой записи указаны: владелец, тип, триггер отключения, дашборд мониторинга
3. Отчеты помечают отсутствующую документацию (ОШИБКА) или отсутствующие поля (ПРЕДУПРЕЖДЕНИЕ)

Используйте в качестве гейта перед слиянием перед отправкой любого нового флага.

## Выбор поставщика (5 + DIY) { #provider-chooser-5--diy }

| Поставщик | Лучше всего подходит для | Модель ценообразования | Риск блокировки | Вариант OSS |
|---|---|---|---|---|
| ** Запуск в темноте** | Предприятие, комплексный таргетинг, аудит/соответствие требованиям | За МАУ, дорого | Высокий | Нет |
| **Книга роста** | Среднерыночный, ориентированный на A/B тестирование, удобный для OSS | Per-MAU + OSS | Низкий | Да (самостоятельный хостинг) |
| **Статистика** | Команды по развитию/разработке продуктов, продвинутые эксперименты | Бесплатный уровень + per-MAU | Средний | Нет |
| ** Дайте волю** | OSS-first, автономный хостинг, удобный для разработчиков | OSS + Предприятие | Низкий | Да |
| ** Перевернуть** | Легкий, встроенный в k8s, простой в использовании | Только для OSS | Нет | Да |
| ** СДЕЛАЙ САМ** | <100 флагов, без таргетинга, полный контроль | Нет | Нет | Н/Д |

Правила принятия решений:
- <50 флагов + нет таргетинга → СДЕЛАЙ сам с помощью конфигурационного файла или переменных env
- Нужна аналитика + эксперименты → Статистика или книга роста
- Требуются журналы аудита соответствия требованиям/SOC2 → LaunchDarkly
- Требуется самостоятельный хостинг (постоянное хранение данных / с воздушным зазором) → Развернуть или перевернуть
- Видишь `references/provider_comparison.md` для детализации.

## Воркфлоу { #workflows }

### Воркфлоу 1: Отправляем новую функцию за флагом { #workflow-1-ship-a-new-feature-behind-a-flag }

```
1. Classify: which of the 4 flag types?
   → Release (most common for engineering work)
2. Run rollout_planner.py to design the ramp
3. Add flag entry to docs/feature-flags.md BEFORE writing code:
   - name, owner, type, kill-switch trigger, dashboard URL
4. Write the code with the flag
5. Run kill_switch_audit.py — must pass before merge
6. Deploy at 0%; verify kill switch works
7. Execute rollout schedule; abort if abort criteria met
8. At 100% for 7+ days: remove flag, delete dead branch, archive doc entry
```

### Воркфлоу 2: Ежеквартальная очистка флага { #workflow-2-quarterly-flag-cleanup }

```
1. Run flag_debt_scanner.py --repo . --max-age-days 90 > debt.md
2. For each flagged item:
   a. Confirm it reached 100% (or was killed)
   b. Find the issue/PR that introduced it; verify owner agrees to remove
   c. Delete dead branches; remove flag config
   d. Run kill_switch_audit.py — should now show one fewer flag
3. Update CHANGELOG: "Removed N stale flags"
```

### Воркфлоу 3: Выберите поставщика { #workflow-3-choose-a-provider }

```
1. Estimate flag count (current + 12-month projection)
2. Required features:
   - Targeting rules (user, account, geo, %)?
   - A/B testing + stats?
   - Audit log / SOC2?
   - Self-hosting / data residency?
3. Pricing budget (MAU * cost-per-MAU)
4. See provider_comparison.md decision tree
5. Build a 30-day proof-of-concept before signing
```

### Воркфлоу 4: Спроектируйте kill switch { #workflow-4-design-a-kill-switch }

```
1. Identify the failure modes:
   - Latency spike (which threshold?)
   - Error rate spike (which threshold?)
   - Business metric regression (which threshold?)
2. Wire each to an abort:
   - Manual: dashboard link + on-call playbook
   - Automated: alert threshold flips flag back to 0%
3. Test the kill switch in staging BEFORE production rollout
4. Document in flag-doc; pass kill_switch_audit.py
```

## Ссылки { #references }

- `references/flag_taxonomy.md` — 4 типа, дерево решений, право собственности, срок службы
- `references/provider_comparison.md` — Компромиссы LaunchDarkly / GrowthBook / Statsig / Unleash / Flipt / DIY
- `references/rollout_strategies.md` — кольцевой / линейный / логарифмический / когортный / гео, критерии прерывания, мониторинг
- `references/flag_lifecycle.md` — запрос → дизайн → корабль → рампа → очистка → архив

## Слэш-команда { #slash-command }

`/flag-cleanup` — Запустите полный воркфлоу очистки текущего репозитория: проверьте наличие долгов, сгенерируйте план удаления, аудит kill Switch.

## Шаблоны активов { #asset-templates }

- `assets/flag_request_template.md` — заполните форму для запросов на новые флаги (имя, владелец, тип, kill switch, план раскатки)

## Анти-паттерны { #anti-patterns }

- **Постоянный флаг с `if (FLAG_FOO)` 50 мест** — должен быть флаг разрешения с конфигурацией среды выполнения, а не флаг выпуска
- **Флаг без владельца** — когда первоначальный инженер уходит, никто его не убирает
- ** Документально не задокументирован kill switch ** — когда функция отключается, никто не знает, как ее отключить
- ** A/B тест, который длился 6 месяцев** — выберите победителя; бессрочный тест - это долг
- ** Флаги в качестве переключателей функций для косметических изменений ** — отправка через депло, а не флаг

## Поддающийся проверке успех { #verifiable-success }

Команда, использующая этот скилл, должна достичь:
- 100% новых флагов проходят `kill_switch_audit.py` во время слияния
- `flag_debt_scanner.py --max-age-days 90` возвращает ≤5 устаревших флагов по всему репозиторию
- У каждого флага есть задокументированный владелец, тип и kill switch
- Среднее время для отмены флага выпуска: <60 дней с момента 100%-ной раскатки
