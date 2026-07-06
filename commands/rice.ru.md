---
name: rice
description: "В RICE предусмотрена расстановка приоритетов с помощью подсчета очков и планирования производственных мощностей. Использование: /rice расставляет приоритеты <features.csv> [параметры]"
---

# /рис { #rice }

Расставьте приоритеты функций, используя оценку RICE (охват, воздействие, уверенность, усилия) с дополнительными ограничениями по мощности.

## Использование { #usage }

```
/rice prioritize <features.csv>                              Score and rank features
/rice prioritize <features.csv> --capacity 20                Rank with effort capacity limit
```

## Формат ввода { #input-format }

```csv
feature,reach,impact,confidence,effort
Dark mode,5000,2,0.8,3
API v2,12000,3,0.9,8
SSO integration,3000,2,0.7,5
Mobile app,20000,3,0.5,13
```

## Примеры { #examples }

```
/rice prioritize features.csv
/rice prioritize features.csv --capacity 20
/rice prioritize features.csv --output json
```

## Сценарии { #scripts }
- `product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py` — Определитель приоритетов риса (`<input.csv> [--capacity N] [--output text|json|csv]`)

## Ссылка на Скилл { #skill-reference }
> `product-team/skills/product-manager-toolkit/SKILL.md`
