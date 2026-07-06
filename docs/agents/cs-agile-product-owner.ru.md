---
title: "Гибкий агент-владелец продукта { #agile-product-owner-agent } — ИИ-агент для Claude Code и Codex"
description: "Гибкий агент владельца продукта для эпической разбивки, планирования спринта, уточнения бэклога и создания пользовательских историй, соответствующих. Агентский оркестратор для Claude Code, Codex, Gemini CLI."
---

# Гибкий агент-владелец продукта { #agile-product-owner-agent }

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Агент</span>
<span class="meta-badge">:material-lightbulb-outline: Продукт</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/agents/product/cs-agile-product-owner.md">Источник</a></span>
</div>


## Цель { #purpose }

Агент cs-agile-product-owner - это специализированный агент владения гибким продуктом, специализирующийся на управлении бэклогом, планировании спринта, создании пользовательских историй и эпической декомпозиции. Этот агент использует скиллы agile-владельца продукта наряду с инструментарием менеджера продукта, чтобы обеспечить хорошую структуру незавершенного производства, правильную расстановку приоритетов и соответствие бизнес-целям.

Этот агент предназначен для владельцев продуктов, scrum-мастеров, носящих шляпу PO, и руководителей гибких команд, которым нужны структурированные процессы для разбивки epic на конечные пользовательские истории, проведения эффективных сессий планирования спринта и поддержания здорового списка невыполненных работ по продукту. Сочетая генерацию историй на основе Python с расстановкой приоритетов RICE, агент гарантирует, что незавершенные работы являются стратегически обоснованными и готовыми к исполнению.

Агент cs-agile-product-owner объединяет стратегические цели продукта с выполнением на уровне спринта, предоставляя фреймворки для преобразования элементов дорожной карты в четко определенные, соответствующие инвестициям пользовательские истории с четкими критериями приемлемости. Это лучше всего работает в тандеме с мастерами scrum, которые обеспечивают контекст velocity, и инженерными командами, которые проверяют техническую осуществимость.

## Интеграция в скиллы { #skill-integration }

**Основной скилл:** [`product-team/agile-product-owner`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/agile-product-owner)

### Все организованные скиллы { #all-orchestrated-skills }

| # | Скилл | Местоположение | Основной инструмент |
|---|-------|----------|-------------|
| 1 | Гибкий владелец продукта | [`product-team/agile-product-owner`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/agile-product-owner) | user_story_generator.py |
| 2 | Инструментарий менеджера по продукту | [`skills/product-manager-toolkit`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-manager-toolkit) | rice_prioritizer.py |

### Инструменты Python { #python-tools }

1. ** Генератор пользовательских историй**
   - ** Цель:** Разбить epics на пользовательские истории, соответствующие требованиям INVEST, с критериями приемлемости в формате Given/When/Then
   - **Путь:** [`scripts/user_story_generator.py`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py)
   - **Использование:** `python ../../product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py epic.yaml`
   - ** Особенности: ** Эпическая декомпозиция, генерация критериев приемлемости, оценка сюжетных точек, отображение зависимостей
   - ** Примеры использования:** Планирование спринта, доработка бэклога, семинары по написанию историй.

2. **Приоритетность РИСА**
   - **Цель:** фреймворк RICE для определения приоритетов невыполненных работ с помощью анализа портфеля
   - **Путь:** [`scripts/rice_prioritizer.py`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py)
   - **Использование:** `python ../../product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py backlog.csv --capacity 20`
   - ** Особенности:** Анализ квадрантов портфеля, планирование производственных мощностей, составление ежеквартальной дорожной карты
   - ** Варианты использования:** Упорядочение невыполненных работ, принятие решений о масштабах спринта, согласование с стейкхолдерами

### Базы знаний { #knowledge-bases }

1. **Руководство по планированию спринта**
   - **Местоположение:** [`references/sprint-planning-guide.md`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/agile-product-owner/skills/agile-product-owner/references/sprint-planning-guide.md)
   - ** Содержание:** Церемонии планирования спринта, отслеживание скорости, распределение мощностей, постановка целей спринта
   - ** Пример использования:** Упрощение планирования спринта, управление производительностью

