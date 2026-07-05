---
title: "Допрашивай меня { #grill-me } — Агентский скилл для Codex и OpenClaw"
description: "Неустанно опрашивайте пользователя о плане или дизайне до достижения общего понимания, разрешая каждую ветвь дерева решений. Используйте, когда. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Допрашивай меня { #grill-me }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `grill-me`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/grill-me/skills/grill-me/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> Полученный из [Гриль-бар Мэтта Покока-я](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) (Массачусетский технологический институт). Дисциплина интервью Мэтта сохранилась дословно. Дополнения: извлечение + вопрос + инструменты сеанса + ссылки + оболочка cs-* (смотрите [ссылки/companion_tooling.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/grill-me/skills/grill-me/references/companion_tooling.md)).

Неустанно расспрашивайте меня о каждом аспекте этого плана, пока мы не придем к общему пониманию. Пройдитесь по каждой ветви дерева проектирования, устраняя зависимости между решениями одно за другим. На каждый вопрос укажите свой рекомендуемый ответ.

Задавайте вопросы по одному за раз.

Если на вопрос можно ответить, изучив кодовую базу, изучите ее вместо этого.

## Правила (сохранены + дополнены) { #rules-preserved--amplified }

1. ** По одному вопросу за ход. ** Никогда не связывайтесь.
2. ** Укажите рекомендуемый ответ на каждый вопрос.** По умолчанию задавать вопрос "что вы думаете?" - это лень.
3. ** Изучите кодовую базу, прежде чем задавать вопрос.** Если `grep` / `Read` чтобы решить эту проблему, сделайте это в первую очередь. Сохраняет ход.
4. ** Сначала пройдитесь по дереву в глубину. ** Закончите одну ветку, прежде чем открывать другую.
5. **Отслеживание зависимостей.** Если решение В зависит от решения А, сначала спросите А.

## Воркфлоу { #workflow }

1. Пользователь предоставляет план или дизайн (или путь к нему).
2. Бежать `scripts/decision_tree_extractor.py` для извлечения веток.
3. Бежать `scripts/question_generator.py` подготовить список вопросов с рекомендациями.
4. Начать сеанс: `scripts/grill_session_tracker.py --action start`.
5. Пройдитесь по дереву, задавая по одному вопросу за раз, записывая ответы во время сеанса.
6. Когда все ветви разрешены: отчет "достигнуто общее понимание" + заблокированные решения.

## Шаблон вывода { #output-pattern }

За каждый поворот вопроса:

```
Q[i]/[total]: [question]
Recommended answer: [your call + 1-sentence rationale]

(Or: I explored the codebase and found [evidence]. Confirm?)
```

## Оснастка { #tooling }

Видишь [ссылки/companion_tooling.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/grill-me/skills/grill-me/references/companion_tooling.md) Инструменты: экстрактор + генератор + трекер. Агент: `cs-grill-master`. Команда: `/cs:grill-me`.

---

**Версия:** 1.0.0
** Производное: ** Мэтт Покок (Массачусетский технологический институт) + оболочка этого репозитория
