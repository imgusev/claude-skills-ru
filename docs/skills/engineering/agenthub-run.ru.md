---
title: "/hub:run — Жизненный цикл с одним выстрелом { #hubrun--one-shot-lifecycle } — Агентский скилл для Codex и OpenClaw"
description: "Одноразовая команда жизненного цикла, которая объединяет init → baseline → spawn → eval → merge в одном вызове. Используйте, когда пользователь. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /hub:run — Жизненный цикл с одним выстрелом { #hubrun--one-shot-lifecycle }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `run`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/agenthub/skills/run/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Запустите полный жизненный цикл AgentHub одной командой: инициализируйте, зафиксируйте базовую линию, запустите агентов, оцените результаты и объедините победителя.

## Использование { #usage }

```
/hub:run --task "Reduce p50 latency" --agents 3 \
  --eval "pytest bench.py --json" --metric p50_ms --direction lower \
  --template optimizer

/hub:run --task "Refactor auth module" --agents 2 --template refactorer

/hub:run --task "Cover untested utils" --agents 3 \
  --eval "pytest --cov=utils --cov-report=json" --metric coverage_pct --direction higher \
  --template test-writer

/hub:run --task "Write 3 email subject lines for spring sale campaign" --agents 3 --judge
```

## Параметры { #parameters }

| Параметр | Требуемый | Описание |
|-----------|----------|-------------|
| `--task` | Да | Описание задачи для агентов |
| `--agents` | Нет | Количество параллельных агентов (по умолчанию: 3) |
| `--eval` | Нет | Команда Eval для измерения результатов (пропустить для режима LLM judge) |
| `--metric` | Нет | Имя метрики для извлечения из выходных данных eval (требуется, если `--eval` дано) |
| `--direction` | Нет | `lower` или `higher` — какое направление лучше (требуется, если `--metric` дано) |
| `--template` | Нет | Шаблон агента: `optimizer`, `refactorer`, `test-writer`, `bug-fixer` |

## Что он делает { #what-it-does }

Выполните эти шаги последовательно:

### Шаг 1: Инициализируйте { #step-1-initialize }

Бежать `/hub:init` с предоставленными аргументами:

```bash
python {skill_path}/scripts/hub_init.py \
  --task "{task}" --agents {N} \
  [--eval "{eval_cmd}"] [--metric {metric}] [--direction {direction}]
```

Отобразите идентификатор сеанса для пользователя.

### Шаг 2: Захват базовой линии { #step-2-capture-baseline }

Если `--eval` был предоставлен:

1. Запустите команду eval в текущем рабочем каталоге
2. Извлеките значение метрики из стандартного вывода
3. Дисплей: `Baseline captured: {metric} = {value}`
4. Добавить `baseline: {value}` к `.agenthub/sessions/{session-id}/config.yaml`

Если нет `--eval` был предоставлен, пропустите этот шаг.

### Шаг 3: Запускаем агентов { #step-3-spawn-agents }

Бежать `/hub:spawn` с идентификатором сеанса.

Если `--template` был предоставлен, используйте промпту отправки шаблона из [`references/agent-templates.md`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/agenthub/skills/agenthub/references/agent-templates.md) вместо промпта отправки по умолчанию. Передайте команду eval, метрику и базовую линию переменным шаблона.

Запуск всех агентов в одном сообщении с несколькими вызовами инструментов агента (истинный параллелизм).

### Шаг 4: Подождите и контролируйте { #step-4-wait-and-monitor }

После запуска сообщите пользователю, что агенты запущены. Когда все агенты завершат работу (инструмент агента возвращает результаты):

1. Отобразите краткую информацию о работе каждого агента
2. Переходите к оценке

### Шаг 5: Оценка { #step-5-evaluate }

Бежать `/hub:eval` с идентификатором сеанса:

- Если `--eval` было предоставлено: ранжирование на основе метрик с `result_ranker.py`
- Если нет `--eval`: Режим судьи LLM (координатор считывает различия и ранжирует)

Если базовая линия была захвачена, передайте `--baseline {value}` к `result_ranker.py` итак, показаны дельты.

Отобразите таблицу ранжированных результатов.

### Шаг 6: Подтвердите и объедините { #step-6-confirm-and-merge }

Представьте результаты пользователю и запросите подтверждение:

```
Agent-2 is the winner (128ms, -52ms from baseline).
Merge agent-2's branch? [Y/n]
```

Если подтвердится, запустите `/hub:merge`. В случае отклонения сообщите пользователю, что он может:
- `/hub:merge --agent agent-{N}` чтобы выбрать другого победителя
- `/hub:eval --judge` провести повторную оценку с судьей LLM
- Проверяйте ветви вручную

## Важнейшие правила { #critical-rules }

- **Последовательное выполнение** — каждый шаг зависит от предыдущего
- **Остановка при сбое ** — если какой-либо шаг завершается неудачей, сообщите об ошибке и остановитесь
- **Пользователь подтверждает слияние ** — никогда не выполняйте автоматическое слияние без запроса
- **шаблон необязателен** — без `--template`, агенты используют промпту отправки по умолчанию из `/hub:spawn`
