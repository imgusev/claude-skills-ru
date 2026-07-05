---
name: "product-strategist"
description: "Инструментарий стратегического руководства продуктом для руководителя отдела продуктов, охватывающий каскадную генерацию OKR, ежеквартальное планирование, анализ конкурентного ландшафта, документы о видении продукта и предложения по масштабированию команды. Используйте при создании ежеквартальных документов OKR, определении целей продукта или ключевых показателей эффективности, составлении дорожных карт продукта, проведении конкурентного анализа, составлении структуры команды или планов найма персонала, согласовании стратегии продукта с инженерными разработками и дизайном или создании каскадных иерархий целей от уровня компании до уровня команды."
---

# Специалист по продуктовому стратегу { #product-strategist }

Стратегический инструментарий для руководителя отдела продуктов для обеспечения видения, согласованности и организационного совершенства.

---

## Основные возможности { #core-capabilities }

| Способность | Описание | Инструмент |
|------------|-------------|------|
| **Каскад OKR** | Генерируйте согласованные OKR от уровня компании до уровня команды | `okr_cascade_generator.py` |
| **Оценка выравнивания** | Измерьте вертикальное и горизонтальное выравнивание | Встроенный в генератор |
| **Шаблоны стратегий** | 5 готовых типов стратегий | Рост, удержание, Выручка, Инновации, Операционная |
| **Конфигурация команды** | Настройка в соответствии со структурой вашей организации | `--teams` флаг |

---

## Быстрый старт { #quick-start }

```bash
# Growth strategy with default teams
python scripts/okr_cascade_generator.py growth

# Retention strategy with custom teams
python scripts/okr_cascade_generator.py retention --teams "Engineering,Design,Data"

# Revenue strategy with 40% product contribution
python scripts/okr_cascade_generator.py revenue --contribution 0.4

# Export as JSON for integration
python scripts/okr_cascade_generator.py growth --json > okrs.json
```

---

## Воркфлоу: Ежеквартальное стратегическое планирование { #workflow-quarterly-strategic-planning }

### Шаг 1: Определите стратегическую направленность { #step-1-define-strategic-focus }

| Стратегия | Когда использовать |
|----------|-------------|
| **Рост** | Масштабирование пользовательской базы, расширение рынка |
| **Удержание** | Сокращение оттока, повышение LTV |
| **Доход** | Увеличение ARPU, новая монетизация |
| **Инновации** | Дифференциация рынка, новые возможности |
| **Оперативный** | Повышение эффективности, масштабирование операций |

Видишь `references/strategy_types.md` для получения подробных указаний.

### Шаг 2: Соберите входные показатели { #step-2-gather-input-metrics }

```json
{
  "current": 100000,      // Current MAU
  "target": 150000,       // Target MAU
  "current_nps": 40,      // Current NPS
  "target_nps": 60        // Target NPS
}
```

### Шаг 3: Настройте команды и запустите генератор { #step-3-configure-teams--run-generator }

```bash
# Default teams
python scripts/okr_cascade_generator.py growth

# Custom org structure with contribution percentage
python scripts/okr_cascade_generator.py growth \
  --teams "Core,Platform,Mobile,AI" \
  --contribution 0.3
```

### Шаг 4: Ревью оценки выравнивания { #step-4-review-alignment-scores }

| Оценка | Цель | Действие, если ниже |
|-------|--------|-----------------|
| Вертикальное выравнивание | >90% | Убедитесь, что все цели связаны с родительской |
| Горизонтальное выравнивание | >75% | Проверьте, нет ли пробелов в координации команды |
| Охват | >80% | Проверьте, соблюдены ли все требования к компании |
| Равновесие | >80% | Перераспределять, если одна команда перегружена |
| **Общий** | **>80%** | <60% нуждается в реструктуризации |

### Шаг 5: Уточнение, проверка и экспорт { #step-5-refine-validate-and-export }

Перед завершением работы:

- [ ] Ревью сформированных целей с стейкхолдерами
- [ ] Корректируйте назначения команд в зависимости от возможностей
- [ ] Проверьте, реалистичны ли проценты взносов
- [ ] Убедитесь, что цели разных команд не противоречат друг другу
- [ ] Настройка частоты отслеживания (проверки раз в две недели)

```bash
# Export JSON for tools like Lattice, Ally, Workboard
python scripts/okr_cascade_generator.py growth --json > q1_okrs.json
```

---

## Каскадный генератор OKR { #okr-cascade-generator }

### Использование { #usage }

```bash
python scripts/okr_cascade_generator.py [strategy] [options]
```

**Стратегии:** `growth` | `retention` | `revenue` | `innovation` | `operational`

