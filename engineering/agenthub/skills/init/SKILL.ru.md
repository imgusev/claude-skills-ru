---
name: "init"
description: "Создайте новый сеанс совместной работы AgentHub с заданием, количеством агентов и критериями оценки. Используется, когда пользователь запускает /hub:init или запрашивает запуск соревнования с несколькими агентами для выполнения задачи."
command: /hub:init
---

# /hub:init — Создать новую сессию { #hubinit--create-new-session }

Инициализируйте сеанс совместной работы AgentHub. Создает `.agenthub/` структура каталогов, генерирует идентификатор сеанса и настраивает критерии оценки.

## Использование { #usage }

```
/hub:init                                                    # Interactive mode
/hub:init --task "Optimize API" --agents 3 --eval "pytest bench.py" --metric p50_ms --direction lower
/hub:init --task "Refactor auth" --agents 2                  # No eval (LLM judge mode)
```

## Что он делает { #what-it-does }

### Если предоставлены аргументы { #if-arguments-provided }

Передайте их в сценарий инициализации:

```bash
python {skill_path}/scripts/hub_init.py \
  --task "{task}" --agents {N} \
  [--eval "{eval_cmd}"] [--metric {metric}] [--direction {direction}] \
  [--base-branch {branch}]
```

### Если аргументов нет (интерактивный режим) { #if-no-arguments-interactive-mode }

Соберите каждый параметр:

1. **Задача** — Что должны делать агенты? (обязательно)
2. **Количество агентов** — Сколько параллельных агентов? (по умолчанию: 3)
3. **команда Eval** — команда для измерения результатов (необязательно — пропустить для режима LLM judge)
4. **Название метрики** — Какую метрику извлекать из выходных данных eval (требуется, если задана команда eval)
5. **Направление** — Ниже или выше лучше? (требуется, если указана метрика)
6. **Базовая ветвь** — Ветвь, от которой нужно разветвиться (по умолчанию: текущая ветвь)

### Выход { #output }

```
AgentHub session initialized
  Session ID: 20260317-143022
  Task: Optimize API response time below 100ms
  Agents: 3
  Eval: pytest bench.py --json
  Metric: p50_ms (lower is better)
  Base branch: dev
  State: init

Next step: Run /hub:spawn to launch 3 agents
```

Для задач по содержанию или исследованию (без команды eval → режим оценки LLM):

```
AgentHub session initialized
  Session ID: 20260317-151200
  Task: Draft 3 competing taglines for product launch
  Agents: 3
  Eval: LLM judge (no eval command)
  Base branch: dev
  State: init

Next step: Run /hub:spawn to launch 3 agents
```

## Захват базовой линии { #baseline-capture }

Если `--eval` было предоставлено, зафиксируйте базовое измерение после создания сеанса:

1. Запустите команду eval в текущем рабочем каталоге
2. Извлеките значение метрики из стандартного вывода
3. Добавить `baseline: {value}` к `.agenthub/sessions/{session-id}/config.yaml`
4. Дисплей: `Baseline captured: {metric} = {value}`

Эта базовая линия используется `result_ranker.py --baseline` во время оценки, чтобы показать дельты. Если команда eval завершится неудачей на этом этапе, предупредите пользователя, но продолжайте — базовый уровень необязателен.

## После инициализации { #after-init }

Сообщите пользователю:
- Сеанс, созданный с идентификатором `{session-id}`
- Базовый показатель (если он зафиксирован)
- Следующий шаг: `/hub:spawn` для запуска агентов
- Или `/hub:spawn {session-id}` если существует несколько сеансов
