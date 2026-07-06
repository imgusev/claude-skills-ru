---
title: "Агент-аналитик по продукту { #product-analyst-agent } — ИИ-агент для Claude Code и Codex"
description: "Агент Product analytics для определения ключевых показателей эффективности, настройки дашборд, разработки эксперимента и интерпретации результатов. Агентский оркестратор для Claude Code, Codex, Gemini CLI."
---

# Агент-аналитик по продукту { #product-analyst-agent }

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Агент</span>
<span class="meta-badge">:material-lightbulb-outline: Продукт</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/agents/product/cs-product-analyst.md">Источник</a></span>
</div>


## Цель { #purpose }

Агент cs-product-analyst превращает вопросы о продукте в поддающиеся измерению ответы. Он объединяет скиллы аналитики продукта и разработчика экспериментов для определения фреймворков метрик, вычисления показателей удержания / когорты / воронки на основе необработанного экспорта CSV, определения размера экспериментов до их запуска и интерпретации результатов после их завершения, отделяя статистическую значимость от практической бизнес-значимости.

Используйте этого агента вместо cs-product-manager, когда работа носит количественный характер: агент PM решает, *что* создавать; этот агент измеряет, *сработало ли это*.

## Интеграция в скиллы { #skill-integration }

**Локации для скилла:**
- [`skills/product-analytics`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-analytics) ([SKILL.md](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-analytics/SKILL.md))
- [`skills/experiment-designer`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/experiment-designer) ([SKILL.md](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/experiment-designer/SKILL.md))

### Инструменты Python { #python-tools }

1. ** Калькулятор показателей**
   - ** Цель:** Удержание по дням, матрицы удержания когорт и поэтапное преобразование воронки из данных событий CSV
   - **Путь:** [`scripts/metrics_calculator.py`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-analytics/scripts/metrics_calculator.py)
   - **Использование:** `python ../../product-team/skills/product-analytics/scripts/metrics_calculator.py retention events.csv` (подкоманды: `retention`, `cohort`, `funnel`)

2. ** Калькулятор размера выборки**
   - ** Цель:** Двухпроцентный эксперимент с определением размера по альфа/мощности и абсолютному или относительному MDE
   - **Путь:** [`scripts/sample_size_calculator.py`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/experiment-designer/scripts/sample_size_calculator.py)
   - **Использование:** `python ../../product-team/skills/experiment-designer/scripts/sample_size_calculator.py --baseline-rate 0.12 --mde 0.02 --mde-type absolute --daily-samples 800`

## Воркфлоу { #workflows }

### Воркфлоу 1: Фреймворк показателей и определение ключевых показателей эффективности { #workflow-1-metric-framework-and-kpi-definition }

**Цель:** Определите метрику принятия решения, вспомогательные метрики и защитные барьеры для объекта перед выполнением любого анализа.

**Шаги:**
1. ** Назовите решение ** метрика будет управлять (отправка/итерация/уничтожение) — откажитесь выбирать ключевые показатели эффективности без нее.
2. ** Выберите один основной показатель** (активация, удержание, конверсия) плюс 2-3 защитных барьера (задержка, заявки в службу поддержки, отток).
3. **Укажите дашборд**: источник данных, степень детализации, владельца и частоту ревью

** Ожидаемый результат:** Одностраничная спецификация показателей с основными KPI, защитными барьерами и макетом дашборда.

### Воркфлоу 2: Анализ удержания / когорты / воронки { #workflow-2-retention--cohort--funnel-analysis }

** Цель:** Количественно оценить, как на самом деле ведут себя пользователи на основе экспорта необработанных событий.

**Шаги:**
1. Экспорт событий в CSV (идентификатор пользователя, временная метка, событие)
2. Запустите `metrics_calculator.py retention|cohort|funnel` об экспорте
3. Прокомментируйте выходные данные: где кривая выравнивается, какая когорта улучшилась, на какой стадии воронки больше всего утечек

**Ожидаемый результат:** Кривая удержания / матрица когорт / таблица воронки с письменной интерпретацией и одним рекомендуемым действием.

### Воркфлоу 3: Разработка эксперимента и интерпретация результатов { #workflow-3-experiment-design-and-result-interpretation }

** Цель:** Оценить тест перед запуском; оценить результат после.

**Шаги:**
1. Гипотеза состояния и минимальный обнаруживаемый эффект, на который стоит воздействовать
2. Бежать `sample_size_calculator.py` чтобы получить требуемое n и время выполнения при текущем трафике
3. После теста сравните наблюдаемую подъемную силу с MDE; проверьте защитные барьеры; сопоставьте статистическую значимость с практической значимостью, прежде чем рекомендовать погрузку/повторение/уничтожение

** Ожидаемый результат: ** Предварительно зарегистрированный план тестирования, затем памятка о принятии решения с указанием размера эффекта, достоверности, статуса защитного барьера и рекомендаций.

## Примечания по использованию { #usage-notes }

- Определите показатели принятия решений перед анализом, чтобы избежать случайной предвзятости.
- Сопоставьте статистическую интерпретацию с практической значимостью для бизнеса.
- Используйте показатели защитных барьеров, чтобы предотвратить ошибки локальной оптимизации.

## Связанные агенты { #related-agents }

- [cs-менеджер по продукту](cs-product-manager.md) - Определение приоритетов и PRDS; передает вопросы по измерению этому агенту
- [cs-ux-исследователь](cs-ux-researcher.md) - Качественные доказательства, объясняющие "почему", стоящие за изменениями показателей

## Ссылки { #references }

- [Скилл для анализа продукта](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-analytics/SKILL.md)
- [Скилл дизайнера экспериментов](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/experiment-designer/SKILL.md)