### Параметры конфигурации { #configuration-options }

| Вариант | Описание | Значение по умолчанию |
|--------|-------------|---------|
| `--teams`, `-t` | Названия команд, разделенные запятыми | Рост,Платформа, Мобильные устройства,Данные |
| `--contribution`, `-c` | Вклад продукта в OKR компании (0-1) | 0.3 (30%) |
| `--json`, `-j` | Вывод в формате JSON вместо дашборда | Ложный |
| `--metrics`, `-m` | Метрики в виде строки JSON | Примеры показателей |

### Выходные примеры { #output-examples }

#### Вывод на Дашборд (`growth` стратегия) { #dashboard-output-growth-strategy }

```
============================================================
OKR CASCADE DASHBOARD
Quarter: Q1 2025  |  Strategy: GROWTH
Teams: Growth, Platform, Mobile, Data  |  Product Contribution: 30%
============================================================

🏢 COMPANY OKRS
📌 CO-1: Accelerate user acquisition and market expansion
   └─ CO-1-KR1: Increase MAU from 100,000 to 150,000
   └─ CO-1-KR2: Achieve 50% MoM growth rate
   └─ CO-1-KR3: Expand to 3 new markets

📌 CO-2: Achieve product-market fit in new segments
📌 CO-3: Build sustainable growth engine

🚀 PRODUCT OKRS
📌 PO-1: Build viral product features and market expansion
   ↳ Supports: CO-1
   └─ PO-1-KR1: Increase product MAU to 45,000
   └─ PO-1-KR2: Achieve 45% feature adoption rate

👥 TEAM OKRS
Growth Team:
  📌 GRO-1: Build viral product features through acquisition and activation
     └─ GRO-1-KR1: Increase product MAU to 11,250
     └─ GRO-1-KR2: Achieve 11.25% feature adoption rate

🎯 ALIGNMENT SCORES
✓ Vertical Alignment: 100.0%
! Horizontal Alignment: 75.0%
✓ Coverage: 100.0%  |  ✓ Balance: 97.5%  |  ✓ Overall: 94.0%
✅ Overall alignment is GOOD (≥80%)
```

#### Вывод в формате JSON (`retention --json`, усеченный) { #json-output-retention---json-truncated }

```json
{
  "quarter": "Q1 2025",
  "strategy": "retention",
  "company": {
    "objectives": [
      {
        "id": "CO-1",
        "title": "Create lasting customer value and loyalty",
        "key_results": [
          { "id": "CO-1-KR1", "title": "Improve retention from 70% to 85%", "current": 70, "target": 85 }
        ]
      }
    ]
  },
  "product": { "contribution": 0.3, "objectives": ["..."] },
  "teams": ["..."],
  "alignment_scores": {
    "vertical_alignment": 100.0, "horizontal_alignment": 75.0,
    "coverage": 100.0, "balance": 97.5, "overall": 94.0
  }
}
```

Видишь `references/examples/sample_growth_okrs.json` для полного примера.

---

## Справочные документы { #reference-documents }

| Документ | Описание |
|----------|-------------|
| `references/okr_framework.md` | Методология OKR, рекомендации по написанию, оценка соответствия |
| `references/strategy_types.md` | Подробная разбивка всех 5 типов стратегий с примерами |
| `references/examples/sample_growth_okrs.json` | Полный пример выходных данных для стратегии роста |

---

## Лучшие практики { #best-practices }

### Каскад ОКР { #okr-cascade }

- Ограничьтесь 3-5 целями на уровне, каждая из которых имеет 3-5 ключевых результатов
- Ключевые результаты должны быть измеримы текущими и целевыми значениями
- Проверьте отношения между родителями и дочерними элементами перед завершением работы

### Оценка выравнивания { #alignment-scoring }

- Цель >80% общего соответствия; исследуйте любой балл ниже 60%
- Сбалансированные баллы гарантируют, что ни одна команда не будет перегружена
- Горизонтальное выравнивание предотвращает противоречивые цели в разных командах

### Конфигурация команды { #team-configuration }

- Настройте команды в соответствии с вашей фактической организационной структурой
- Отрегулируйте процент вклада в зависимости от размера команды
- Команды платформы/инфраструктуры часто поддерживают все цели
- Специализированные группы (ML, Data) могут поддерживать только соответствующие цели

## Связанные скиллы { #related-skills }

- **Старший премьер-министр** (`project-management/senior-pm/`) — Управление портфелем и анализ рисков являются основой стратегического планирования
- **Конкурентный срыв** (`product-team/competitive-teardown/`) — Конкурентная разведка формирует стратегию продукта
