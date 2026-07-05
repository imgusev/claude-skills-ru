---
title: "Тестировщик скилла { #skill-tester } — Агентский скилл для Codex и OpenClaw"
description: "Подтверждайте, тестируйте и оценивайте качество скиллы в рамках экосистемы claude-скиллы. Комплексный мета-скилл: проверка структуры, тестирование. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Тестировщик скилла { #skill-tester }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `skill-tester`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/skill-tester/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Уровень **: МОЩНЫЙ · ** Категория**: Обеспечение инженерного качества · ** Зависимости**: Отсутствуют (только Python stdlib)

Мета-скиллы, которые проверяют, тестируют и оценивают скиллы в этом хранилище. Четыре инструмента, запускаемые из **корневого хранилища** с полными путями:

1. **`scripts/skill_validator.py`** — структура + соответствие документации
2. **`scripts/script_tester.py`** — Синтаксис скрипта Python/импорт/время выполнения/тестирование вывода
3. **`scripts/quality_scorer.py`** — многомерная оценка с буквенной оценкой
4. **`scripts/security_scorer.py`** — оценка состояния безопасности (также доступна через `quality_scorer.py --include-security`)

> ** Примечание по области применения: ** минимальные значения количества строк уровня этого скилла измеряют * унаследованные* скиллы. Для разработки *новых* скиллы, `engineering/write-a-skill` (SKILL.md менее ~ 100 строк, доктрина Мэтта Покока) является обязательным стандартом — не добавляйте новый скилл, чтобы соответствовать минимальному уровню.

## Быстрый запуск (точный, запускаемый из корневого хранилища) { #quick-start-exact-runnable-from-repo-root }

```bash
# 1. Validate structure (exit non-zero on failure — usable as a gate)
python3 engineering/skills/skill-tester/scripts/skill_validator.py engineering/skills/self-eval --json

# 2. Test the skill's Python scripts (30s default timeout per script)
python3 engineering/skills/skill-tester/scripts/script_tester.py engineering/skills/self-eval --json

# 3. Score quality (fail CI below threshold with --minimum-score)
python3 engineering/skills/skill-tester/scripts/quality_scorer.py engineering/skills/self-eval --json --detailed --minimum-score 75
```

Потребляйте JSON: валидатор выдает `overall_score`, `compliance_level`, за каждый чек `checks{}`; бомбардир выдает `overall_score`, `letter_grade`, `tier_recommendation`, `dimensions`, и ан `improvement_roadmap` — проработайте дорожную карту сверху вниз, затем повторяйте до тех пор, пока не будет достигнут целевой показатель.

Для аудита в масштабах репо предпочитайте `scripts/audit_skills.py` в корне репозитория (переносит бегунок с чек-листом записи скилла на все скиллы).

## Что проверяет каждый инструмент { #what-each-tool-checks }

### skill_validator.py { #skill_validatorpy }
- SKILL.md синтаксический анализ frontmatter, необходимые разделы, минимальное количество строк на уровне (`--tier BASIC|STANDARD|POWERFUL`)
- Требуемая структура: SKILL.md , README.md , скрипты/, ссылки/, ресурсы/, ожидаемые выходные данные/
- Скрипты на Python: присутствует argparse, импортируется только stdlib

### script_tester.py { #script_testerpy }
- Проверка синтаксиса на основе AST; анализ импорта (помечает внешние зависимости)
- Контролируемое выполнение с защитой от тайм-аута (`--timeout`, по умолчанию 30 секунд)
- `--help` проверка функциональности; выборка-данные выполняются по сравнению с ожидаемыми выходными/

### quality_scorer.py { #quality_scorerpy }
Четыре измерения, по 25% каждое: ** Документация** (глубина, примеры, ссылки), ** Качество кода** (сложность, обработка ошибок, согласованность выходных данных), ** Полнота** (требуемые каталоги, примеры данных, ожидаемые выходные данные), ** Удобство использования** (текст справки, наглядность примера). Результаты 0-100 + оценка A-F + рекомендация по уровню.

## Классификация уровней { #tier-classification }

| Уровень | SKILL.md | Сценарии | Поверхность CLI |
|---|---|---|---|
| БАЗОВЫЙ | ≥ 100 строк | 1 (100-300 LOC) | базовый argparse |
| СТАНДАРТНЫЙ | ≥ 200 строк | 1-2 (300-500 LOC) | подкоманды, вывод текста в формате JSON + |
| МОЩНЫЙ | ≥ 300 строк | 2-3 (500-800 LOC) | несколько режимов, интеграция CI |

(Рекомендации по устаревшим скиллам; новые скиллы следуют за написанием скилла - смотрите примечание о сфере применения выше.)

## Интеграция CI { #ci-integration }

```yaml
# GitHub Actions: gate changed skills
- name: "validate-changed-skills"
  run: |
    for skill in $changed_skills; do
      python3 engineering/skills/skill-tester/scripts/skill_validator.py "$skill" --json
      python3 engineering/skills/skill-tester/scripts/script_tester.py "$skill"
      python3 engineering/skills/skill-tester/scripts/quality_scorer.py "$skill" --minimum-score 75
    done
```

Крючок предварительной фиксации: запустите валидатор в каталоге поэтапного скилла и заблокируйте фиксацию при ненулевом выходе.

## Цикл проверки { #verification-loop }

Скилл "проходит", когда за один запуск из корня репозитория:

1. `skill_validator.py <skill> --json` выходы 0,
2. `script_tester.py <skill>` сообщает о прохождении всех сценариев, и
3. `quality_scorer.py <skill> --minimum-score <target>` завершает работу 0.

Если какой-либо шаг не удался, примените верхний `improvement_roadmap` выберите пункт и повторно запустите все три - никогда не сообщайте о частичном прохождении.

## Устранение неполадок { #troubleshooting }

- **Ошибки тайм-аута** → поднять `--timeout` или оптимизируйте тестируемый скрипт
- **Сбои импорта** → обнаружены внешние deps; политика репозитория доступна только для stdlib
- **Неправильная классификация уровней ** → проверьте количество строк/LOC в таблице уровней; помните об исключении записи скилла для новых скиллы.

Ссылки: `references/` содержит спецификацию структуры, матрицу требований к уровням и рубрику оценки, реализуемую инструментами.
