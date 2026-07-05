---
name: "spawn"
description: "Запустите N параллельных субагентов в изолированных рабочих деревьях git, чтобы конкурировать в задаче сеанса. Используется, когда пользователь запускает /hub:spawn или запрашивает запуск конкурирующих агентов для инициализированного сеанса AgentHub."
command: /hub:spawn
---

# /hub:spawn — Запуск параллельных агентов { #hubspawn--launch-parallel-agents }

Создайте N субагентов, которые параллельно работают над одной и той же задачей, каждый в изолированном рабочем дереве git.

## Использование { #usage }

```
/hub:spawn                                    # Spawn agents for the latest session
/hub:spawn 20260317-143022                    # Spawn agents for a specific session
/hub:spawn --template optimizer               # Use optimizer template for dispatch prompts
/hub:spawn --template refactorer              # Use refactorer template
```

## Шаблоны { #templates }

Когда `--template <name>` если это предусмотрено, воспользуйтесь промпту отправки из `../agenthub/references/agent-templates.md` вместо промпта по умолчанию, приведенного ниже. Доступные шаблоны:

| Шаблон | Узор | Вариант использования |
|----------|---------|----------|
| `optimizer` | Редактировать → вычислять → сохранить/отбросить → повторить x10 | Производительность, задержка, уменьшение размера |
| `refactorer` | Реструктурировать → тестировать → повторять до получения зеленого цвета | Качество кода, технический долг |
| `test-writer` | Написать тесты → измерить охват → повторить | Пробелы в тестовом покрытии |
| `bug-fixer` | Воспроизвести → диагностировать → исправить → проверить | Исправлена ошибка с конкурирующими подходами |

При использовании шаблона замените все `{variables}` со значениями из конфигурации сеанса. Назначьте каждому агенту ** различную стратегию**, соответствующую шаблону и задаче — разнообразные стратегии максимизируют ценность параллельного исследования.

## Что он делает { #what-it-does }

1. Загрузите конфигурацию сеанса из `.agenthub/sessions/{session-id}/config.yaml`
2. Для каждого агента 1..N:
   - Напишите назначение задачи для `.agenthub/board/dispatch/`
   - Создайте промпту агента с задачей, ограничениями и инструкциями по написанию на доске
3. Запуск ВСЕХ агентов в ** одном сообщении** с несколькими вызовами инструментов агента:

```
Agent(
  prompt: "You are agent-{i} in hub session {session-id}.

Your task: {task}

Read your full assignment at .agenthub/board/dispatch/{seq}-agent-{i}.md

Instructions:
1. Work in your worktree — make changes, run tests, iterate
2. Commit all changes with descriptive messages
3. Write your result summary to .agenthub/board/results/agent-{i}-result.md
   Include: approach taken, files changed, metric if available, confidence level
4. Exit when done

Constraints:
- Do NOT read or modify other agents' work
- Do NOT access .agenthub/board/results/ for other agents
- Commit early and often with descriptive messages
- If you hit a dead end, commit what you have and explain in your result",
  isolation: "worktree"
)
```

4. Обновите состояние сеанса до `running` через:
```bash
python {skill_path}/scripts/session_manager.py --update {session-id} --state running
```

## Важнейшие правила { #critical-rules }

- **Все агенты в ОДНОМ сообщении ** — запускает все вызовы инструментов агента одновременно для обеспечения истинного параллелизма
- **изоляция: "worktree"** обязательна — каждому агенту нужна своя собственная файловая система
- **Никогда не изменяйте конфигурацию сеанса ** после появления — агенты полагаются на стабильную конфигурацию
- **Каждый агент получает уникальную запись на доске объявлений** — сообщения диспетчеров нумеруются последовательно

## После появления { #after-spawn }

Сообщите пользователю:
- {N} агенты, запущенные параллельно
- Каждый работает в изолированном рабочем дереве
- Монитор с `/hub:status`
- Оцените, когда закончите с `/hub:eval`
