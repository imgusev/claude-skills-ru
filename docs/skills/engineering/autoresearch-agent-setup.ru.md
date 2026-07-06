---
title: "/ar:setup — Создайте новый эксперимент { #arsetup--create-new-experiment } — Агентский скилл для Codex и OpenClaw"
description: "Настройте новый эксперимент с автоматическим поиском в интерактивном режиме. Собирает домен, целевой файл, команду eval, метрику, направление и. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /ar:setup — Создайте новый эксперимент { #arsetup--create-new-experiment }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `setup`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/autoresearch-agent/skills/setup/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Настройте новый эксперимент с автоматическим поиском со всеми необходимыми настройками.

## Использование { #usage }

```
/ar:setup                                    # Interactive mode
/ar:setup engineering api-speed src/api.py "pytest bench.py" p50_ms lower
/ar:setup --list                             # Show existing experiments
/ar:setup --list-evaluators                  # Show available evaluators
```

## Что он делает { #what-it-does }

### Если предоставлены аргументы { #if-arguments-provided }

Передайте их непосредственно в сценарий установки:

```bash
python {skill_path}/scripts/setup_experiment.py \
  --domain {domain} --name {name} \
  --target {target} --eval "{eval_cmd}" \
  --metric {metric} --direction {direction} \
  [--evaluator {evaluator}] [--scope {scope}]
```

### Если аргументов нет (интерактивный режим) { #if-no-arguments-interactive-mode }

Собирайте каждый параметр по одному за раз:

1. **Домен** — Спросите: "Какой домен? (инжиниринг, маркетинг, контент, промптов, кастомизация)"
2. **Название** — Спросите: "Название эксперимента? (например, скорость api, заголовки блогов)"
3. **Целевой файл** — Спросите: "Какой файл оптимизировать?" Убедитесь, что он существует.
4. **Команда Eval** — Спросите: "Как это измерить? (например, pytest bench.py , питон evaluate.py )"
5. **Метрика** — Спросите: "Какую метрику выводит eval? (например, p50_ms, ctr_score)"
6. **Направление** — Спросите: "Ниже или выше лучше?"
7. **Оценщик** (необязательно) — Отображение встроенных оценщиков. Спросите: "Используете встроенный оценщик или свой собственный?"
8. **Область применения** — Спросите: "Хранить в проекте (.autoresearch/) или у пользователя (~/.autoresearch/)?"

Затем беги `setup_experiment.py` с собранными параметрами.

### Список { #listing }

```bash
# Show existing experiments
python {skill_path}/scripts/setup_experiment.py --list

# Show available evaluators
python {skill_path}/scripts/setup_experiment.py --list-evaluators
```

## Встроенные средства оценки { #built-in-evaluators }

| Имя | Метрика | Вариант использования |
|------|--------|----------|
| `benchmark_speed` | `p50_ms` (ниже) | Время выполнения функции/API |
| `benchmark_size` | `size_bytes` (ниже) | Размер файла, пакета, изображения Docker |
| `test_pass_rate` | `pass_rate` (выше) | Процент прохождения набора тестов |
| `build_speed` | `build_seconds` (ниже) | Строить/compile/Время сборки Docker |
| `memory_usage` | `peak_mb` (ниже) | Максимальный объем памяти во время выполнения |
| `llm_judge_content` | `ctr_score` (выше) | Заголовки, заглавия, описания |
| `llm_judge_prompt` | `quality_score` (выше) | Системные промпты, инструкции агента |
| `llm_judge_copy` | `engagement_score` (выше) | Посты в социальных сетях, копия рекламы, электронные письма |

## После настройки { #after-setup }

Отчитываться перед пользователем:
- Путь к эксперименту и название ветви
- Сработала ли команда eval и базовый показатель
- Предложите: "Запустите `/ar:run {domain}/{name}` чтобы начать итерацию, или `/ar:loop {domain}/{name}` для автономного режима."