2. **Шаблоны пользовательских историй**
   - **Местоположение:** [`references/user-story-templates.md`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/agile-product-owner/skills/agile-product-owner/references/user-story-templates.md)
   - ** Содержание:** Форматы историй, соответствующие требованиям ИНВЕСТОРОВ, шаблоны критериев приемлемости, методы разделения историй
   - ** Пример использования: ** Написание истории, обработка невыполненных работ, определение "сделано".

3. **Шаблоны PRD**
   - **Местоположение:** [`references/prd_templates.md`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-manager-toolkit/references/prd_templates.md)
   - **Содержание:** Форматы документов с требованиями к продукту для различных уровней сложности
   - ** Пример использования:** Документация Epic, спецификация функций

### Шаблоны { #templates }

1. **Шаблон планирования спринта**
   - **Местоположение:** [`assets/sprint_planning_template.md`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/agile-product-owner/skills/agile-product-owner/assets/sprint_planning_template.md)
   - ** Пример использования: ** Сеансы планирования спринта, отслеживание пропускной способности, документирование целей спринта

2. **Шаблон истории пользователя**
   - **Местоположение:** [`assets/user_story_template.md`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/agile-product-owner/skills/agile-product-owner/assets/user_story_template.md)
   - ** Пример использования:** Согласованный формат истории, структура критериев приемлемости

3. **шаблон для ввода РИСА**
   - **Местоположение:** [`assets/rice_input_template.csv`](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-manager-toolkit/assets/rice_input_template.csv)
   - ** Пример использования:** Структурирование элементов невыполненной работы для определения приоритетов РИСА

## Воркфлоу { #workflows }

### Воркфлоу 1: Эпическая поломка { #workflow-1-epic-breakdown }

** Цель:** Разложить большой epic на готовые к спринту пользовательские истории с критериями приемлемости

**Шаги:**
1. **Определите эпопею** - Задокументируйте эпопею с четким охватом:
   - Бизнес-цель и ценность для пользователей
   - Персоны целевого пользователя (ов)
   - Критерии приемлемости высокого уровня
   - Известные ограничения и зависимости

2. **Создайте Epic YAML** - Структурируйте epic для генератора историй:
   ```yaml
   epic:
     title: "User Dashboard"
     description: "Comprehensive dashboard for user activity and metrics"
     personas: ["admin", "standard-user"]
     features:
       - "Activity feed"
       - "Usage metrics"
       - "Settings panel"
   ```

3. **Генерировать истории** - Запустить генератор пользовательских историй:
   ```bash
   python ../../product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py epic.yaml
   ```

4. ** Ревью и доработка ** - Для каждой сгенерированной истории:
   - Подтверждение соответствия ИНВЕСТИЦИЙ (Независимое, подлежащее обсуждению, ценное, оцениваемое, небольшое, проверяемое)
   - Уточнить критерии приемлемости (заданный формат/Когда/затем)
   - Выявлять зависимости между историями
   - Оценивайте сюжетные моменты вместе с командой

5. **Закажите Бэклог** - Последовательность историй для доставки:
   - Обязательные истории в первую очередь (MVP)
   - Группировать по цепочке зависимостей
   - Сбалансируйте техническую работу и работу, ориентированную на пользователя

** Ожидаемый результат: ** 8-15 четко определенных пользовательских историй для каждой эпопеи с критериями приемлемости, сюжетными точками и картой зависимостей

** Оценка времени: ** 2-4 часа на эпопею

**Пример:**
```bash
# Create epic definition
cat > dashboard-epic.yaml << 'EOF'
epic:
  title: "User Dashboard"
  description: "Real-time dashboard showing user activity, key metrics, and account settings"
  personas: ["admin", "standard-user"]
  features:
    - "Real-time activity feed"
    - "Key metrics display with charts"
    - "Quick settings access"
    - "Notification preferences"
EOF

# Generate user stories
python ../../product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py dashboard-epic.yaml

# Review the sprint planning guide for context
cat ../../product-team/agile-product-owner/skills/agile-product-owner/references/sprint-planning-guide.md
```

