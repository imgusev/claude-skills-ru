---
title: "/cs-procurement — слэш-команда для ИИ-агентов разработки"
description: "Категоризация расходов + рационализация поставщиков + анализ цикла закупок. НЕ оценка эффективности работы поставщиков (родственное управление. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-procurement

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/business-operations/commands/cs-procurement.md">Источник</a></span>
</div>


Запустите `procurement-optimizer` скилл на основе этого ввода:

**$АРГУМЕНТЫ**

## Воркфлоу с тремя инструментами { #three-tool-workflow }

1. **`spend_categorizer.py`** — Сопоставление категорий, выровненных по UNSPSC, + анализ по Парето (согласно которому 20% категорий определяют 80% расходов). Отраслевая настройка `--profile {tech-startup,scaleup,enterprise,services,manufacturing}`.

2. **`purchasing_cycle_analyzer.py`** — Время получения заказа, время оплаты, одобрения -количество переходов по категориям. Помечает категории со временем цикла > 2× медиана.

3. **`supplier_consolidation.py`** — Идентифицирует поставщиков с дублирующими функциями (например, 3 инструмента мониторинга, 2 платформы для учета расходов) + план консолидации, сбалансированный с учетом рисков (не проводите консолидацию с одним источником для рисков уровня 1).

## Отличный от { #distinct-from }

- `business-operations/skills/vendor-management` (sibling) — оценка эффективности поставщиков, которым вы продолжаете платить. Оптимизатор закупок - это рационализация расходов + консолидация поставщиков.
- `finance/financial-analysis` — финансовое закрытие + отчетность. Оптимизатор закупок - это поддержка принятия решений, а не отчетность.
