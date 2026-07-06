---
name: competitive-matrix
description: "Создайте матрицы конкурентного анализа с помощью скоринга и анализа пробелов. Использование: /конкурентная матрица <анализ> [параметры]"
argument-hint: "<analyze> [options]"
---

# /competitive-matrix { #competitive-matrix }

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