### Воркфлоу 2: Планирование спринта { #workflow-2-sprint-planning }

**Цель:** Спланируйте спринт с четкими целями, выбранными историями и выявленными рисками

**Шаги:**
1. **Рассчитать вместимость** - Определить доступность команды:
   - Перечислите членов команды и доступные дни
   - Учет ВОМ, дежурств, тренингов, встреч
   - Рассчитать общее количество человеко-дней
   - Исходная историческая скорость (среднее значение за последние 3 спринта)

2. ** Ревью невыполненной работы ** - Убедитесь, что истории готовы:
   - Проверьте определение готовности для лучших кандидатов
   - Убедитесь, что критерии приемлемости выполнены
   - Подтвердите техническую осуществимость с инженерами
   - Определите любые блокирующие зависимости

3. ** Установите цель спринта** - Определите одну четкую, измеримую цель:
   - Приведено в соответствие с ежеквартальными OKR
   - Достижимо в рамках возможностей спринта
   - Ценный для пользователей или бизнеса

4. ** Выберите истории** - Извлеките из приоритетного списка невыполненных работ:
   ```bash
   # Prioritize candidates if not already ordered
   python ../../product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py sprint-candidates.csv --capacity 12
   ```

5. **Задокументируйте план** - Используйте шаблон планирования спринта:
   ```bash
   cat ../../product-team/agile-product-owner/skills/agile-product-owner/assets/sprint_planning_template.md
   ```

6. **Выявлять риски** - Документировать потенциальные препятствия:
   - Внешние зависимости
   - Технические неизвестные
   - Изменения в доступности команды
   - Планы смягчения последствий для каждого риска

** Ожидаемый результат: ** Документ плана спринта с указанием цели, выбранных историй (в пределах скорости), распределения мощностей, зависимостей и рисков.

** Оценка времени: ** 2-3 часа на сеанс планирования спринта

**Пример:**
```bash
# Prepare sprint candidates
cat > sprint-candidates.csv << 'EOF'
feature,reach,impact,confidence,effort
User Dashboard - Activity Feed,500,3,0.8,3
User Dashboard - Metrics Charts,500,2,0.9,5
Notification Preferences,300,1,1.0,2
Password Reset Flow Fix,1000,2,1.0,1
EOF

# Run prioritization
python ../../product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py sprint-candidates.csv --capacity 8

# Reference sprint planning template
cat ../../product-team/agile-product-owner/skills/agile-product-owner/assets/sprint_planning_template.md
```

### Воркфлоу 3: Уточнение невыполненной работы { #workflow-3-backlog-refinement }

** Цель:** Поддерживать здоровое отставание с помощью правильно подобранных, расставленных по приоритетам и четко определенных историй.

**Шаги:**
1. **Сортировка новых товаров** - Обработка входящих запросов:
   - Элементы обратной связи с клиентами
   - Сообщения об ошибках
   - Квитанции о техническом долге
   - Запросы на новые функции от стейкхолдеров

2. ** Размер и оценка ** - Применяйте сюжетные точки:
   - Используйте для планирования покера или подбора размера футболки
   - Рекомендации по оценке справочной группы
   - Разделенные истории размером более 13 сюжетных точек
   - Применяйте методы разделения историй на основе ссылок

3. ** Расставьте приоритеты с помощью РИСА ** - Подсчитайте количество невыполненных заданий:
   ```bash
   python ../../product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py backlog.csv
   ```

4. ** Уточните лучшие элементы ** - Убедитесь, что готовы 2 лучших спринта стоимостью:
   - Полные критерии приемлемости
   - Решайте открытые вопросы с стейкхолдерами
   - Добавьте технические примечания и рекомендации по внедрению
   - Проверьте наличие дизайнов (если применимо)

