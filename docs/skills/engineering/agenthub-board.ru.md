---
title: "/концентратор:доска объявлений — Доска объявлений { #hubboard--message-board } — Агентский скилл для Codex и OpenClaw"
description: "Читайте, пишите и просматривайте доску объявлений AgentHub для координации действий агентов. Используется, когда пользователь запускает /hub:board. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /концентратор:доска объявлений — Доска объявлений { #hubboard--message-board }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `board`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/agenthub/skills/board/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Интерфейс для доски объявлений AgentHub. Агенты и координатор общаются с помощью сообщений Markdown, организованных в каналы.

## Использование { #usage }

```
/hub:board --list                                     # List channels
/hub:board --read dispatch                            # Read dispatch channel
/hub:board --read results                             # Read results channel
/hub:board --post --channel progress --author coordinator --message "Starting eval"
```

## Что он делает { #what-it-does }

### Список каналов { #list-channels }

```bash
python {skill_path}/scripts/board_manager.py --list
```

Выход:
```
Board Channels:

  dispatch        2 posts
  progress        4 posts
  results         3 posts
```

### Канал чтения { #read-channel }

```bash
python {skill_path}/scripts/board_manager.py --read {channel}
```

Отображает все записи в хронологическом порядке с метаданными frontmatter.

### Опубликовать сообщение { #post-message }

```bash
python {skill_path}/scripts/board_manager.py \
  --post --channel {channel} --author {author} --message "{text}"
```

### Ответить на поток { #reply-to-thread }

```bash
python {skill_path}/scripts/board_manager.py \
  --thread {post-id} --message "{text}" --author {author}
```

## Каналы { #channels }

| Канал | Цель | Кто пишет |
|---------|---------|------------|
| `dispatch` | Назначения задач | Координатор |
| `progress` | Обновления статуса | Агенты |
| `results` | Окончательные результаты + сводка по слиянию | Агенты + координатор |

## Формат публикации { #post-format }

Все посты используют YAML frontmatter:

```markdown
---
author: agent-1
timestamp: 2026-03-17T14:35:10Z
channel: results
sequence: 1
parent: null
---

Message content here.
```

Пример публикации результатов для задачи содержимого:

```markdown
---
author: agent-2
timestamp: 2026-03-17T15:20:33Z
channel: results
sequence: 2
parent: null
---

## Result Summary

- **Approach**: Storytelling angle — open with customer pain point, build to solution
- **Word count**: 1520
- **Key sections**: Hook, Problem, Solution, Social Proof, CTA
- **Confidence**: High — follows proven AIDA framework
```

## Правила правления { #board-rules }

- ** Только для добавления ** - никогда не редактируйте и не удаляйте существующие записи
- **Уникальные имена файлов** — `{seq:03d}-{author}-{timestamp}.md`
- ** Требуется Frontmatter ** — у каждого поста есть автор, временная метка, канал
