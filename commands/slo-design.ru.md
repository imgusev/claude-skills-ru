---
description: "Интерактивный мастер для создания SLO с предупреждениями о SLI, цели, бюджете ошибок и скорости выгорания"
---

# /slo-design { #slo-design }

Пошаговое проектирование SLO с использованием `slo-architect` скилл. Создает определение SLO, вычисляет бюджет ошибок + многооконные предупреждения о скорости выгорания и запускает средство проверки для выявления распространенных ошибок.

## Использование { #usage }

```
/slo-design
/slo-design --service checkout-svc --sli-type request-success-rate --target 99.9
```

## Реализация { #implementation }

```bash
SKILL=engineering/slo-architect/skills/slo-architect

# Step 1: gather inputs (service, sli-type, target, window, owner)
# Step 2: render SLO definition
python "$SKILL/scripts/slo_designer.py" \
  --service "$SERVICE" \
  --sli-type "$SLI_TYPE" \
  --target "$TARGET" \
  --window-days "$WINDOW_DAYS" \
  --owner "$OWNER" \
  --policy-doc "$POLICY_DOC" \
  --format json > .slo.json

# Step 3: compute error budget + burn-rate alerts
python "$SKILL/scripts/error_budget_calculator.py" \
  --target "$TARGET" \
  --window-days "$WINDOW_DAYS"

# Step 4: render the markdown SLO for peer review
python "$SKILL/scripts/slo_designer.py" \
  --service "$SERVICE" \
  --sli-type "$SLI_TYPE" \
  --target "$TARGET" \
  --window-days "$WINDOW_DAYS" \
  --owner "$OWNER" \
  --policy-doc "$POLICY_DOC"

# Step 5: validate against the reviewer
echo "=== After saving the SLO, run slo_review.py against the doc ==="
```

## Выход { #output }

Определение Markdown SLO с помощью:

- Сервис, владелец, путешествие пользователя
- Тип SLI с числителем/denominator выражения
- Цель, окно, бюджет ошибок
- Пороговые значения оповещения о частоте выгорания в нескольких окнах (в форме PromQL)
- Частота ревью

## Предварительные условия { #pre-conditions }

- `slo-architect` установлен скилл
- Идентифицированная служба
- доступны исторические данные SLI за 30 дней (для выбора устойчивой цели)
- Ошибка документ бюджетной политики существует или будет создан

## Постусловия { #post-conditions }

- `.slo.json` написано для использования с нижестоящими инструментами (chaos-engineering, радиус поражения и т.д.)
- Markdown SLO транслировался для ревью
- Напечатанная рекомендация: ПРОПУСК / ПРЕДУПРЕЖДЕНИЕ / СБОЙ при включении `slo_review.py` проверки
