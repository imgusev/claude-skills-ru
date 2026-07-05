---
title: "Разработчик системы собеседований { #interview-system-designer } — Агентский скилл для Codex и OpenClaw"
description: "Этот скилл следует использовать, когда пользователь просит 'спроектировать процессы собеседования', 'создать пайплайны найма', 'откалибровать циклы. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Разработчик системы собеседований { #interview-system-designer }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `interview-system-designer`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/interview-system-designer/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Всесторонняя поддержка планирования цикла собеседований и калибровки для систем найма на основе ролей.

## Обзор { #overview }

Используйте этот скилл для создания структурированных циклов собеседований, стандартизации качества вопросов и обеспечения согласованности сигналов о приеме на работу у всех интервьюеров.

## Основные возможности { #core-capabilities }

- Планирование цикла собеседования в разбивке по ролям и уровням
- Рекомендации по направленности и срокам проведения каждого раунда
- Предлагаемые наборы вопросов по круглому типу
- Поддержка фреймворка для подсчета очков и калибровки
- Руководство по устранению предвзятости и согласованности процессов

## Быстрый старт { #quick-start }

```bash
# Generate a loop plan for a role and level
python3 scripts/interview_planner.py --role "Senior Software Engineer" --level senior

# JSON output for integration with internal tooling
python3 scripts/interview_planner.py --role "Product Manager" --level mid --json
```

## Рекомендуемый воркфлоу { #recommended-workflow }

1. Бежать `scripts/interview_planner.py` чтобы сгенерировать базовый цикл.
2. Приведите раунды в соответствие с компетенциями, специфичными для конкретной роли.
3. Проверьте соответствие рейтинговых рубрик лидам группы собеседований.
4. Перед раскаткой проведите ревью на предмет контроля смещения.
5. Ежеквартально проводите повторную калибровку, используя данные о результатах найма.

## Ссылки { #references }

- `references/interview-frameworks.md`
- `references/bias_mitigation_checklist.md`
- `references/competency_matrix_templates.md`
- `references/debrief_facilitation_guide.md`

## Распространенные подводные камни { #common-pitfalls }

- Перевешивание в одном раунде при игнорировании других сигналов о компетентности
- Использование неструктурированных интервью без стандартизированной оценки
- Пропуск сеансов калибровки для интервьюеров
- Изменение планки приема на работу без документального обоснования

## Лучшие практики { #best-practices }

1. Держите цели раунда четкими и не пересекающимися.
2. Требуйте доказательств для каждой рекомендации по оценке.
3. Используйте одну и ту же базовую рубрику для сопоставимых ролей.
4. Пересмотрите дизайн цикла, основанный на результатах, связанных с качеством найма.
