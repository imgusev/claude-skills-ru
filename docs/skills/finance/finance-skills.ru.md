---
title: "Финансовые Скиллы — Маршрутизатор { #finance-skills--router } — Агентский скилл для финансов"
description: "Маршрутизатор / индекс для 2-х финансовых скилл, включенных в этот плагин: финансовый аналитик (анализ коэффициентов, оценка DCF, отклонение бюджета. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Финансовые Скиллы — Маршрутизатор { #finance-skills--router }

<div class="page-meta" markdown>
<span class="meta-badge">:material-calculator-variant: Финансы</span>
<span class="meta-badge">:material-identifier: `finance-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/finance/skills/finance-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install finance-skills</code>
</div>


Этот плагин объединяет ** 2 финансовых скилла** (этот маршрутизатор находится в 3-й папке под `finance/skills/`). Каждый скилл является самодостаточным.

## Таблица маршрутизации { #routing-table }

| Сигналы запроса | Скилл | Путь |
|---|---|---|
| Анализ коэффициентов, оценка DCF, отклонение бюджета, прогнозы на основе факторов | финансовый аналитик | `skills/financial-analyst/` |
| ARR/MRR, отток, CAC/LTV, NRR, быстрое соотношение, тесты SaaS | saas-метрики-тренер | `skills/saas-metrics-coach/` |

Если оба варианта совпадают (например, "цените мою SaaS-компанию"), спросите, хочет ли пользователь провести анализ на уровне отчетности (financial-analyst) или операционные показатели SaaS (saas-metrics-coach).

## Быстрый старт { #quick-start }

```bash
# Example: route a statement-analysis request
cat finance/skills/financial-analyst/SKILL.md
python3 finance/skills/financial-analyst/scripts/ratio_calculator.py --help

# Or a SaaS metrics request
python3 finance/skills/saas-metrics-coach/scripts/metrics_calculator.py --help
```

## Связанный (упакован отдельно, не в этом комплекте) { #related-packaged-separately-not-in-this-bundle }

- `finance/business-investment-advisor/` — оценка инвестиционных тезисов, моделирование рентабельности инвестиций (скилл только для промптов, отдельный вложенный плагин)
- Корневые команды `/financial-health` и `/saas-health` оберните эти скрипты скиллами.

## Правила { #rules }

- Перейдите точно к одному скиллу, затем следуйте воркфлоу этого скилла. Этот маршрутизатор не поставляет никаких собственных инструментов.
- Всегда сверяйте финансовые результаты с исходными данными пользователя; результаты - это аналитическая поддержка, а не инвестиционный совет.
