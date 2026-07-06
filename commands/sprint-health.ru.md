---
name: sprint-health
description: "Оценка работоспособности в спринте и анализ скорости для гибких команд. Использование: /спринт-работоспособность <анализ|скорость> [параметры]"
argument-hint: "<analyze|velocity> [options]"
---

# /спринт-здоровье { #sprint-health }

Оценивайте работоспособность спринта по показателям доставки, качества и команды с помощью анализа тенденций скорости.

## Использование { #usage }

```
/sprint-health analyze <sprint_data.json>                    Full sprint health score
/sprint-health velocity <sprint_data.json>                   Velocity trend analysis
```

## Формат ввода { #input-format }

```json
{
  "sprint_name": "Sprint 24",
  "committed_points": 34,
  "completed_points": 29,
  "stories": {"total": 12, "completed": 10, "carried_over": 2},
  "blockers": [{"description": "API dependency", "days_blocked": 3}],
  "ceremonies": {"planning": true, "daily": true, "review": true, "retro": true}
}
```

## Примеры { #examples }

```
/sprint-health analyze sprint-24.json
/sprint-health velocity last-6-sprints.json
/sprint-health analyze sprint-24.json --format json
```

## Сценарии { #scripts }
- `project-management/skills/scrum-master/scripts/sprint_health_scorer.py` — Показатель здоровья в спринте (`<data_file> [--format text|json]`)
- `project-management/skills/scrum-master/scripts/velocity_analyzer.py` — Анализатор скорости (`<data_file> [--format text|json]`)

## Ссылка на Скилл { #skill-reference }
> `project-management/skills/scrum-master/SKILL.md`
