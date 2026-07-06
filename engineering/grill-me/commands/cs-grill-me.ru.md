---
name: "cs-grill-me"
description: "/cs: grill-me <путь к плану> — Начните безжалостный допрос плана или замысла. Обходит дерево решений по одной ветви за раз. По одному вопросу за ход с рекомендуемым ответом. Исследует кодовую базу, прежде чем задавать вопрос."
---

# /cs:grill-me — Безжалостный план допроса { #csgrill-me--relentless-plan-interrogation }

**Команда:** `/cs:grill-me <path-to-plan>`

Персона гриль-мастера опрашивает план по одной ветви принятия решения за раз.

## Когда запускать { #when-to-run }

- Стресс-тестирование плана перед принятием обязательств
- Предварительный анализ проекта (найдите слабые места до того, как они причинят вред)
- Онбординг в соответствии с существующим планом (опросите, что там есть)
- Возобновление приготовления на гриле с предыдущего хода

## Шесть моделей навязывания вопросов { #the-six-forcing-question-patterns }

1. **Намерение:** "Почему X, а не Y?" (называет альтернативу)
2. ** Выбор: ** "На чьей стороне и что является решающим ограничением?"
3. **Открыть:** "Что блокирует это решение и когда блокировщик разрешится?"
4. ** Компромисс: ** "Для какой стороны вы проводите оптимизацию и каков критерий уничтожения?"
5. **Зависимость:** "Заблокировано ли восходящее решение? Если нет, то это на первом месте."
6. ** Неопределенность:** "Даже при 60%—ной уверенности - каково ваше лучшее предположение?"

## Дисциплина { #discipline }

- ** По одному вопросу за ход. ** Никогда не связывайтесь.
- ** Рекомендуемый ответ прилагается.** Каждый вопрос содержит позицию + обоснование.
- ** Кодовая база до спекуляций.** `grep` / `Read` решает, прежде чем спрашивать.
- ** Глубина- первая прогулка.** Завершите работу с одной веткой, прежде чем открывать другую.

## Воркфлоу { #workflow }

```bash
# 1. Extract decision branches from the plan
python ../skills/grill-me/scripts/decision_tree_extractor.py path/to/plan.md

# 2. Generate forcing questions with recommendations
python ../skills/grill-me/scripts/question_generator.py path/to/plan.md

# 3. Start session
python ../skills/grill-me/scripts/grill_session_tracker.py --action start --session NAME --plan path/to/plan.md

# 4. Walk one question at a time:
#    Persona asks Q1 with recommendation.
#    User answers.
#    Record:
python ../skills/grill-me/scripts/grill_session_tracker.py --action record --session NAME --question-id 1 --answer "..."

# 5. When complete:
python ../skills/grill-me/scripts/grill_session_tracker.py --action close --session NAME
```

## Когда остановиться { #when-to-stop }

- У каждой ветви есть ответ
- 3+ хода без возникновения новых вопросов
- Пользователь сигнализирует об усталости ("можем ли мы двигаться дальше?")
- Уменьшение отдачи после ~ 15 вопросов

Подготовьте сводку "решения заблокированы" в конце.

## Выходной формат { #output-format }

```
Q[i]/[total] (L[line]): [question]
Recommended: [position] because [1-sentence rationale]

(or: I explored — found [evidence]. Confirm?)
```

## Связанный { #related }

- Агент: [`cs-grill-master`](../agents/cs-grill-master.md)
- Скилл: [`grill-me`](../skills/grill-me/SKILL.md)
- Смежный: `/cs:caveman`, `/cs:handoff`, `/cs:write-a-skill`

---

**Версия:** 1.0.0
** Производное: ** Matt Pocock's grill-me (Массачусетский технологический институт) + оболочка этого репозитория
