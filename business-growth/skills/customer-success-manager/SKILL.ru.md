---
name: "customer-success-manager"
description: Отслеживает состояние клиентов, прогнозирует риск оттока и определяет возможности расширения, используя взвешенные модели оценки успешности клиентов SaaS. Используйте при анализе учетных записей клиентов, ревью показателей удержания, оценке клиентов из группы риска или когда пользователь упоминает об оттоке, показателях здоровья клиентов, возможностях увеличения продаж, доходах от расширения, анализе удержания или аналитике клиентов. Запускает три инструмента Python CLI для получения детерминированных показателей работоспособности, уровней риска оттока и рекомендаций по приоритетному расширению в сегментах предприятий, среднего и малого бизнеса.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: business-growth
  domain: customer-success
  updated: 2026-02-06
  python-tools: health_score_calculator.py, churn_risk_analyzer.py, expansion_opportunity_scorer.py
  tech-stack: customer-success, saas-metrics, health-scoring
---

# Менеджер по работе с клиентами { #customer-success-manager }

Аналитика успеха клиентов производственного уровня с многомерной оценкой состояния здоровья, прогнозированием риска оттока и выявлением возможностей расширения. Три инструмента Python CLI обеспечивают детерминированный, повторяемый анализ только с использованием стандартной библиотеки - никаких внешних зависимостей, никаких вызовов API, никаких моделей ML.

---

## Оглавление { #table-of-contents }

