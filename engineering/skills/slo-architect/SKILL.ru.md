---
name: slo-architect
description: Используйте при определении, ревью или управлении бюджетами SLO/SLIS/ошибок. Триггеры для "определения SLO", "каким должен быть наш SLO", "бюджет ошибок", "скорость записи", "SLI", "цель уровня обслуживания", "Google SRE workbook", "предупреждение о скорости записи в многооконном режиме" или любой другой вопрос, связанный с надежностью. Поставляется SLO designer, калькулятор бюджета ошибок с пороговыми значениями скорости загрузки в нескольких окнах и SLO reviewer, который выявляет распространенные ошибки (слишком агрессивная цель, слишком короткое окно, конфликтующие SLO, нет определения SLI). 4 ссылки на принципы SLO + дизайн SLI + математика бюджета ошибок + композиция с функциональными флагами-архитектор /хаос-инжиниринг /оператор kubernetes. ЭТО не общий скилл наблюдательности — в частности, дисциплина SLO.
context: fork
version: 2.9.0
author: claude-code-skills
license: MIT
tags: [slo, sli, sla, error-budget, burn-rate, sre, reliability, google-sre-workbook, observability]
compatible_tools: [claude-code, codex-cli, cursor, antigravity, opencode, gemini-cli]
---

# Архитектор SLO { #slo-architect }

Определите СЛО, которые что-то значат. Большинство "SLO" в дикой природе — это произвольные цифры, в которые никто не верит - 99,9% на каждой конечной точке, нет определения SLI, нет бюджета ошибок, нет политики для того, что происходит, когда бюджет сгорает. Этот скилл обеспечивает соблюдение дисциплины из рабочей книги Google по SRE: выберите правильный SLI, установите цель, которая действительно волнует пользователей, рассчитайте бюджет ошибок, подключите многооконные оповещения о частоте выгорания и разработайте письменную политику на случай, если бюджет закончится.

## Когда использовать { #when-to-use }

- Определение нового SLO для сервиса или функции
- Ревью существующих SLO на предмет распространенных ошибок
- Выбор правильного SLI (на основе событий, на основе временного окна или на основе запроса)
- Вычисление бюджетов ошибок и пороговых значений предупреждений о частоте выгорания
- Привязка SLO к существующим элементам управления — фичи-флаги прерывания, радиус поражения хаосом, уровни возможностей оператора

## Когда не следует использовать { #when-not-to-use }

- Общая стратегия наблюдаемости (метрики + журналы + трассировки) → использовать `observability-designer`
- Соглашения об уровне обслуживания, ориентированные на клиента, с юридическими оговорками → это составление контрактов, а не инжиниринг
- Нагрузочное тестирование производительности (производительность, а не надежность) → использование `performance-profiler`
- Активное реагирование на инцидент → использование `incident-response`

## Основной принцип: SLO - это обещание в отношении пользовательского опыта { #core-principle-an-slo-is-a-promise-about-user-experience }

```
SLI  ⟶  measurable signal of user-perceived health (e.g., HTTP 2xx rate)
SLO  ⟶  target for the SLI over a window (e.g., 99.9% over 30 days)
SLA  ⟶  customer-facing commitment with consequences (separate concern)
EB   ⟶  error budget: 100% − SLO target = how much "bad" you can spend
BR   ⟶  burn rate: how fast you're consuming the error budget
```

Четыре кардинальные ошибки:

1. ** Цель слишком высока ** (99,99%+ для сервисов, которые не могут ее поддерживать) — каждый незначительный сбой нарушает SLO; оповещения становятся шумом.
2. ** Неправильный SLI** (использование процессора в качестве прокси для пользовательского интерфейса) — система может быть "зеленой", в то время как пользователи страдают.
3. ** Бюджетная политика без ошибок ** — сокращение бюджета ничего не значит, если нет согласованных действий.
4. **Оповещение о скорости загрузки в одно окно ** - либо слишком шумное (страница с 5-минутным скачком), либо слишком медленное (уведомление об исчерпании бюджета постфактум).

Приведенные ниже 3 инструмента улавливают каждый из них.

## Быстрый старт { #quick-start }

```bash
SKILL=engineering/slo-architect/skills/slo-architect

# 1. Design an SLO
python "$SKILL/scripts/slo_designer.py" \
  --service checkout-svc \
  --sli-type request-success-rate \
  --target 99.9 \
  --window-days 30

# 2. Compute error budget + multi-window burn-rate alerts
python "$SKILL/scripts/error_budget_calculator.py" \
  --target 99.9 --window-days 30

# 3. Review existing SLO definitions for common bugs
python "$SKILL/scripts/slo_review.py" --slo-doc docs/slos/
```

