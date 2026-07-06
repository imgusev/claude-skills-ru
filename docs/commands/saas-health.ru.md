---
title: "/saas-health — слэш-команда для ИИ-агентов разработки"
description: "Рассчитайте показатели работоспособности SaaS (ARR, MRR, отток, CAC, LTV, NRR) и сравните их с отраслевыми стандартами. Использование: /saas-health. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /saas-health

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/saas-health.md">Источник</a></span>
</div>


Рассчитайте показатели финансового состояния SaaS на основе исходных данных о бизнесе, сравните их с отраслевыми стандартами и планируйте дальнейшую работу.

## Использование { #usage }

```
/saas-health metrics --mrr <amount> [--customers <n>] [--churned <n>] [--json]
/saas-health quick-ratio --new-mrr <amount> --churned <amount> [--expansion <amount>]
/saas-health simulate --mrr <amount> --growth <pct> --churn <pct> --cac <amount> [--json]
```

## Примеры { #examples }

```
/saas-health metrics --mrr 80000 --customers 200 --churned 3 --new-customers 15 --sm-spend 25000
/saas-health quick-ratio --new-mrr 10000 --expansion 2000 --churned 3000 --contraction 500
/saas-health simulate --mrr 50000 --growth 10 --churn 3 --cac 2000
```

## Сценарии { #scripts }
- `finance/skills/saas-metrics-coach/scripts/metrics_calculator.py` — Основные показатели SaaS (ARR, MRR, отток, CAC, LTV, NRR, окупаемость)
- `finance/skills/saas-metrics-coach/scripts/quick_ratio_calculator.py` — Коэффициент эффективности роста
- `finance/skills/saas-metrics-coach/scripts/unit_economics_simulator.py` — прогноз на 12 месяцев вперед

## Ссылка на Скилл { #skill-reference }
→ `finance/skills/saas-metrics-coach/SKILL.md`

## Связанные команды { #related-commands }
- `/financial-health` — Традиционный финансовый анализ (коэффициенты, DCF, бюджеты)
