---
name: project-health
description: "Дашборд состояния портфеля и анализ матрицы рисков. Использование: /project-health <Дашборд|риск> [параметры]"
argument-hint: "<dashboard|risk> [options]"
---

# /project-health { #project-health }

Создавайте дашборды состояния портфеля и матрицы рисков для надзора за проектами.

## Использование { #usage }

```
/project-health dashboard <project_data.json>                Portfolio health dashboard
/project-health risk <risk_data.json>                        Risk matrix analysis
```

## Формат ввода { #input-format }

```json
{
  "project_name": "Platform Rewrite",
  "schedule": {"planned_end": "2026-06-30", "projected_end": "2026-07-15", "milestones_hit": 4, "milestones_total": 6},
  "budget": {"allocated": 500000, "spent": 320000, "forecast": 520000},
  "scope": {"features_planned": 40, "features_delivered": 28, "change_requests": 3},
  "quality": {"defect_rate": 0.05, "test_coverage": 0.82},
  "risks": [{"description": "Key engineer leaving", "probability": 0.3, "impact": 0.8}]
}
```

## Примеры { #examples }

```
/project-health dashboard portfolio-q2.json
/project-health risk risk-register.json
/project-health dashboard portfolio-q2.json --format json
```

## Сценарии { #scripts }
- `project-management/skills/senior-pm/scripts/project_health_dashboard.py` — Дашборд работоспособности (`<data_file> [--format text|json]`)
- `project-management/skills/senior-pm/scripts/risk_matrix_analyzer.py` — Анализатор матрицы рисков (`<data_file> [--format text|json]`)

## Ссылка на Скилл { #skill-reference }
> `project-management/skills/senior-pm/SKILL.md`