## 3 инструмента Python { #the-3-python-tools }

Все только для stdlib.

### `slo_designer.py` { #slo_designerpy }

Генерирует структурированное определение SLO с обязательными полями. Отказывается отображать, если отсутствует какое-либо обязательное поле (`exit 1`).

```bash
python scripts/slo_designer.py \
  --service checkout-svc \
  --sli-type request-success-rate \
  --target 99.9 \
  --window-days 30 \
  --owner team-checkout
```

**Поддерживаемые типы SLI:**
- `request-success-rate` — `(total_requests - bad_requests) / total_requests`
- `request-latency` — `count(requests < threshold) / total_requests`
- `availability-time` — `(window - downtime) / window`
- `data-freshness` — `count(data_age < threshold) / total_data_points`
- `correctness` — `count(correct_outputs) / total_outputs`

По умолчанию выводится Markdown со всеми обязательными полями, заполненными или помеченными `<must define>`. Вывод в формате JSON (`--format json`) потребляется `slo_review.py`.

### `error_budget_calculator.py` { #error_budget_calculatorpy }

Учитывая целевую доступность + окно, вычисляет:
- Допустимое время простоя в окне
- Пороговые значения скорости записи в многооконном режиме для рабочей книги Google SRE (глава 5):
  - **Быстрое сжигание** — страница, на которую за 1 час израсходовано 2% месячного бюджета
  - **Медленное сгорание** — страница, если 10% израсходовано за 6 часов, билет, если 10% израсходовано за 3 дня
- Рекомендуемые правила оповещения (вывод в форме PromQL)

```bash
python scripts/error_budget_calculator.py --target 99.9 --window-days 30
python scripts/error_budget_calculator.py --target 99.95 --window-days 7 --format json
```

### `slo_review.py` { #slo_reviewpy }

Аудит каталога определений SLO (Markdown или JSON) на предмет распространенных ошибок.

```bash
python scripts/slo_review.py --slo-doc docs/slos/
```

**Проверки:**
- `target_too_high`: целевой показатель ≥ 99,99% (устойчивый только при значительных инвестициях в инженерное обеспечение)
- `target_too_low`: целевой показатель ≤ 99,0% (вероятно, неверный SLI; пользователи заметят)
- `window_too_short`: окно < 7 дней (преобладает статистический шум)
- `window_too_long`: окно > 90 дней (медленная обратная связь)
- `no_sli_definition`: Раздел SLI отсутствует или расплывчат ("все в порядке")
- `no_error_budget_policy`: никаких документально подтвержденных действий при сжигании бюджета
- `cpu_as_sli`: Процессор/память используются в качестве прокси-сервера пользовательского интерфейса (неверный сигнал)

## Контрольная таблица выбора SLI { #sli-selection-cheatsheet }

| Пользовательский опыт | Тип SLI | Что вы измеряете |
|---|---|---|
| "Был ли запрос выполнен успешно?" | показатель успешности запроса | `2xx / total` |
| "Реакция была быстрой?" | задержка запроса | `count(p99 < threshold) / total` |
| "Служба была включена?" | доступность-время | `(window - downtime) / window` |
| "Являются ли данные актуальными?" | свежесть данных | `count(data_age < threshold) / total` |
| "Был ли ответ правильным?" | правильность | `count(correct) / total` |

Видишь `references/sli_design.md` для примеров и анти-паттернов.

## Математика бюджета ошибок (основы) { #error-budget-math-the-basics }

Для 99,9% SLO в течение 30 дней:
- Допустимая недоступность: `0.1% × 30 × 24 × 60 = 43.2 minutes`
- порог быстрого расходования средств за 1 час (расходуется 2% от месячного бюджета): `2% × 43.2 / 60 ≈ 1.44 ratio multiplier`
- 6-часовой порог медленного горения (10% за 6 часов): `10% × 43.2 / 360 ≈ 0.6 ratio multiplier`

`error_budget_calculator.py` выполняет эту математику за вас и выдает готовые к вставке правила оповещения.

## Композиция с остальной частью портфолио { #composition-with-the-rest-of-the-portfolio }

Этот скилл явно сочетается с тремя другими:

