---
title: "/okr — слэш-команда для ИИ-агентов разработки"
description: "Создавайте каскады OKR от стратегии компании до целей команды. Использование: /okr генерирует <стратегию>. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /okr

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/okr.md">Источник</a></span>
</div>


Создавайте каскадные фреймворки OKR, начиная со стратегии на уровне компании и заканчивая ключевыми результатами на уровне команды.

## Использование { #usage }

```
/okr generate <strategy>                                     Generate OKR cascade
```

Поддерживаемые стратегии: `growth`, `retention`, `revenue`, `innovation`, `operational`

## Формат ввода { #input-format }

Передайте ключевое слово стратегии напрямую. Генератор выдает OKR на уровне компании, отдела и команды в соответствии с выбранной стратегией.

## Примеры { #examples }

```
/okr generate growth
/okr generate retention
/okr generate revenue
/okr generate innovation
/okr generate operational
/okr generate growth --json
```

## Сценарии { #scripts }
- `product-team/skills/product-strategist/scripts/okr_cascade_generator.py` — Каскадный генератор OKR (`<strategy> [--teams "A,B,C"] [--contribution 0.3] [--json]`)

## Ссылка на Скилл { #skill-reference }
> `product-team/skills/product-strategist/SKILL.md`
