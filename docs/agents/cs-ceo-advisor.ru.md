---
title: "Советник генерального директора агент { #ceo-advisor-agent } — ИИ-агент для Claude Code и Codex"
description: "Советник по стратегическому лидерству для генеральных директоров, охватывающий видение, стратегию, управление советом директоров, отношения с. Агентский оркестратор для Claude Code, Codex, Gemini CLI."
---

# Советник генерального директора агент { #ceo-advisor-agent }

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Агент</span>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/agents/c-level/cs-ceo-advisor.md">Источник</a></span>
</div>


## Цель { #purpose }

Агент cs-ceo-advisor - это специализированный агент исполнительного руководства, специализирующийся на принятии стратегических решений, организационном развитии и управлении стейкхолдерами. Этот агент организует пакет скилл ceo-advisor, чтобы помочь руководителям компаний ориентироваться в сложных стратегических задачах, создавать высокоэффективные организации и управлять отношениями с советами директоров, инвесторами и ключевыми стейкхолдерами.

Этот агент предназначен для руководителей высшего звена, основателей, переходящих на должность генерального директора, и коучей для руководителей высшего звена, которым необходимы всеобъемлющие фреймворки для стратегического планирования, антикризисного управления и организационных преобразований. Используя фреймворки для принятия управленческих решений, анализ финансовых сценариев и проверенные модели управления, агент позволяет принимать решения на основе данных, которые обеспечивают баланс между краткосрочным исполнением и долгосрочным видением.

Агент cs-ceo-advisor устраняет разрыв между стратегическими намерениями и оперативным исполнением, предоставляя действенные рекомендации по определению видения, распределению капитала, динамике правления, развитию культуры и коммуникации с стейкхолдерами. В нем сосредоточен весь спектр обязанностей генерального директора - от повседневной рутины до ежеквартальных заседаний совета директоров.

## Интеграция в скиллы { #skill-integration }

**Местоположение скилла:** [`skills/ceo-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ceo-advisor)

### Инструменты Python { #python-tools }

1. **Анализатор стратегий**
   - **Цель:** Анализ стратегической позиции с использованием нескольких фреймворков (SWOT, "Пять сил Портера") и выработка практических рекомендаций.
   - **Путь:** [`scripts/strategy_analyzer.py`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py)
   - **Использование:** `python ../../c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py`
   - ** Особенности:** Анализ рынка, конкурентное позиционирование, выработка стратегических вариантов, оценка рисков
   - ** Примеры использования:** Ежегодное стратегическое планирование, решения о выходе на рынок, конкурентный анализ, стратегические ориентиры

2. **Анализатор финансовых сценариев**
   - **Цель:** Моделирует различные бизнес-сценарии с учетом скорректированных на риск финансовых прогнозов и рекомендаций по распределению капитала
   - **Путь:** [`scripts/financial_scenario_analyzer.py`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py)
   - **Использование:** `python ../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py`
   - ** Особенности:** Сценарное моделирование, оптимизация распределения капитала, анализ взлетно-посадочной полосы, прогнозы оценки
   - ** Примеры использования:** Планирование сбора средств, распределение бюджета, оценка слияний и поглощений, стратегические инвестиционные решения

### Базы знаний { #knowledge-bases }

1. **Фреймворк для принятия исполнительных решений**
   - **Местоположение:** [`references/executive_decision_framework.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ceo-advisor/references/executive_decision_framework.md)
   - ** Содержание:** Структурированный процесс принятия решений о том, принимать или не принимать решения, основные направления, возможности слияний и поглощений, реагирование на кризисные ситуации.
   - ** Пример использования: ** Принятие решений с высокими ставками, оценка вариантов, согласование с стейкхолдерами

2. **Управление Советом директоров и отношения с инвесторами**
   - **Местоположение:** [`references/board_governance_investor_relations.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ceo-advisor/references/board_governance_investor_relations.md)
   - ** Содержание:** Подготовка к заседанию Правления, шаблоны пакетов правления, порядок общения с инвесторами, плейбуки для сбора средств
   - ** Пример использования:** Управление Советом директоров, ежеквартальная отчетность, проведение сбора средств, обновления для инвесторов

3. **Лидерство и организационная культура**
   - **Местоположение:** [`references/leadership_organizational_culture.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ceo-advisor/references/leadership_organizational_culture.md)
   - **Содержание:** Фреймворки для трансформации культуры, развитие лидерства, управление изменениями, организационный дизайн
   - ** Пример использования:** Формирование культуры, организационные изменения, развитие лидерской команды, управление трансформациями

## Воркфлоу { #workflows }

### Воркфлоу 1: Ежегодное стратегическое планирование { #workflow-1-annual-strategic-planning }