5. **Заархивировать или удалить** - Очистить накопившуюся информацию:
   - Закрывайте элементы старше 6 месяцев, которые не использовались
   - Объединять повторяющиеся истории
   - Удалять элементы, которые больше не соответствуют стратегии

** Ожидаемый результат: ** Уточненный список невыполненных работ с 20 лучшими историями, полностью определенными, оцененными и упорядоченными

** Ориентировочное время: ** 1-2 часа на еженедельный сеанс уточнения

**Пример:**
```bash
# Export backlog for prioritization
cat > backlog-q2.csv << 'EOF'
feature,reach,impact,confidence,effort
Search Improvement,800,3,0.8,5
Mobile Responsive Tables,600,2,0.7,3
API Rate Limiting,400,2,0.9,2
Onboarding Wizard,1000,3,0.6,8
Export to PDF,200,1,1.0,1
Dark Mode,300,1,0.8,3
EOF

# Run full prioritization with capacity
python ../../product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py backlog-q2.csv --capacity 15

# Review user story templates for refinement
cat ../../product-team/agile-product-owner/skills/agile-product-owner/references/user-story-templates.md
```

### Воркфлоу 4: Мастер-класс по написанию рассказа { #workflow-4-story-writing-workshop }

** Цель:** Совместно с командой создавать высококачественные пользовательские истории

**Шаги:**
1. **Подготовьте сессию** - Соберите материалы:
   - Эпическое или художественное описание
   - Задействованные персонажи-пользователи
   - Создавайте макеты или каркасы
   - Технические ограничения

2. ** Идентификация персонажей пользователей ** - Сопоставление историй с персонажами:
   - Кто является основными пользователями?
   - Каковы их цели?
   - Каковы их ограничения?

3. ** Пишите истории совместно ** - Используйте шаблон:
   ```bash
   cat ../../product-team/agile-product-owner/skills/agile-product-owner/assets/user_story_template.md
   ```
   - "В качестве [персона], я хочу [способность], так что [выгода]"
   - Сосредоточьтесь на пользовательской ценности, а не на деталях реализации
   - Одна история для каждого отдельного действия пользователя или результата

4. **Добавить критерии приемлемости** - Определить "готово":
   - Заданный формат/When/Then для каждого сценария
   - Рассмотрим счастливый путь, крайние случаи и состояния ошибок
   - Включать требования к производительности и доступности

5. ** Подтвердите ИНВЕСТИЦИИ ** - проверьте каждую историю:
   - ** Независимый**: Может быть представлен без других историй
   - **Подлежит обсуждению**: Гибкие детали реализации
   - **Ценный**: Обеспечивает ценность для пользователя или бизнеса
   - **Оцениваемый**: Команда может оценить усилия
   - **Маленький**: Помещается в пределах одного спринта
   - **Проверяемо**: Чистый проход/fail критерии

6. ** Оценивайте как команда ** - Консенсус по сюжетной линии:
   - Используйте покер планирования или кулак из пяти
   - Обсудите оценки выбросов
   - Повторное разделение, если оценка превышает 13 баллов

**Ожидаемый результат:** Набор пользовательских историй, соответствующих требованиям INVEST, с критериями приемлемости и оценками

** Ориентировочное время: ** 1-2 часа на семинар (охватывающий 1 эпическую или тематическую область)

**Пример:**
```bash
# Generate initial story candidates from epic
python ../../product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py feature-epic.yaml

# Reference story templates for format guidance
cat ../../product-team/agile-product-owner/skills/agile-product-owner/references/user-story-templates.md

# Reference sprint planning guide for estimation practices
cat ../../product-team/agile-product-owner/skills/agile-product-owner/references/sprint-planning-guide.md
```

## Примеры интеграции { #integration-examples }

### Пример 1: Сквозной цикл спринта { #example-1-end-to-end-sprint-cycle }

