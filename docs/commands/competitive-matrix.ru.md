---
title: "/competitive-matrix — слэш-команда для ИИ-агентов разработки"
description: "Создайте матрицы конкурентного анализа с помощью скоринга и анализа пробелов. Использование: /конкурентная матрица <анализ> [параметры]. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /competitive-matrix

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/competitive-matrix.md">Источник</a></span>
</div>


Создавайте конкурентные матрицы с использованием взвешенных оценок, анализа пробелов и информации о позиционировании на рынке.

## Использование { #usage }

```
/competitive-matrix analyze <competitors.json>                    Full analysis
/competitive-matrix analyze <competitors.json> --weights pricing=2,ux=1.5    Custom weights
```

## Формат ввода { #input-format }

```json
{
  "your_product": { "name": "MyApp", "scores": {"ux": 8, "pricing": 7, "features": 9} },
  "competitors": [
    { "name": "Competitor A", "scores": {"ux": 7, "pricing": 9, "features": 6} }
  ],
  "dimensions": ["ux", "pricing", "features"]
}
```

## Примеры { #examples }

```
/competitive-matrix analyze competitors.json
/competitive-matrix analyze competitors.json --format json --output matrix.json
```

## Сценарии { #scripts }
- `product-team/skills/competitive-teardown/scripts/competitive_matrix_builder.py` — Построитель матриц

## Ссылка на Скилл { #skill-reference }
→ `product-team/skills/competitive-teardown/SKILL.md`
