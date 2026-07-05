---
title: "/cs:cro-ревью — CRO форсирует вопросы { #cscro-review--cro-forcing-questions } — Агентский скилл для руководителей"
description: "/cs:cro-ревью <плана> — Пайплайн - параноидальный опрос о доходах, коэффициенте выигрыша, NRR и времени нарастания. Используйте, когда прогноз не. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:cro-ревью — CRO форсирует вопросы { #cscro-review--cro-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `cro-review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/cro-review/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:cro-review <plan>`

Пайплайн - параноидальное давление оператора - проверяет предположения о доходах. Шесть вопросов, которые поднимут проблему следующего квартала в этом квартале.

## Когда запускать { #when-to-run }

- Прежде чем взять на себя обязательства по достижению квартального целевого показателя выручки
- Перед изменением направления продаж (PLG ↔ ориентированный на продажи, средний рынок ↔ предприятие)
- Прежде чем нанимать группу представителей
- Когда покрытие пайплайна падает ниже 3-кратного
- Когда NRR имеет тенденцию к снижению

## Шесть вопросов CRO { #the-six-cro-questions }

### 1. Покрытие пайплайна { #1-pipeline-coverage }
**Каков охват пайплайна на текущий квартал в разбивке по этапам?**
- Высокий уровень входящих сообщений: в 3 раза. Высокий уровень исходящих сообщений: в 4 раза. Ниже любого из пороговых значений = действуйте сейчас.
- Взвешенный по этапам, а не просто суммарный.

### 2. Траектория выигрышной ставки { #2-win-rate-trajectory }
** Каков процент побед в этом квартале по сравнению с предыдущими 4—мя - и какова точка утечки?**
- Поэтапное преобразование.
- Если на каком-то одном этапе происходит смягчение, определите причину, прежде чем прогнозировать.

### 3. Разложение NRR { #3-nrr-decomposition }
** Что такое общее удержание, сокращение и расширение по отдельности?**
- Только NRR скрывает отток.
- Показатель NRR в 110% при общем удержании 95% отличается от 110% при 80%.

### 4. Время нарастания { #4-ramp-time }
** Для последних 4 сотрудников, сколько дней требуется для первой сделки и квотирования?**
- Если период роста превышает 90 дней, профиль найма или предоставление возможностей нарушается.
- Предполагаемые наймиты должны набираться по нарастающей.

### 5. Дисконтная дисциплина { #5-discount-discipline }
** Какова средняя скидка в этом квартале по сравнению с предыдущими 4 кварталами? Куда это ползет?**
- Ползучесть скидок является основным показателем слабости ценообразования или позиционирования.
- Ограничивайте скидки в зависимости от уровня утверждающего.

### 6. Исходная смесь для пайплайна { #6-pipeline-source-mix }
**Какой % пайплайна создается за счет маркетинга, продаж и партнеров?**
- Если один источник доминирует более чем на 80%, у вас есть риск концентрации.
- Перепроверьте с cs-cmo-advisor.

## Воркфлоу { #workflow }

```bash
python ../../../skills/cro-advisor/scripts/revenue_forecast_model.py
python ../../../skills/cro-advisor/scripts/churn_analyzer.py
```

## Выходной формат { #output-format }

```markdown
# CRO Review: <plan>
**Date:** YYYY-MM-DD

## Pipeline
- Coverage: X.Xx (target 3x+)
- Win rate: X% (4Q trend: ↑ / → / ↓)
- Top leaking stage: <name>

## Retention
- Gross retention: X%
- NRR: X%
- Expansion: X%
- Contraction: X%

## Ramp
- New hires last quarter: N
- Median days to first deal: X
- Median days to quota: X

## Discount
- Median discount this quarter: X%
- Trend vs 4Q ago: <delta>

## Source Mix
- Marketing: X% | Sales: X% | Partner: X%

## Verdict
🟢 ON PLAN | 🟡 GAP | 🔴 PIPELINE CRISIS

## Next Steps
[3 concrete actions]
```

## Маршрутизация { #routing }

- `/cs:cfo-review` — это входит в кассовый план?
- `/cs:cmo-review` — полезна ли смесь источников для пайплайна?
- `/cs:execute` — квартальный план, если ЗЕЛЕНЫЙ
- `/cs:boardroom` — если КРАСНЫЙ

## Связанный { #related }

- Агент: [`cs-cro-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/agents/cs-cro-advisor.md)
- Скилл: [`cro-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/cro-advisor/SKILL.md)
- Исполнение: [`business-growth`](https://github.com/imgusev/claude-skills-ru/tree/main/business-growth)

---

**Версия:** 1.0.0
