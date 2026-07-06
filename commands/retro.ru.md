---
name: retro
description: "Проанализируйте ретроспективы спринта на предмет выявления закономерностей и отслеживания элементов действий. Использование: /ретро анализ <retro_data.json>"
---

# /retro { #retro }

Проанализируйте данные ретроспективы на предмет повторяющихся тем, тенденций настроений и эффективности действий.

## Использование { #usage }

```
/retro analyze <retro_data.json>                             Full retrospective analysis
```

## Формат ввода { #input-format }

```json
{
  "sprint_name": "Sprint 24",
  "went_well": ["CI pipeline improvements", "Pair programming sessions"],
  "improvements": ["Too many meetings", "Flaky integration tests"],
  "action_items": [
    {"description": "Reduce standup to 10 min", "owner": "SM", "status": "done"},
    {"description": "Fix flaky tests", "owner": "QA Lead", "status": "in_progress"}
  ],
  "participants": 8
}
```

## Примеры { #examples }

```
/retro analyze sprint-24-retro.json
/retro analyze sprint-24-retro.json --format json
```

## Сценарии { #scripts }
- `project-management/skills/scrum-master/scripts/retrospective_analyzer.py` — Анализатор ретроспективы (`<data_file> [--format text|json]`)

## Ссылка на Скилл { #skill-reference }
> `project-management/skills/scrum-master/SKILL.md`
