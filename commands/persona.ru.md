---
name: persona
description: "Создавайте пользовательские образы, основанные на данных, для исследований UX и проектирования продуктов. Использование: /создание персоны [параметры]"
---

# /persona { #persona }

Создавайте структурированные пользовательские образы с демографическими данными, целями, болевыми точками и поведенческими моделями.

## Использование { #usage }

```
/persona generate                                            Generate persona (interactive)
/persona generate json                                       Generate persona as JSON
```

## Формат ввода { #input-format }

Интерактивный режим промпт для определения контекста продукта. В качестве альтернативы, предоставьте встроенный контекст:

```
/persona generate
> Product: B2B project management tool
> Target: Engineering managers at mid-size companies
> Key problem: Cross-team visibility
```

## Примеры { #examples }

```
/persona generate
/persona generate json
/persona generate json > persona-eng-manager.json
```

## Сценарии { #scripts }
- `product-team/skills/ux-researcher-designer/scripts/persona_generator.py` — Генератор персон (позиционный `json` аргумент для вывода в формате JSON)

## Ссылка на Скилл { #skill-reference }
> `product-team/skills/ux-researcher-designer/SKILL.md`