| Скилл | Композиция |
|---|---|
| `feature-flags-architect` | Критерии прерывания раскатки ссылаются на пороговые значения скорости выгорания SLO |
| `chaos-engineering` | Калькулятор радиуса взрыва уже принимает в качестве входных данных ежемесячный бюджет ошибок - определите его здесь |
| `kubernetes-operator` | Возможности оператора L4 (глубокое понимание) требуют SLOs + правил Prometheus |

Тот `error_budget_calculator.py` выходные данные имеют ту же форму `engineering/skills/chaos-engineering/scripts/blast_radius_calculator.py` ожидает на stdin.

## Воркфлоу { #workflows }

### Воркфлоу 1: Определите новый SLO { #workflow-1-define-a-new-slo }

```
1. Pick the user journey to protect (e.g., "checkout completion").
2. Choose SLI type (request-success-rate, latency, availability, freshness, correctness).
3. Define the SLI precisely: numerator/denominator with concrete labels.
4. Pick a target by measuring 30 days of historical SLI value:
     target = floor(p50 of last 30 days × 100) / 100
   This avoids targets the system has never sustained.
5. Pick a window (28 days = 4 calendar weeks, recommended).
6. Run slo_designer.py to render the SLO definition.
7. Run error_budget_calculator.py to get burn-rate alerts.
8. Write the error budget policy (what happens when budget burns).
9. Run slo_review.py — must pass before the SLO is "live".
```

### Воркфлоу 2: Ежеквартальный ревью SLO { #workflow-2-quarterly-slo-review }

```
1. For every active SLO, run slo_review.py — fix any FAIL findings.
2. Look at last quarter's data:
   - Was the SLO too easy (never burned budget)? Tighten target.
   - Was it too hard (frequently burned)? Loosen target OR fix the system.
   - Did burn-rate alerts fire usefully (not too noisy, not too late)? Adjust thresholds.
3. Audit error budget policies — were they actually followed when budget burned?
4. Commit revised SLOs; archive old versions with date stamps.
```

### Воркфлоу 3: Откат, управляемый SLO { #workflow-3-slo-driven-rollback }

```
1. New deploy starts burning error budget faster than baseline.
2. Burn-rate alert fires (from error_budget_calculator.py thresholds).
3. Auto-rollback via feature flag (kill switch from feature-flags-architect).
4. Postmortem feeds into next SLO revision.
```

## Ссылки { #references }

- `references/slo_principles.md` — SLI против SLO против SLA, рабочая книга Google SRE для канона
- `references/sli_design.md` — выбор правильного SLI; 5 типов с примерами
- `references/error_budget.md` — математика бюджета с ошибками, оповещения о расходах, бюджетная политика
- `references/composition.md` — как в SLO подаются фич-флаги, хаос, операторы

## Слэш-команда { #slash-command }

`/slo-design` — интерактивный мастер SLO-проектирования, который запускает все 3 инструмента.

## Шаблоны активов { #asset-templates }

- `assets/slo_template.yaml` — заполняемый SLO YAML
- `assets/error_budget_policy.md` — заполняемый шаблон политики

## Анти-паттерны { #anti-patterns }

- **99,99% на каждой конечной точке** — ошибки копирования-вставки, которые никто не проверял, может ли система выдержать
- ** Использование процессора в качестве SLI** — системные показатели не являются пользовательским опытом
- ** Предупреждение о скорости выгорания в одно окно ** - слишком шумно, если 5-минутный, слишком медленно, если 30-дневный
- ** Бюджетная политика без ошибок ** — сокращение бюджета ничего не значит без принятия мер
- **Слоты без владельцев** — никто не несет ответственности; они кусаются-гниют
- **Ревью SLO проводится раз в год** — характеристики системы меняются быстрее, чем это
- ** Соглашения об уровне обслуживания в документе SLO** — разная аудитория, разные ставки; держите их отдельно
- **Цель SLO = цель SLA** — Условия SLO должны быть более жесткими (вы должны разорвать свой контракт до того, как клиенты заметят)

## Поддающийся проверке успех { #verifiable-success }

Команда, использующая этот скилл, должна достичь:

- 100% SLO проходят `slo_review.py` с 0 ошибочными выводами
- У каждого SLO есть задокументированный владелец, бюджет ошибок, предупреждения о частоте выгорания и политика
- Оповещения о частоте выгорания срабатывают ≤2 раз в месяц на каждый пораженный SLO (сигнал, а не шум)
- Среднее время обнаружения нарушения SLO: <30 мин (работают многооконные оповещения о скорости выгорания)
- Ежеквартальный ревью SLO проводится каждый квартал (не ежегодно)
