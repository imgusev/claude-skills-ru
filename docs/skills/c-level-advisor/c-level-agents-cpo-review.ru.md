---
title: "/cs:cpo-ревью — CPO форсирует вопросы { #cscpo-review--cpo-forcing-questions } — Агентский скилл для руководителей"
description: "/cs: cpo-ревью <план> — управляемый JTBD опрос о дорожной карте продукта, сигнале PMF и фокусе портфолио. Используйте при составлении дорожной карты. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:cpo-ревью — CPO форсирует вопросы { #cscpo-review--cpo-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `cpo-review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/cpo-review/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:cpo-review <plan>`

Разработчик, управляемый JTBD, сокращает дорожную карту вдвое. Шесть вопросов, которые должны всплыть на поверхность: что перевозить и что убивать.

## Когда запускать { #when-to-run }

- До принятия ежеквартальных обязательств по дорожной карте
- Перед запуском новой линейки продуктов
- Перед добавлением > 3 функций в выпуск
- Когда удержание остается неизменным или снижается
- Когда команда обсуждает "должны ли мы создавать X?"

## Шесть вопросов CPO { #the-six-cpo-questions }

### 1. JTBD { #1-jtbd }
** Для выполнения какой работы, по словам пользователя, нанята эта функция?**
- Не "улучшать онбординг". "Помогите новому операционному менеджеру закрыть их первую сделку в течение 7 дней".
- Задание ≠ функция. Нанять - попробуй.

### 2. Метрика полярной звезды { #2-north-star-metric }
** Какое поведение пользователя приводит к этому перемещению и как эта лестница ведет к Полярной звезде?**
- Показатель должен быть ведущим, основанным на поведении и коррелированным с ценностями.
- Если вы не можете отследить объект до Полярной звезды, не создавайте его.

### 3. Сигнал PMF { #3-pmf-signal }
** Какова кривая удержания пользователей, которые нанимаются на эту работу — она плоская, затухающая или улыбчивая?**
- Ровный или улыбающийся = сигнал PMF. Затухание = отсутствие PMF.
- "Пользователям нравится это в опросах" - это не сигнал.

### 4. Оценка РИСА { #4-rice-score }
** Охват, влияние, уверенность, усилия — каков балл и какое место это занимает в очереди?**
```bash
python product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py
```

### 5. Альтернативные издержки { #5-opportunity-cost }
** Что будет сокращено, если это отправится? Назовите конкретную инициативу или функцию.**
- Численность персонала и время имеют нулевую сумму. Список вырезов - это список фокусов.

### 6. Критерии уничтожения { #6-kill-criteria }
** Какой сигнал через 90 дней подскажет вам, что это была неправильная ставка?**
- Определите показатель и пороговое значение в письменной форме перед запуском.
- Если вы не можете определить критерий уничтожения, вы не сможете ответственно отнестись к отправке.

## Воркфлоу { #workflow }

1. **Запустите анализы:**
   ```bash
   python ../../../skills/cpo-advisor/scripts/pmf_scorer.py
   python ../../../skills/cpo-advisor/scripts/portfolio_analyzer.py
   ```
2. ** Ответьте на шесть вопросов.**
3. ** Вынесите вердикт.**

## Выходной формат { #output-format }

```markdown
# CPO Review: <feature/plan>
**Date:** YYYY-MM-DD

## JTBD
> <one sentence in user voice>

## North Star Link
- Metric moved: <name>
- Expected delta: <%>

## PMF Signal
- Retention curve shape: flat / smiling / decaying
- Cohort sample size: N

## Score
- RICE: <number>
- Rank in queue: #N of M

## Cut List
- Cut: <initiative>
- Reason: <why this matters more>

## Kill Criteria (90 days)
- Metric: <name>
- Threshold: <value>
- Action if missed: <kill | iterate>

## Verdict
🟢 SHIP | 🟡 SHARPEN | 🔴 KILL
```

## Маршрутизация { #routing }

- `/cs:cmo-review` — поддерживает ли позиционирование эту функцию?
- `/cs:execute` — составьте 90-дневный план
- `/cs:post-mortem` — если триггер "критерии уничтожения" сработал

## Связанный { #related }

- Агент: [`cs-cpo-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/agents/cs-cpo-advisor.md)
- Скилл: [`cpo-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/cpo-advisor/SKILL.md)
- Исполнение: `product-team/skills/product-manager-toolkit/`

---

**Версия:** 1.0.0