```bash
#!/bin/bash
# sprint-cycle.sh - Complete sprint planning automation

SPRINT_NUM=14
CAPACITY=12  # person-days equivalent in story points

echo "Sprint $SPRINT_NUM Planning"
echo "=========================="

# Step 1: Prioritize backlog
echo ""
echo "1. Backlog Prioritization:"
python ../../product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py backlog.csv --capacity $CAPACITY

# Step 2: Generate stories for top epic
echo ""
echo "2. Story Generation for Top Epic:"
python ../../product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py top-epic.yaml

# Step 3: Reference planning template
echo ""
echo "3. Sprint Planning Template:"
echo "See: ../../product-team/agile-product-owner/skills/agile-product-owner/assets/sprint_planning_template.md"
```

### Пример 2: Проверка работоспособности журнала невыполненных работ { #example-2-backlog-health-check }

```bash
#!/bin/bash
# backlog-health.sh - Weekly backlog health assessment

echo "Backlog Health Check - $(date +%Y-%m-%d)"
echo "========================================"

# Count stories by status
echo ""
echo "Backlog Items:"
wc -l < backlog.csv
echo "items in backlog"

# Run prioritization
echo ""
echo "Current Priorities:"
python ../../product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py backlog.csv --capacity 20

# Check story templates
echo ""
echo "Story Template Reference:"
echo "Location: ../../product-team/agile-product-owner/skills/agile-product-owner/references/user-story-templates.md"
```

## Показатели успеха { #success-metrics }

**Качество невыполненной работы:**
- **Готовность к рассказу:** >80% кандидатов на участие в спринте соответствуют определению готовности
- **Точность оценки:** Фактическое усилие в пределах 20% от расчетного (скользящее среднее)
- ** Размер истории:** <5% историй превышают 13 сюжетных баллов
- ** Критерии приемлемости:** 100% историй имеют проверяемые критерии приемлемости

**Выполнение спринта:**
- ** Достижение цели спринта:** >85% участников спринта достигают заявленной цели
- ** Стабильность скорости: ** Отклонение скорости <20% от спринта к спринту
- **Изменение области:** Изменение области менее чем на 10% после планирования спринта
- ** Уровень завершенности:** >90% зафиксированных историй завершено за спринт

**Ценность для стейкхолдеров:**
- ** Предоставление ценности:** Каждый спринт обеспечивает очевидную пользовательскую ценность
- ** Время цикла:** Среднее время цикла рассказа <5 дней
- ** Время выполнения заказа: ** Срок поставки в среднем <6 недель
- ** Удовлетворенность стейкхолдеров:** >4/5 по отзывам о ревью спринта

## Связанные агенты { #related-agents }

- [cs-менеджер по продукту](cs-product-manager.md) - Полный жизненный цикл управления продуктом (рисование, интервью, PRDS)
- [cs-продукт-стратег](cs-product-strategist.md) - Каскад OKR и стратегическое планирование для согласования дорожной карты
- [cs-ux-исследователь](cs-ux-researcher.md) - Исследование пользователей для информирования о требованиях к истории и критериях приемлемости
- Scrum Master - контекст скорости и выполнение спринта (см. [`skills/scrum-master`](https://github.com/imgusev/claude-skills-ru/tree/main/project-management/skills/scrum-master))

## Ссылки { #references }

- **Основной скилл:** [../../product-team/agile-product-owner/skills/agile-product-owner/SKILL.md](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/agile-product-owner/skills/agile-product-owner/SKILL.md)
- **РИСОВЫЙ фреймворк:** [../../product-team/skills/product-manager-toolkit/SKILL.md](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/product-manager-toolkit/SKILL.md)
- **Руководство по предметной области продукта:** [../../product-team/CLAUDE.md](https://github.com/imgusev/claude-skills-ru/tree/main/product-team/CLAUDE.md)
- **Руководство по разработке агента:** [../CLAUDE.md](https://github.com/imgusev/claude-skills-ru/tree/main/agents/CLAUDE.md)
- **Скилл мастера Scrum:** [../../project-management/skills/scrum-master/SKILL.md](https://github.com/imgusev/claude-skills-ru/tree/main/project-management/skills/scrum-master/SKILL.md)

---

** Последнее обновление:** 9 марта 2026 г.
**Статус:** Производство готово
**Версия:** 1.0