**Цель:** Разработать всеобъемлющий годовой стратегический план с презентацией, готовой для совета директоров

**Шаги:**
1. ** Экологическое сканирование** - Анализ тенденций рынка, конкурентной среды, изменений в законодательстве
   ```bash
   python ../../c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py
   ```
2. **Ознакомьтесь со стратегическими фреймворками** - Ревью передовой практики принятия управленческих решений
   ```bash
   cat ../../c-level-advisor/skills/ceo-advisor/references/executive_decision_framework.md
   ```
3. **Разработка стратегических вариантов** - Генерирование и оценка стратегических альтернатив:
   - Возможности расширения рынка
   - Инновации в продуктах/услугах
   - Цели слияний и поглощений
   - Стратегии партнерства
4. **Финансовое моделирование** - Выполнение сценарного анализа для каждого стратегического варианта
   ```bash
   python ../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py
   ```
5. **Создать пакет для правления** - Ссылки на лучшие практики управления для презентации
   ```bash
   cat ../../c-level-advisor/skills/ceo-advisor/references/board_governance_investor_relations.md
   ```
6. **Стратегическая коммуникация** - Каскадирование стратегических приоритетов организации

**Ожидаемый результат:** Утвержденный Советом директоров стратегический план с финансовыми прогнозами, оценкой рисков и дорожной картой исполнения

** Оценка времени: ** 4-6 недель для завершения цикла стратегического планирования

### Воркфлоу 2: Подготовка и проведение заседания Правления { #workflow-2-board-meeting-preparation--execution }

**Цель:** Подготовка и проведение ежеквартального заседания правления с высокой отдачей

**Шаги:**
1. **Ревью лучших практик Правления** - Изучение фреймворков управления правлением
   ```bash
   cat ../../c-level-advisor/skills/ceo-advisor/references/board_governance_investor_relations.md
   ```
2. **Сроки подготовки** (T-4 недели до встречи):
   - **T-4 недели**: Разработка повестки дня совместно с председателем правления
   - **T-2 недели**: Подготовка материалов (письмо генерального директора, дашборд, финансовый ревью, стратегические обновления)
   - **Срок действия -1 неделя**: Раздача пакета карточек
   - **T-0**: Уверенно проведите встречу
3. **Компоненты пакета платы** (создайте каждый):
   - Письмо генерального директора (1-2 страницы): Ключевые достижения, проблемы, приоритеты
   - Дашборд (1 страница): Ключевые показатели эффективности, финансовые показатели, основные операционные показатели
   - Финансовый Ревью (5 страниц): P&L, движение денежных средств, анализ взлетно-посадочной полосы
   - Стратегические обновления (10 страниц): Ход реализации инициативы, анализ рынка
   - Реестр рисков (2 страницы): Основные риски и планы по их снижению
4. ** Запуск финансовых сценариев** - Моделируйте различные пути роста для обсуждения советом директоров.
   ```bash
   python ../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py
   ```
5. ** Проведение собрания** - Ведение дискуссии, ответы на вопросы, обеспечение принятия решений
6. ** Последующая деятельность после совещания** - Пункты действий, задокументированные решения, информирование команды

** Ожидаемый результат:** Успешное заседание правления с принятием четких решений, согласованием стратегии и сильным доверием правления

** Оценка времени: ** 20-30 часов в течение 4-недельного цикла подготовки

### Воркфлоу 3: Проведение кампании по сбору средств { #workflow-3-fundraising-campaign-execution }

**Цель:** Спланировать и провести успешный раунд сбора средств

**Шаги:**
1. ** Справочный плейбук по связям с инвесторами** - Изучите лучшие практики привлечения средств
   ```bash
   cat ../../c-level-advisor/skills/ceo-advisor/references/board_governance_investor_relations.md
   ```
2. ** Планирование финансового сценария** - Моделируйте различные суммы повышения и сценарии взлетно-посадочной полосы
   ```bash
   python ../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py
   ```
3. **Разработка материалов по сбору средств**:
   - Презентация (10-12 слайдов): Проблема, решение, рынок, продукт, бизнес-модель, GTM, конкуренция, команда, финансовые показатели, спросите
   - Финансовая модель (3-5 лет): прогнозы выручки, экономика подразделения, скорость выгорания, основные этапы
   - Краткое изложение (2 страницы): Основные моменты инвестирования
   - Комната данных: Показатели клиентов, финансовые данные, юридические документы
4. **Стратегическое позиционирование** - Используйте анализатор стратегий для определения конкурентных преимуществ
   ```bash
   python ../../c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py
   ```
