---
title: "/karpathy-check — слэш-команда для ИИ-агентов разработки"
description: "Запустите ревью по 4-м принципам Karpathy для поэтапных изменений или последней фиксации. Проверяет сложность, разностный шум, скрытые допущения и. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /karpathy-check

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/karpathy-check.md">Источник</a></span>
</div>

<!-- canonical copy: engineering/karpathy-coder/commands/karpathy-check.md — keep in sync (root copy uses repo-root-relative script paths) -->

# /karpathy-check { #karpathy-check }

Ревью ваши поэтапные изменения (или последнюю фиксацию) в соответствии с 4 принципами кодирования Karpathy.

## Использование { #usage }

```
/karpathy-check                 # review staged changes
/karpathy-check --last-commit   # review the most recent commit
```

## Что он запускает { #what-it-runs }

1. **Принцип №2 (простота):** `engineering/karpathy-coder/skills/karpathy-coder/scripts/complexity_checker.py` во всех измененных файлах — обнаруживает чрезмерную инженерию, преждевременные абстракции, глубокую вложенность, длинные функции
2. **Принцип №3 (хирургический):** `engineering/karpathy-coder/skills/karpathy-coder/scripts/diff_surgeon.py` в diff — обнаруживает изменения только для комментариев, шум пробелов, смещение стиля, рефакторинг по ходу
3. **Принципы №1 + №4 (Мышление + цели):** `karpathy-reviewer` агент считывает разницу и применяет проверку на основе человеческого суждения - скрытые предположения, пропущенная проверка

## Выход { #output }

Структурированный отчет с вердиктами по каждому принципу и конкретными рекомендациями по исправлению на линейном уровне.

## Когда запускать { #when-to-run }

- Перед фиксацией (улавливает шум и чрезмерное усложнение на ранней стадии)
- После завершения функции (проверка работоспособности перед PR)
- Когда вы подозреваете, что LLM что-то перекодировал

## Саб-агент { #sub-agent }

Отправляет `karpathy-reviewer` агент. Видишь `agents/karpathy-reviewer.md`.

## Сценарии { #scripts }

- `engineering/karpathy-coder/skills/karpathy-coder/scripts/complexity_checker.py`
- `engineering/karpathy-coder/skills/karpathy-coder/scripts/diff_surgeon.py`
- `engineering/karpathy-coder/skills/karpathy-coder/scripts/assumption_linter.py`
- `engineering/karpathy-coder/skills/karpathy-coder/scripts/goal_verifier.py`

## Ссылка на Скилл { #skill-reference }

→ `engineering/karpathy-coder/skills/karpathy-coder/SKILL.md`
