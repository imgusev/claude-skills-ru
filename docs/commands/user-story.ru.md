---
title: "/user-story — слэш-команда для ИИ-агентов разработки"
description: "Создавайте пользовательские истории с критериями приемлемости и планированием спринта. Использование: /user-story <сгенерировать|спринт> [параметры]. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /user-story

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/user-story.md">Источник</a></span>
</div>


Создавайте структурированные пользовательские истории с критериями приемлемости, точками публикации и планированием пропускной способности спринта.

## Использование { #usage }

```
/user-story generate                                         Generate user stories (interactive)
/user-story sprint <capacity>                                Plan sprint with story point capacity
```

## Формат ввода { #input-format }

Интерактивный режим промпт для ввода контекста объекта. Для планирования спринта укажите пропускную способность в качестве сюжетных точек:

```
/user-story generate
> Feature: User authentication
> Persona: Engineering manager
> Epic: Platform Security

/user-story sprint 21
> Stories are ranked by priority and fit within 21-point capacity
```

## Примеры { #examples }

```
/user-story generate
/user-story sprint 34
/user-story sprint 21
```

## Сценарии { #scripts }
- `product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py` — Генератор пользовательских историй (позиционные аргументы: `sprint <capacity>`)

## Ссылка на Скилл { #skill-reference }
> `product-team/agile-product-owner/skills/agile-product-owner/SKILL.md`
