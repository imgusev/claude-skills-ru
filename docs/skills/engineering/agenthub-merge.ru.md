---
title: "/hub:merge — Победитель слияния { #hubmerge--merge-winner } — Агентский скилл для Codex и OpenClaw"
description: "Объедините ветку победившего агента с базой, заархивируйте проигравших и очистите рабочие деревья. Используйте, когда пользователь запускает. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /hub:merge — Победитель слияния { #hubmerge--merge-winner }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `merge`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/agenthub/skills/merge/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Объедините ветку лучшего агента с базовой веткой, заархивируйте потерянные ветви с помощью тегов git и очистите рабочие деревья.

## Использование { #usage }

```
/hub:merge                                       # Merge winner of latest session
/hub:merge 20260317-143022                       # Merge winner of specific session
/hub:merge 20260317-143022 --agent agent-2       # Explicitly choose winner
```

## Что он делает { #what-it-does }

### 1. Определите победителя { #1-identify-winner }

Если `--agent` указано, используйте это. В противном случае используйте агента с рейтингом #1 из самых последних `/hub:eval`.

### 2. Победитель слияния { #2-merge-winner }

```bash
git checkout {base_branch}
git merge --no-ff hub/{session-id}/{winner}/attempt-1 \
  -m "hub: merge {winner} from session {session-id}

Task: {task}
Winner: {winner}
Session: {session-id}"
```

### 3. Архив Неудачников { #3-archive-losers }

За каждого не выигравшего агента:

```bash
# Create archive tag (preserves commits forever)
git tag hub/archive/{session-id}/{agent-id} hub/{session-id}/{agent-id}/attempt-1

# Delete branch ref (commits preserved via tag)
git branch -D hub/{session-id}/{agent-id}/attempt-1
```

### 4. Очистите рабочие деревья { #4-clean-up-worktrees }

```bash
python {skill_path}/scripts/session_manager.py --cleanup {session-id}
```

### 5. Опубликуйте резюме слияния { #5-post-merge-summary }

Писать `.agenthub/board/results/merge-summary.md`:

```markdown
---
author: coordinator
timestamp: {now}
channel: results
---

## Merge Summary

- **Session**: {session-id}
- **Winner**: {winner}
- **Merged into**: {base_branch}
- **Archived**: {loser-1}, {loser-2}, ...
- **Worktrees cleaned**: {count}
```

### 6. Обновите состояние { #6-update-state }

```bash
python {skill_path}/scripts/session_manager.py --update {session-id} --state merged
```

## Безопасность { #safety }

- ** Подтвердите с пользователем ** перед объединением — сначала покажите сводку различий
- ** Никогда не нажимайте принудительно ** — слияние всегда `--no-ff` для ясной истории
- **Архивировать, не удалять** — коммиты потерянных агентов сохраняются с помощью тегов
- **Очистите рабочие деревья** — не оставляйте бесхозные каталоги на диске

## После слияния { #after-merge }

Сообщите пользователю:
- Победитель объединился в `{base_branch}`
- Проигравшие заархивированы с тегами `hub/archive/{session-id}/agent-{N}`
- Рабочие деревья очищены
- Состояние сеанса: `merged`