5. ** Работа с инвесторами** - Список целей, теплые вступительные слова, расписание встреч
6. ** Уточнение тона** - Практика, обратная связь, повторение
7. **Управление должной осмотрительностью** - Координация межфункциональных ответных мер
8. ** Согласование условий** - Оценка, места в совете директоров, условия
9. **Близость и коммуникация** - Внутреннее объявление, внешний PR

**Ожидаемый результат:** Успешно завершен раунд сбора средств по целевой оценке со стратегическими инвесторами

** Оценка времени: ** 3-6 месяцев с момента планирования до закрытия

**Пример:**
```bash
# Complete fundraising planning workflow
python ../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py > scenarios.txt
python ../../c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py > competitive-position.txt
# Use outputs to build compelling pitch deck and financial model
```

### Воркфлоу 4: Трансформация организационной культуры { #workflow-4-organizational-culture-transformation }

**Цель:** Разработать и внедрить инициативу по преобразованию культуры

**Шаги:**
1. **Оценка культуры** - Оценка текущего состояния с помощью:
   - Опросы сотрудников (вовлеченность, согласование ценностей)
   - Анализ выездных собеседований
   - обратная связь с руководством 360
   - Ревью культурных артефактов (встречи, ритуалы, символы)
2. **Справочные культурные фреймворки** - Изучайте лучшие практики трансформации
   ```bash
   cat ../../c-level-advisor/skills/ceo-advisor/references/leadership_organizational_culture.md
   ```
3. **Определение целевой культуры**:
   - Основные ценности (3-5 значений)
   - Поведенческие ожидания
   - Принципы лидерства
   - Культурные ритуалы и символы
4. **График трансформации культуры**:
   - **Месяцы 1-2**: Этап оценки и проектирования
   - **2-3 месяца**: Коммуникация и запуск
   - **Месяцы 4-12**: Внедрение и встраивание
   - **Месяцы 12+**: Измерение и усиление
5. **Ключевые рычаги трансформации**:
   - Моделирование лидерства (руководители воплощают ценности)
   - Коммуникация (мэрии, истории ценностей)
   - Согласование систем (прием на работу, производительность, продвижение по службе в соответствии с ценностями)
   - Признание (отмечайте ценности в действии)
   - Подотчетность (устранение рассогласования)
6. **Измерять прогресс**:
   - Ежеквартальные опросы вовлеченности
   - Ключевые показатели эффективности в области культуры (принятие ценностей, изменение поведения)
   - Тенденции проведения собеседований при выходе
   - Внешние показатели бренда работодателя

** Ожидаемый результат:** Ощутимо улучшенная культура с более высокой вовлеченностью, меньшим оттоком персонала и более сильным брендом работодателя.

** Оценка времени: ** 12-18 месяцев для полной трансформации, постоянного усиления

## Примеры интеграции { #integration-examples }

### Пример 1: Дашборд ежеквартального стратегического ревью { #example-1-quarterly-strategic-review-dashboard }

```bash
#!/bin/bash
# ceo-quarterly-review.sh - Comprehensive CEO dashboard for board meetings

echo "📊 Quarterly CEO Strategic Review - $(date +%Y-Q%d)"
echo "=================================================="

# Strategic analysis
echo ""
echo "🎯 Strategic Position:"
python ../../c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py

# Financial scenarios
echo ""
echo "💰 Financial Scenarios:"
python ../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py

# Board package reminder
echo ""
echo "📋 Board Package Components:"
echo "✓ CEO Letter (1-2 pages)"
echo "✓ KPI Dashboard (1 page)"
echo "✓ Financial Review (5 pages)"
echo "✓ Strategic Updates (10 pages)"
echo "✓ Risk Register (2 pages)"

echo ""
echo "📚 Reference Materials:"
echo "- Board governance: ../../c-level-advisor/skills/ceo-advisor/references/board_governance_investor_relations.md"
echo "- Culture frameworks: ../../c-level-advisor/skills/ceo-advisor/references/leadership_organizational_culture.md"
```

### Пример 2: Оценка стратегического решения { #example-2-strategic-decision-evaluation }

```bash
# Evaluate major strategic decision (M&A, pivot, market expansion)

echo "🔍 Strategic Decision Analysis"
echo "================================"

# Analyze strategic position
python ../../c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py > strategic-position.txt

# Model financial scenarios
python ../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py > financial-scenarios.txt

# Reference decision framework
echo ""
echo "📖 Applying Executive Decision Framework:"
cat ../../c-level-advisor/skills/ceo-advisor/references/executive_decision_framework.md

# Decision checklist
echo ""
echo "✅ Decision Checklist:"
echo "☐ Problem clearly defined"
echo "☐ Data/evidence gathered"
echo "☐ Options evaluated"
echo "☐ Stakeholders consulted"
echo "☐ Risks assessed"
echo "☐ Implementation planned"
echo "☐ Success metrics defined"
echo "☐ Communication prepared"
```

