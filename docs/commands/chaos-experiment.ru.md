---
title: "/chaos-experiment — слэш-команда для ИИ-агентов разработки"
description: "Интерактивный мастер для разработки и проверки эксперимента по созданию хаоса. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /chaos-experiment

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/chaos-experiment.md">Источник</a></span>
</div>


Пройдите через проектирование эксперимента по созданию хаоса с использованием `chaos-engineering` скилл. Создает план, вычисляет радиус поражения, проверяет критерии отмены и выводит план Markdown, готовый для экспертной ревью.

## Использование { #usage }

```
/chaos-experiment
/chaos-experiment --target checkout-svc --attack latency
```

## Реализация { #implementation }

```bash
SKILL=engineering/chaos-engineering/skills/chaos-engineering

# Step 1: gather inputs interactively (target, hypothesis, attack, magnitude, ...)
# Step 2: run experiment_designer.py to produce the plan
python "$SKILL/scripts/experiment_designer.py" \
  --target "$TARGET" --hypothesis "$HYPOTHESIS" \
  --attack "$ATTACK" --magnitude "$MAGNITUDE" \
  --duration-min "$DURATION" \
  --abort-if "$ABORT" --owner "$OWNER" \
  --format json > .chaos-plan.json

# Step 3: calculate blast radius against the team's error budget
python "$SKILL/scripts/blast_radius_calculator.py" \
  --traffic-share "$TRAFFIC_SHARE" \
  --user-pop "$USER_POP" \
  --duration-min "$DURATION" \
  --baseline-availability "$BASELINE_AVAIL" \
  --expected-impact-availability "$IMPACT_AVAIL"

# Step 4: render the markdown plan for peer review
python "$SKILL/scripts/experiment_designer.py" \
  --target "$TARGET" --hypothesis "$HYPOTHESIS" \
  --attack "$ATTACK" --abort-if "$ABORT" --owner "$OWNER"
```

## Выход { #output }

План Markdown с:

- Гипотеза, показатель устойчивого состояния, атака, величина, продолжительность
- Радиус поражения (рассчитанный) с оценкой риска (ЗЕЛЕНЫЙ/ЖЕЛТЫЙ/КРАСНЫЙ)
- Критерии отмены, проанализированные из `--abort-if`
- Процедура отката
- Ссылка на дашборд мониторинга
- Учебный вопрос

## Предварительные условия { #pre-conditions }

- `chaos-engineering` установлен скилл
- Цель определена
- Доступны стационарные показатели и дашборд
- Доступна команда по вызову
- Известен бюджет ошибки (или используйте значения по умолчанию)

## Постусловия { #post-conditions }

- `.chaos-plan.json` написано для использования с `experiment_postmortem.py` позже
- План Markdown передан для ревью
- Напечатанная рекомендация: ПРОДОЛЖИТЬ / УМЕНЬШИТЬ / ПРЕРВАТЬ
