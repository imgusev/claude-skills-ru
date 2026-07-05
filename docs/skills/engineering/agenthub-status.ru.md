---
title: "/hub:status — Статус сеанса { #hubstatus--session-status } — Агентский скилл для Codex и OpenClaw"
description: "Показывать состояние DAG, прогресс агента и статус филиала для сеанса AgentHub. Используйте, когда пользователь запускает /hub:status или спрашивает. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /hub:status — Статус сеанса { #hubstatus--session-status }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `status`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/agenthub/skills/status/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Отображать текущее состояние сеанса AgentHub: ветви агента, количество фиксаций, статус границы и обновления доски объявлений.

## Использование { #usage }

```
/hub:status                        # Status for latest session
/hub:status 20260317-143022        # Status for specific session
```

## Что он делает { #what-it-does }

1. Обзор сеанса запуска:
```bash
python {skill_path}/scripts/session_manager.py --status {session-id}
```

2. Запустите анализ DAG:
```bash
python {skill_path}/scripts/dag_analyzer.py --status --session {session-id}
```

3. Ознакомьтесь с последними обновлениями доски объявлений:
```bash
python {skill_path}/scripts/board_manager.py --read progress
```

## Выходной формат { #output-format }

```
Session: 20260317-143022 (running)
Task: Optimize API response time below 100ms
Agents: 3 | Base: dev

AGENT    BRANCH                                        COMMITS  STATUS     LAST UPDATE
agent-1  hub/20260317-143022/agent-1/attempt-1         3        frontier   2026-03-17 14:35:10
agent-2  hub/20260317-143022/agent-2/attempt-1         5        frontier   2026-03-17 14:36:45
agent-3  hub/20260317-143022/agent-3/attempt-1         2        frontier   2026-03-17 14:34:22

Recent Board Activity:
  [progress] agent-1: Implemented caching, running tests
  [progress] agent-2: Hash map approach working, benchmarking
  [results]  agent-2: Final result posted
```

Пример вывода для задачи содержимого:

```
Session: 20260317-151200 (running)
Task: Draft 3 competing taglines for product launch
Agents: 3 | Base: dev

AGENT    BRANCH                                        COMMITS  STATUS     LAST UPDATE
agent-1  hub/20260317-151200/agent-1/attempt-1         2        frontier   2026-03-17 15:18:30
agent-2  hub/20260317-151200/agent-2/attempt-1         2        frontier   2026-03-17 15:19:12
agent-3  hub/20260317-151200/agent-3/attempt-1         1        frontier   2026-03-17 15:17:55

Recent Board Activity:
  [progress] agent-1: Storytelling angle draft complete, refining CTA
  [progress] agent-2: Benefit-led draft done, testing urgency variant
  [results]  agent-3: Final result posted
```

## После статуса { #after-status }

Если все агенты опубликовали результаты:
- Предложить `/hub:eval` для ранжирования результатов

Если некоторые агенты все еще запущены:
- Показать, что сделано, а что находится в процессе выполнения
- Предложите подождать или проверить еще раз позже
