---
name: "cs-grill-with-docs"
description: "/cs:grill-with-docs <путь-к-плану> — Запуск сеанса приготовления на гриле с привязкой к документам. Предварительные рейсы CONTEXT.md + docs/adr/ linters, затем опрашивает план по одному решению за раз, обновляя глоссарий + встроенное написание ADR по мере их кристаллизации."
---

# /cs:grill-with-docs — Привязанный к документам план допроса { #csgrill-with-docs--docs-anchored-plan-interrogation }

**Команда:** `/cs:grill-with-docs <path-to-plan>`

Тот `cs-grill-with-docs` персона предварительно знакомится с документированным языком проекта и решениями, затем обрабатывает план по одной ветви за раз, противопоставляя нечеткие термины `CONTEXT.md`, выявляя противоречия между кодом и глоссарием и записывая ADR только тогда, когда выполняется гейт из 3 критериев.

## Когда запускать { #when-to-run }

- Стресс-тестирование плана, который использует установленную кодовую базу с документированным языком
- Онбординг новой функции в существующий ограниченный контекст
- Устранение двусмысленности, возникающей из-за смещения между глоссарием и кодом
- Предварительная оценка архитектурного решения перед его принятием

## Когда не запускать (использовать `/cs:grill-me` вместо этого) { #when-not-to-run-use-csgrill-me-instead }

- У репозитория нет `CONTEXT.md` и нет `docs/adr/` и вы не хотите их засевать
- Вам нужен гриль только по плану в вакууме (привязка к документам не добавит никакого сигнала)
- План является исследовательским / до принятия языкового решения

## Шесть шаблонов принудительных вопросов (с привязкой к документам) { #the-six-forcing-question-patterns-docs-anchored }

1. **Конфликт в глоссарии:** "CONTEXT.md определяет '{term}- как X. Вы только что использовали его в значении Y. Что это — или это два разных понятия?"
2. **Противоречие ДОПОГ:** "ДОПОГ-{nnnn} запертый в {choice} Ваш план подразумевает {opposite}. Мы заменяем друг друга, или план отклонился от курса?"
3. **Неопределенный термин:** "Вы сказали '{term}'. CONTEXT.md это не определяет его. Ты имеешь в виду {candidate-1}, {candidate-2} или что-то новое?"
4. ** Код против утверждения: ** "В вашем коде написано X. Вы только что сказали Y. Каково текущее состояние — и что мы меняем?"
5. **ДОПОГ 3 - гейт по критериям:** "Это решение может быть отменено во второй половине дня. Зачем ему нужен ADR? Если "это не так" — пропустите это".
6. ** Проверка границ:** "Какому ограниченному контексту принадлежит это понятие? Если два контекста оба касаются этого, каков контракт между ними?"

## Дисциплина { #discipline }

- ** Сначала подготовьте линтеры к полету.** Никогда не готовьте на гриле без моментального снимка состояния документов.
- ** По одному вопросу за ход. ** Никогда не связывайтесь.
- ** Рекомендуемый ответ прилагается.** Каждый вопрос содержит позицию + обоснование.
- ** Кодовая база + документы перед предположениями.** `grep` / `Read` / ворсинка рассасывается перед тем, как спрашивать.
- **CONTEXT.md отредактировано встроенно.** Никаких отложенных пакетов глоссариев.
- **Гейт по критериям ADR 3.** Трудно поддающийся отмене + неожиданный + реальный компромисс. Все три или пропустить.

## Воркфлоу { #workflow }

```bash
# 1. Pre-flight — snapshot the docs state
python ../skills/grill-with-docs/scripts/context_md_linter.py CONTEXT.md
python ../skills/grill-with-docs/scripts/adr_scanner.py docs/adr/
python ../skills/grill-with-docs/scripts/glossary_code_consistency.py \
  --context CONTEXT.md --code src/

# 2. Read the plan
#    Use the linter findings as opening question seeds.

# 3. Walk one question at a time:
#    Persona asks Q1 with recommendation (anchored to docs/code).
#    User answers.
#    Apply edits inline if the answer changes the glossary or warrants an ADR.

# 4. Re-lint after any structural CONTEXT.md edit:
python ../skills/grill-with-docs/scripts/context_md_linter.py CONTEXT.md

# 5. Re-scan after any new ADR:
python ../skills/grill-with-docs/scripts/adr_scanner.py docs/adr/

# 6. At close — final consistency sweep:
python ../skills/grill-with-docs/scripts/glossary_code_consistency.py \
  --context CONTEXT.md --code src/
```

## Когда остановиться { #when-to-stop }

- У каждой ветви есть ответ, И
- Конечное состояние lint является чистым (context_md_linter + adr_scanner оба ПРОХОДЯТ), И
- За последние 3 хода не появилось никаких новых нечетких терминов

Подготовьте сводку "изменения в глоссарии + ADR + открытые элементы" при закрытии.

## Выходной формат { #output-format }

```
Q[i]/[total] (anchor: CONTEXT.md§Language | ADR-0003 | code:src/orders/cancel.ts:42 | plan:L18):

[question]

Recommended: [position] because [rationale grounded in the anchor]
```

## Связанный { #related }

- Агент: [`cs-grill-with-docs`](../agents/cs-grill-with-docs.md)
- Скилл: [`grill-with-docs`](../skills/grill-with-docs/SKILL.md)
- Спецификации формата: [ФОРМАТ ADR](../skills/grill-with-docs/ADR-FORMAT.md), [КОНТЕКСТ-ФОРМАТ](../skills/grill-with-docs/CONTEXT-FORMAT.md)
- Скилл родного брата: `/cs:grill-me` (гриль только для готовки)
- Смежный: `/cs:caveman`, `/cs:handoff`, `/cs:write-a-skill`

---

**Версия:** 1.0.0
** Производное: ** Matt Pocock's grill-with-docs (MIT) + оболочка этого репозитория
