---
title: "/hub:eval — Оценка результатов работы агента { #hubeval--evaluate-agent-results } — Агентский скилл для Codex и OpenClaw"
description: "Оценивайте и ранжируйте результаты агентов по показателям или LLM judge для сеанса AgentHub. Используется, когда пользователь запускает /hub:eval или. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /hub:eval — Оценка результатов работы агента { #hubeval--evaluate-agent-results }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `eval`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/agenthub/skills/eval/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Ранжируйте все результаты агента за сеанс. Поддерживает оценку на основе показателей (запуск команды), оценку LLM (сравнение различий) или гибрид.

## Использование { #usage }

```
/hub:eval                           # Eval latest session using configured criteria
/hub:eval 20260317-143022           # Eval specific session
/hub:eval --judge                   # Force LLM judge mode (ignore metric config)
```

## Что он делает { #what-it-does }

### Режим метрики (настроена команда eval) { #metric-mode-eval-command-configured }

Запустите команду оценки в рабочем дереве каждого агента:

```bash
python {skill_path}/scripts/result_ranker.py \
  --session {session-id} \
  --eval-cmd "{eval_cmd}" \
  --metric {metric} --direction {direction}
```

Выход:
```
RANK  AGENT       METRIC      DELTA      FILES
1     agent-2     142ms       -38ms      2
2     agent-1     165ms       -15ms      3
3     agent-3     190ms       +10ms      1

Winner: agent-2 (142ms)
```

### Режим судьи LLM (без команды eval или флага --judge) { #llm-judge-mode-no-eval-command-or---judge-flag }

Для каждого агента:
1. Получите разницу: `git diff {base_branch}...{agent_branch}`
2. Прочтите сообщение о результатах работы агента из `.agenthub/board/results/agent-{i}-result.md`
3. Сравните все различия и ранжируйте по:
   - **Корректность** — Решает ли это задачу?
   - **Простота** — Чем меньше изменено строк, тем лучше (при одинаковой корректности)
   - **Качество** — Чистое исполнение, хорошая структура, отсутствие регрессий

Приведите рейтинги с обоснованием.

Пример вывода LLM judge для задачи по содержанию:
```
RANK  AGENT    VERDICT                               WORD COUNT
1     agent-1  Strong narrative, clear CTA            1480
2     agent-3  Good data points, weak intro           1520
3     agent-2  Generic tone, no differentiation       1350

Winner: agent-1 (strongest narrative arc and call-to-action)
```

### Гибридный режим { #hybrid-mode }

1. Сначала запустите оценку показателя
2. Если ведущие агенты находятся в пределах 10% друг от друга, используйте LLM judge для разрыва связей
3. Представлены как метрические, так и качественные рейтинги

## После оценки { #after-eval }

1. Обновить состояние сеанса:
```bash
python {skill_path}/scripts/session_manager.py --update {session-id} --state evaluating
```

2. Сообщите пользователю:
   - Ранжированные результаты с выделением победителя
   - Следующий шаг: `/hub:merge` чтобы объединить победителя
   - Или `/hub:merge {session-id} --agent {winner}` быть откровенным
