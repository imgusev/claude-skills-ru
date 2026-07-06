---
title: "/cs:cfo-review — Финансовый директор, форсирующий вопросы { #cscfo-review--cfo-forcing-questions } — Агентский скилл для руководителей"
description: "/cs: финансовый директор - ревью <плана> — Подсчитать - скептическое отношение к любому плану, который касается денег. Экономика предприятия. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:cfo-review — Финансовый директор, форсирующий вопросы { #cscfo-review--cfo-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `cfo-review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/cfo-review/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:cfo-review <plan>`

Заядлый скептик подвергает стресс-тестированию все, что касается денег. Шесть вопросов перед любыми тратами или сбором средств.

## Когда запускать { #when-to-run }

- Прежде чем одобрять какие-либо расходы > 1% от выручки
- Перед открытием новой заявки на прием на работу
- Перед любым разговором о сборе средств
- Перед изменением ценообразования или удельной экономики
- Перед подписанием многолетнего контракта

## Шесть вопросов финансовому директору { #the-six-cfo-questions }

### 1. Ожог и взлетно-посадочная полоса { #1-burn--runway }
** Каков коэффициент выгорания и сколько месяцев наличных денег остается на базовом / бычьем / медвежьем рынке?**
- Записать несколько раз = Чистая запись ÷ Чистая новая запись. Выше 2x - это проблема.
- Если срок подачи заявки < 12 месяцев, вы уже находитесь в режиме сбора средств.

### 2. Экономика подразделения { #2-unit-economics }
**Сколько стоит LTV / CAC для каждого канала и каков срок окупаемости на каналах из топ-2?**
- LTV / CAC > 3x - это нормально. Окупаемость < 12 месяцев - это нормально.
- Если какой-либо из них сломан, не масштабируйте этот канал.

### 3. Путь разбавления { #3-dilution-path }
**Если этот план требует повышения, каково разбавление базовой и медвежьей оценок?**
- Разбавление основателя за раунд.
- Кумулятивное разбавление до следующих 2 раундов.

### 4. Альтернативный вариант распределения капитала { #4-capital-allocation-alternative }
** Если этот доллар был потрачен не здесь, куда еще он мог бы пойти и какова ожидаемая отдача?**
- Три альтернативы: найм, продукт, маркетинг.
- Четко укажите альтернативные издержки.

### 5. Качество выручки { #5-revenue-quality }
**Какова валовая прибыль и как она меняется в масштабе?**
- Если поле сжимается с увеличением масштаба, модель нарушается.
- Затраты на выручку должны расти медленнее, чем выручка.

### 6. Выживание в случае с медведем { #6-bear-case-survival }
**Если выручка составляет 50% от плана, продержится ли компания 18 месяцев?**
- Значение по умолчанию-alive не подлежит обсуждению.
- Если нет, заранее определите триггеры отключения.

## Воркфлоу { #workflow }

1. **Прогоните цифры:**
   ```bash
   python ../../../skills/cfo-advisor/scripts/burn_rate_calculator.py
   python ../../../skills/cfo-advisor/scripts/unit_economics_analyzer.py
   python ../../../skills/cfo-advisor/scripts/fundraising_model.py
   ```
2. ** Ответьте на все шесть вопросов** цифрами, а не прилагательными.
3. **Вынести вердикт:**
   - 🟢 ЗЕЛЕНЫЙ — финансируйте это
   - 🟡 ЖЕЛТЫЙ — фонд с сокращенными триггерами
   - 🔴 КРАСНЫЙ — уничтожить или пересмотреть

## Выходной формат { #output-format }

```markdown
# CFO Review: <plan>
**Date:** YYYY-MM-DD
**Reviewer:** cs-cfo-advisor

## Numbers
- Burn multiple: X.Xx
- Runway (base/bull/bear): X / X / X months
- LTV/CAC top channel: X.Xx, payback Y months
- Gross margin: X% (trend: Y)
- Dilution this round: X%
- Bear-case survival: PASS / FAIL

## Verdict
🟢 GREEN | 🟡 YELLOW | 🔴 RED

## Conditions (if YELLOW)
- Cut trigger: <metric> < <threshold> → <action>
- Review checkpoint: <date>

## Recommendation
[3 concrete next steps]
```

## Маршрутизация { #routing }

- `/cs:decide` — зарегистрируйте вердикт
- `/cs:execute` — составьте 90-дневный план, если он ЗЕЛЕНЫЙ
- `/cs:boardroom` — эскалация, если многоцелевые последствия

## Связанный { #related }

- Агент: [`cs-cfo-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/agents/cs-cfo-advisor.md)
- Скилл: [`cfo-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/cfo-advisor/SKILL.md)

---

**Версия:** 1.0.0