- [Входные требования](#input-requirements)
- [Выходные форматы](#output-formats)
- [Как использовать](#how-to-use)
- [Сценарии](#scripts)
- [Справочные руководства](#reference-guides)
- [Шаблоны](#templates)
- [Лучшие практики](#best-practices)
- [Ограничения](#limitations)

---

## Входные требования { #input-requirements }

Все скрипты принимают файл JSON в качестве позиционного входного аргумента. Видишь `assets/sample_customer_data.json` для получения полных примеров схем и выборочных данных.

### Калькулятор показателей здоровья { #health-score-calculator }

Обязательные поля для каждого объекта клиента: `customer_id`, `name`, `segment`, `arr`, и вложенные объекты `usage` (login_frequency, feature_adoption, dau_mau_ratio), `engagement` (support_ticket_volume, meeting_attendance, nps_score, csat_score), `support` (open_tickets, escalation_rate, avg_resolution_hours), `relationship` (executive_sponsor_engagement, multi_threading_depth, renewal_sentiment), и `previous_period` баллы за анализ тенденций.

### Анализатор рисков оттока { #churn-risk-analyzer }

Обязательные поля для каждого объекта клиента: `customer_id`, `name`, `segment`, `arr`, `contract_end_date`, и вложенные объекты `usage_decline`, `engagement_drop`, `support_issues`, `relationship_signals`, и `commercial_factors`.

### Бомбардир возможностей расширения { #expansion-opportunity-scorer }

Обязательные поля для каждого объекта клиента: `customer_id`, `name`, `segment`, `arr`, и вложенные объекты `contract` (лицензированные места, активные места, плановые места, доступные места), `product_usage` (флаги принятия для каждого модуля и проценты использования), и `departments` (текущий и потенциальный).

---

## Выходные форматы { #output-formats }

Все скрипты поддерживают два выходных формата через `--format` флаг:

- **`text`** (по умолчанию): Удобочитаемый форматированный вывод для просмотра на терминале
- **`json`**: Машиночитаемый вывод в формате JSON для интеграций и пайплайнов

---

## Как использовать { #how-to-use }

### Быстрый старт { #quick-start }

```bash
# Health scoring
python scripts/health_score_calculator.py assets/sample_customer_data.json
python scripts/health_score_calculator.py assets/sample_customer_data.json --format json

# Churn risk analysis
python scripts/churn_risk_analyzer.py assets/sample_customer_data.json
python scripts/churn_risk_analyzer.py assets/sample_customer_data.json --format json

# Expansion opportunity scoring
python scripts/expansion_opportunity_scorer.py assets/sample_customer_data.json
python scripts/expansion_opportunity_scorer.py assets/sample_customer_data.json --format json
```

### Интеграция с воркфлоу { #workflow-integration }

```bash
# 1. Score customer health across portfolio
python scripts/health_score_calculator.py customer_portfolio.json --format json > health_results.json
# Verify: confirm health_results.json contains the expected number of customer records before continuing

# 2. Identify at-risk accounts
python scripts/churn_risk_analyzer.py customer_portfolio.json --format json > risk_results.json
# Verify: confirm risk_results.json is non-empty and risk tiers are present for each customer

# 3. Find expansion opportunities in healthy accounts
python scripts/expansion_opportunity_scorer.py customer_portfolio.json --format json > expansion_results.json
# Verify: confirm expansion_results.json lists opportunities ranked by priority

# 4. Prepare QBR using templates
# Reference: assets/qbr_template.md
```

**Обработка ошибок:** Если скрипт завершает работу с ошибкой, проверьте, что:
- Входной JSON соответствует требуемой схеме для этого скрипта (см. Требования к вводу выше)
- Все обязательные поля присутствуют и введены правильно
- Используется Python 3.7+ (`python --version`)
- Выходные файлы предыдущих шагов не являются пустыми перед переходом к последующим шагам

---

## Сценарии { #scripts }

### 1. health_score_calculator.py { #1-health_score_calculatorpy }

** Цель:** Многомерная оценка состояния здоровья клиентов с анализом тенденций и сравнительным анализом с учетом сегментов.

**Размеры и вес:**
| Измерение | Вес | Показатели |
|-----------|--------|---------|
| Использование | 30% | Частота входа в систему, внедрение функций, соотношение DAU/MAU |
| Помолвка | 25% | Количество заявок в службу поддержки, посещаемость собраний, NPS/CSAT |
| Поддержка | 20% | Открытые заявки, скорость эскалации, среднее время разрешения |
| Отношения | 25% | Вовлечение исполнительного спонсора, глубина многопоточности, стремление к обновлению |

**Классификация:**
- Зеленый (75-100): Здоровый - достижение ценности для клиентов
- Желтый (50-74): Требует внимания - внимательно следите
- Красный (0-49): В зоне риска - требуется немедленное вмешательство.

**Использование:**
```bash
python scripts/health_score_calculator.py customer_data.json
python scripts/health_score_calculator.py customer_data.json --format json
```

### 2. churn_risk_analyzer.py { #2-churn_risk_analyzerpy }

**Цель:** Выявление учетных записей, подверженных риску, с помощью обнаружения поведенческих сигналов и рекомендаций по вмешательству на основе уровней.

**Весовые коэффициенты сигналов о риске:**
| Категория сигнала | Вес | Индикаторы |
|----------------|--------|------------|
| Снижение использования | 30% | Тенденция входа в систему, изменение в использовании функций, изменение DAU/MAU |
| Снижение вовлеченности | 25% | Отмена собраний, время ответа, изменение NPS |
| Проблемы с поддержкой | 20% | Открытая эскалация, нерешенная проблема, тенденция к удовлетворенности |
| Сигналы о взаимоотношениях | 15% | Чемпион ушел, сменился спонсор, упоминания о конкурентах |
| Коммерческие факторы | 10% | Тип контракта, жалобы на ценообразование, сокращение бюджета |

**Уровни риска:**
- Критический (80-100): Немедленная эскалация исполнительной власти
- Высокий (60-79): Срочное вмешательство CSM
- Средний (40-59): Активный охват
- Низкий уровень (0-39): Стандартный мониторинг

**Использование:**
```bash
python scripts/churn_risk_analyzer.py customer_data.json
python scripts/churn_risk_analyzer.py customer_data.json --format json
```

### 3. expansion_opportunity_scorer.py { #3-expansion_opportunity_scorerpy }

**Цель:** Определить возможности для увеличения продаж, перекрестных продаж и расширения с оценкой выручки и ранжированием приоритетов.

**Типы расширения:**
- **Повышение продаж**: Обновление существующего продукта до более высокого уровня или большего количества
- **Перекрестная продажа**: Добавление новых модулей продукта
- **Расширение**: Дополнительные места или отделы

**Использование:**
```bash
python scripts/expansion_opportunity_scorer.py customer_data.json
python scripts/expansion_opportunity_scorer.py customer_data.json --format json
```

---

## Справочные руководства { #reference-guides }

| Ссылка | Описание |
|-----------|-------------|
| `references/health-scoring-framework.md` | Полная методология оценки состояния здоровья, определения размеров, обоснование взвешивания, калибровка порогового значения |
| `references/cs-playbooks.md` | Плейбуки для вмешательства для каждого уровня риска, процедуры онбординга, обновления, расширения и эскалации |
| `references/cs-metrics-benchmarks.md` | Отраслевые критерии для NRR, GRR, показателей оттока, показателей здоровья, темпов расширения по сегментам и отраслям |

---

## Шаблоны { #templates }

| Шаблон | Цель |
|----------|---------|
| `assets/qbr_template.md` | Структура презентации ежеквартального бизнес-ревью |
| `assets/success_plan_template.md` | План успеха клиента с целями, контрольными точками и показателями |
| `assets/onboarding_checklist_template.md` | чек-лист для онбординга на 90 дней с фазовыми гейтами |
| `assets/executive_business_review_template.md` | Ревью руководителей стейкхолдеров по стратегическим счетам |

---

## Лучшие практики { #best-practices }

1. ** Комбинируйте сигналы**: Используйте все три скрипта вместе для получения полной картины клиента
2. ** Действуйте в соответствии с тенденциями, а не моментальными снимками **: Снижающийся зеленый цвет более актуален, чем стабильный желтый
3. ** Откалибруйте пороговые значения**: Отрегулируйте ориентиры сегмента в зависимости от вашего продукта и отрасли в соответствии с `references/health-scoring-framework.md`
4. **Подготовка с использованием данных**: Запуск сценариев перед каждым QBR и совещанием руководителей; ссылка `references/cs-playbooks.md` для руководства по вмешательству

---

## Ограничения { #limitations }

- **Нет данных в реальном времени**: Скрипты анализируют моментальные снимки из входных файлов JSON
- ** Нет интеграции с CRM **: Данные должны быть экспортированы вручную с вашей платформы CRM/CS
- ** Только детерминированный **: Нет прогнозирующего ML - оценка производится алгоритмически на основе взвешенных сигналов
- ** Настройка порога **: Пороговые значения по умолчанию являются отраслевыми стандартами, но могут потребовать калибровки для вашего бизнеса
- ** Оценки выручки **: Оценки выручки от расширения являются приблизительными, основанными на моделях использования

---

** Последнее обновление:** Февраль 2026
** Инструменты:** 3 инструмента Python CLI
**Зависимости:** Только стандартная библиотека Python 3.7+