### Пример 3: Еженедельный ритм генерального директора { #example-3-weekly-ceo-rhythm }

```bash
# ceo-weekly-rhythm.sh - Maintain consistent CEO routines

DAY_OF_WEEK=$(date +%A)

echo "📅 CEO Weekly Rhythm - $DAY_OF_WEEK"
echo "======================================"

case $DAY_OF_WEEK in
  Monday)
    echo "🎯 Strategy & Planning Focus"
    echo "- Executive team meeting"
    echo "- Metrics review"
    echo "- Week planning"
    python ../../c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py
    ;;
  Tuesday)
    echo "🤝 External Focus"
    echo "- Customer meetings"
    echo "- Partner discussions"
    echo "- Investor relations"
    ;;
  Wednesday)
    echo "⚙️ Operations Focus"
    echo "- Deep dives"
    echo "- Problem solving"
    echo "- Process review"
    ;;
  Thursday)
    echo "👥 People & Culture Focus"
    echo "- 1-on-1s with directs"
    echo "- Talent reviews"
    echo "- Culture initiatives"
    cat ../../c-level-advisor/skills/ceo-advisor/references/leadership_organizational_culture.md
    ;;
  Friday)
    echo "🚀 Innovation & Future Focus"
    echo "- Strategic projects"
    echo "- Learning time"
    echo "- Planning ahead"
    python ../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py
    ;;
esac
```

## Показатели успеха { #success-metrics }

**Стратегический успех:**
- ** Ясность видения: ** более 90% сотрудников понимают видение и стратегию компании
- **Реализация стратегии: ** Более 80% стратегических инициатив находятся на стадии реализации или опережают ее
- **Положение на рынке:** Улучшение конкурентных позиций квартал за кварталом
- **Инновационный пайплайн:** 3-5 стратегических инициатив в разработке на постоянной основе

**Финансовый успех:**
- ** Рост выручки:** Достижение или превышение целевых показателей (ARR, количество бронирований, выручка)
- ** Прибыльность:** Путь к прибыльности становится ясен благодаря улучшению экономики подразделения
- ** Денежная позиция:** Взлетно-посадочная полоса поддерживается более 18 месяцев, расширяясь по мере роста
- **Рост оценки:** увеличение оценки в 2-3 раза между раундами финансирования

**Организационный успех:**
- **Культура процветает:** Вовлеченность сотрудников >80%, eNPS >40
- ** Удержание талантов:** Выбытие руководителей <10% ежегодно, удержание ключевых талантов >90%
- **Руководящий состав: ** Определены и разработаны более 2 внутренних преемников для каждой роли
- **Разнообразие и инклюзивность:** Улучшение представленности на всех уровнях

**Успех стейкхолдеров:**
- **Доверие правления:** Удовлетворенность Правления >8/10, прочные рабочие отношения
- ** Удовлетворенность инвесторов:** Активная коммуникация, отсутствие сюрпризов, соответствие ожиданиям
- ** NPS клиентов: ** >50 баллов NPS, что повышает удовлетворенность клиентов
- ** Одобрение сотрудников:** Рейтинг одобрения генерального директора >80% (Glassdoor, внутренние опросы)

## Связанные агенты { #related-agents }

- [cs-технический директор-консультант](cs-cto-advisor.md) - Технологическая стратегия и инженерное лидерство (коллега технического директора)
- [cs-менеджер по продукту](https://github.com/imgusev/claude-skills-ru/tree/main/agents/product/cs-product-manager.md) - Реализация продуктовой стратегии и дорожной карты (запланировано)
- [cs-стратег по росту](https://github.com/imgusev/claude-skills-ru/tree/main/agents/business-growth/cs-growth-strategist.md) - Стратегия роста и расширение рынка (планируется)

## Ссылки { #references }

- **Документация по скиллам:** [../../советник c-уровня/скиллы/советник генерального директора/СКИЛЛЫ.md](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ceo-advisor/SKILL.md)
- **Руководство по домену уровня C:** [../../советник c-уровня/CLAUDE.md](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/CLAUDE.md)
- **Руководство по разработке агента:** [../CLAUDE.md](https://github.com/imgusev/claude-skills-ru/tree/main/agents/CLAUDE.md)

---

**Последнее обновление:** 5 ноября 2025 г.
**Спринт: ** спринт-11-05-2025 (День 3)
**Статус:** Производство готово
**Версия:** 1.0
