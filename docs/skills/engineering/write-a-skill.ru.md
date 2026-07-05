---
title: "Письменные скиллы { #writing-skills } — Агентский скилл для Codex и OpenClaw"
description: "Создавайте новые скиллы агента с надлежащей структурой, постепенным раскрытием информации и комплексными ресурсами. Используйте, когда пользователь. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Письменные скиллы { #writing-skills }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `write-a-skill`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/write-a-skill/skills/write-a-skill/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> Полученный из [Скилл Мэтта Покока по написанию](https://github.com/mattpocock/skills/tree/main/skills/productivity/write-a-skill) (Массачусетский технологический институт). Голос Мэтта и трехэтапный воркфлоу сохранены дословно. Дополнения: инструменты проверки + ссылки + cs-* оболочка (смотрите *Инструменты + компаньоны* ниже).

## Процесс { #process }

1. **Соберите требования ** - спросите пользователя о:
   - Какую задачу/предметную область охватывает этот скилл?
   - Какие конкретные варианты использования он должен обрабатывать?
   - Нужны ли для этого исполняемые скрипты или просто инструкции?
   - Какие-либо справочные материалы следует включить?

2. **Набросать скилл** - создать:
   - SKILL.md с краткими инструкциями
   - Дополнительные справочные файлы, если содержимое превышает 500 строк
   - Служебные скрипты, если требуются детерминированные операции

3. ** Ревью с пользователем** - представьте черновик и спросите:
   - Распространяется ли это на ваши варианты использования?
   - Чего-нибудь не хватает или неясно?
   - Должен ли какой-либо раздел быть более/менее подробным?

## Структура скилла { #skill-structure }

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Шаблон { #skillmd-template }

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/write-a-skill/skills/write-a-skill/REFERENCE.md)]
```

## Требования к описанию { #description-requirements }

Описание - это ** единственное, что видит ваш агент** при принятии решения о том, какой скилл загрузить. Он появляется в системной промпте вместе со всеми другими установленными скиллы. Ваш агент читает эти описания и выбирает соответствующий скилл на основе запроса пользователя.

**Цель**: Предоставьте своему агенту ровно столько информации, чтобы он знал:

1. Какие возможности предоставляет этот скилл
2. Когда/почему его триггеры (конкретные ключевые слова, контексты, типы файлов)

**Формат**:

- Максимальное количество символов - 1024
- Пишите от третьего лица
- Первое предложение: что он делает
- Второе предложение: "Используйте, когда [конкретные триггеры]"

**Хороший пример**:

```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**Плохой пример**:

```
Helps with documents.
```

Неудачный пример не дает вашему агенту возможности отличить это от других скилл, связанных с документооборотом.

## Когда добавлять скрипты { #when-to-add-scripts }

Добавляйте служебные скрипты, когда:

- Операция является детерминированной (проверка, форматирование)
- Один и тот же код будет генерироваться повторно
- Ошибки требуют явной обработки

Скрипты экономят токены и повышают надежность по сравнению с сгенерированным кодом.

## Когда следует разделять файлы { #when-to-split-files }

Разделить на отдельные файлы, когда:

- SKILL.md превышает 100 строк
- Контент имеет различные домены (финансы и схемы продаж).
- Расширенные функции требуются редко

## Ревью Чек-лист - "Контрольный список" Review Review { #review-checklist }

После составления проекта проверьте:

- [ ] Описание включает в себя триггеры ("Использовать, когда...")
- [ ] SKILL.md менее 100 строк
- [ ] Нет информации, зависящей от времени
- [ ] Согласованная терминология
- [ ] Включены конкретные примеры
- [ ] Ссылки на глубину в один уровень

## Инструменты + компаньоны { #tooling--companions }

Инструменты проверки + оболочка cs-* дополняют этот скилл. Запустите все 6 пунктов чек-листа для ревью программно:

```
python scripts/skill_review_checklist_runner.py path/to/skill-folder
```

Видишь [ссылки/companion_tooling.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/write-a-skill/skills/write-a-skill/references/companion_tooling.md) для каталога инструментов cs-скилл-автор персоны агента, а `/cs:write-a-skill` слэш-команда.

---

**Версия:** 1.0.0
** Производное: ** Мэтт Покок (Массачусетский технологический институт) + оболочка этого репозитория
