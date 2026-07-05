---
title: "Скиллы по продукту — Маршрутизатор { #product-skills--router } — Агентский скилл для продуктовых команд"
description: "Маршрутизатор / индекс для 12 скилл-продуктов, включенных в этот плагин (расстановка приоритетов RICE, OKR, исследование UX, маркеры дизайна, анализ. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Скиллы по продукту — Маршрутизатор { #product-skills--router }

<div class="page-meta" markdown>
<span class="meta-badge">:material-lightbulb-outline: Продукт</span>
<span class="meta-badge">:material-identifier: `product-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install product-skills</code>
</div>


Этот плагин объединяет ** 12 скиллы продукта ** (этот маршрутизатор является 13-й папкой в разделе `product-team/skills/`). Каждый скилл самодостаточен: ознакомьтесь с его `SKILL.md`, запустите его `scripts/`, примените его `references/` и `assets/`.

## Таблица маршрутизации { #routing-table }

Сопоставьте запрос с приведенными ниже сигналами, затем загрузите `product-team/skills/<skill>/SKILL.md`. Если две или более строк совпадают, задайте пользователю один уточняющий вопрос, прежде чем что-либо загружать.

| Сигналы запроса | Скилл | Путь |
|---|---|---|
| Определение приоритетов функций, оценки РАЙСА, обобщение интервью | product-manager-инструментарий | `skills/product-manager-toolkit/` |
| OKR, каскад стратегий, согласование целей | продукт-стратег | `skills/product-strategist/` |
| Персонажи, выводы о юзабилити, обобщение исследований | ux-исследователь-дизайнер | `skills/ux-researcher-designer/` |
| Маркеры дизайна, спецификации компонентов, контраст WCAG | пользовательский интерфейс-дизайн-система | `skills/ui-design-system/` |
| Анализ конкурентов, матрица характеристик/ценообразования | конкурентный срыв | `skills/competitive-teardown/` |
| Удержание, когорты, воронкообразный анализ | продукт-аналитика | `skills/product-analytics/` |
| Дизайн A/B-теста, размер выборки, гейты гипотез | эксперимент-дизайнер | `skills/experiment-designer/` |
| Деревья возможностей, сопоставление предположений, обнаружение | открытие продукта | `skills/product-discovery/` |
| Форматы дорожной карты для каждой аудитории, списки изменений | дорожная карта-коммуникатор | `skills/roadmap-communicator/` |
| Превратите написанную спецификацию в каркас репозитория | от спецификации к репо | `skills/spec-to-repo/` |
| Целевая страница (Next.js TSX + Попутный ветер) | генератор целевых страниц | `skills/landing-page-generator/` |
| Загрузите скелет SaaS-приложения | saas-держатель строительных лесов | `skills/saas-scaffolder/` |

## Быстрый старт { #quick-start }

```bash
# Example: route a prioritization request
cat product-team/skills/product-manager-toolkit/SKILL.md
python3 product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py --help
```

## Сопутствующий продукт-командные плагины (упакованы отдельно, не в этом комплекте) { #related-product-team-plugins-packaged-separately-not-in-this-bundle }

- `product-team/agile-product-owner/` — истории пользователей, пропускная способность спринта
- `product-team/code-to-prd/` — обратный инжиниринг PRD из кодовой базы
- `product-team/apple-hig-expert/` — Аудит Apple HIG (эпоха жидкого стекла)
- `product-team/research-summarizer/` — обобщение документа с извлечением цитат

## Правила { #rules }

- Перейдите точно к одному скиллу, затем следуйте собственному воркфлоу этого скилла.
- Этот маршрутизатор не поставляет собственных инструментов — если ни одна строка не совпадает, скажите об этом и спросите, а не импровизируйте.
