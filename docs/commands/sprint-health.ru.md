---
title: "/sprint-health — слэш-команда для ИИ-агентов разработки"
description: "Оценка работоспособности в спринте и анализ скорости для гибких команд. Использование: /спринт-работоспособность <анализ|скорость> [параметры]. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /sprint-health

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/sprint-health.md">Источник</a></span>
</div>


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
