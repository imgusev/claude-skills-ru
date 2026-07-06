---
name: financial-health
description: "Выполните анализ финансовых коэффициентов, оценку DCF, анализ отклонений бюджета и скользящие прогнозы. Использование: /financial-health <коэффициенты|dcf|бюджет|прогноз> <data.json>"
argument-hint: "<ratios|dcf|budget|forecast> <data.json>"
---

# /финансовое здоровье { #financial-health }

Анализируйте финансовую отчетность, стройте модели оценки, оценивайте отклонения в бюджете и составляйте прогнозы.

## Использование { #usage }

```
/financial-health ratios <financial_data.json> [--format json|text]
/financial-health dcf <valuation_data.json> [--format json|text]
/financial-health budget <budget_data.json> [--format json|text]
/financial-health forecast <forecast_data.json> [--format json|text]
```

## Примеры { #examples }

```
/financial-health ratios quarterly_financials.json --format json
/financial-health dcf acme_valuation.json
/financial-health budget q1_budget.json --format json
/financial-health forecast revenue_history.json
```

## Сценарии { #scripts }
- `finance/skills/financial-analyst/scripts/ratio_calculator.py` — Прибыльность, ликвидность, кредитное плечо, эффективность, оценочные коэффициенты
- `finance/skills/financial-analyst/scripts/dcf_valuation.py` — Оценка предприятия и собственного капитала DCF с анализом чувствительности
- `finance/skills/financial-analyst/scripts/budget_variance_analyzer.py` — Анализ фактических отклонений от бюджета по сравнению с предыдущим годом
- `finance/skills/financial-analyst/scripts/forecast_builder.py` — Прогнозирование доходов на основе драйверов с использованием сценарного моделирования

## Ссылка на Скилл { #skill-reference }
→ `finance/skills/financial-analyst/SKILL.md`

## Связанные команды { #related-commands }
- `/saas-health` — Показатели, специфичные для SaaS (ARR, MRR, отток, CAC, LTV, быстрый коэффициент)
