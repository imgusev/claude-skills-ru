---
name: tech-debt
description: "Сканируйте, расставляйте приоритеты и сообщайте о технической задолженности. Использование: /tech-debt <сканирование|определение приоритетов|отчет> [параметры]"
argument-hint: "<scan|prioritize|report> [options]"
---

# /технический долг { #tech-debt }

Сканируйте кодовые базы на предмет технических неисправностей, оценивайте степень серьезности и создавайте приоритетные планы устранения неполадок.

## Использование { #usage }

```
/tech-debt scan <project-dir>           Scan for debt indicators
/tech-debt prioritize <inventory.json>  Prioritize debt backlog
/tech-debt report <project-dir>         Full dashboard with trends
```

## Примеры { #examples }

```
/tech-debt scan ./src
/tech-debt scan . --format json
/tech-debt report . --format json --output debt-report.json
```

## Сценарии { #scripts }
- `engineering/skills/tech-debt-tracker/scripts/debt_scanner.py` — Сканирование на предмет структуры задолженности (`debt_scanner.py <directory> [--format json] [--output file]`)
- `engineering/skills/tech-debt-tracker/scripts/debt_prioritizer.py` — Определить приоритетность накопившейся задолженности (`debt_prioritizer.py <inventory.json> [--framework cost_of_delay|wsjf|rice] [--format json]`)
- `engineering/skills/tech-debt-tracker/scripts/debt_dashboard.py` — Генерировать долговую дашборд (`debt_dashboard.py [files...] [--input-dir dir] [--period weekly|monthly|quarterly] [--format json]`)

## Ссылка на Скилл { #skill-reference }
→ `engineering/skills/tech-debt-tracker/SKILL.md`
