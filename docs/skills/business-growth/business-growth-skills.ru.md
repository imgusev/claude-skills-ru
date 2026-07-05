---
title: "Скиллы для бизнеса и роста — Router { #business--growth-skills--router } — Агентский скилл для роста"
description: "Маршрутизатор/ указатель для 4-х скилл для бизнеса и роста, включенных в этот плагин: менеджер по работе с клиентами (оценка работоспособности, риск. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Скиллы для бизнеса и роста — Router { #business--growth-skills--router }

<div class="page-meta" markdown>
<span class="meta-badge">:material-trending-up: Бизнес и рост</span>
<span class="meta-badge">:material-identifier: `business-growth-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/business-growth/skills/business-growth-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install business-growth-skills</code>
</div>


Этот плагин объединяет ** 4 скилла** (этот маршрутизатор находится в 5-й папке под `business-growth/skills/`). Каждый скилл является самодостаточным.

## Таблица маршрутизации { #routing-table }

Сопоставьте запрос, затем загрузите `business-growth/skills/<skill>/SKILL.md`. Если несколько строк совпадают, сначала задайте один уточняющий вопрос.

| Сигналы запроса | Скилл | Путь |
|---|---|---|
| Показатели здоровья клиентов, риск оттока, возможности расширения | клиент-успешный менеджер | `skills/customer-success-manager/` |
| Охват RFP/RFI, конкурентное позиционирование, планы PoC | инженер по продажам | `skills/sales-engineer/` |
| Охват пайплайна, точность прогноза (MAPE), эффективность GTM | выручка-операции | `skills/revenue-operations/` |
| Предложения, контракты, отчеты о проделанной работе, DPA | составитель контрактов и предложений | `skills/contract-and-proposal-writer/` |

## Быстрый старт { #quick-start }

```bash
# Example: route an account-health request
cat business-growth/skills/customer-success-manager/SKILL.md
python3 business-growth/skills/customer-success-manager/scripts/health_score_calculator.py --help
```

## Правила { #rules }

- Перейдите точно к одному скиллу, затем следуйте воркфлоу этого скилла. Этот маршрутизатор не поставляет никаких собственных инструментов.
- Используйте скиллы Python scorers для показателей, а не для ручных оценок; выходные данные сделки / контракта - это черновики для юридического / коммерческого ревью.
