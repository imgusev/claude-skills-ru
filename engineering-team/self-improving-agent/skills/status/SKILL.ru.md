---
name: "status"
description: "Дашборд работоспособности памяти, показывающий количество строк, файлы тем, емкость, устаревшие записи и рекомендации. Используется, когда пользователь запускает /si:status или спрашивает, насколько заполнена или исправна память агента."
---

# /si:status — Дашборд работоспособности памяти { #sistatus--memory-health-dashboard }

Краткий обзор состояния памяти вашего проекта во всех системах памяти.

## Использование { #usage }

```
/si:status                    # Full dashboard
/si:status --brief            # One-line summary
```

## О чем он сообщает { #what-it-reports }

### Шаг 1: Найдите все файлы в памяти { #step-1-locate-all-memory-files }

```bash
# Auto-memory directory
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"

# Count lines in MEMORY.md
wc -l "$MEMORY_DIR/MEMORY.md" 2>/dev/null || echo "0"

# List topic files
ls "$MEMORY_DIR/"*.md 2>/dev/null | grep -v MEMORY.md

# CLAUDE.md
wc -l ./CLAUDE.md 2>/dev/null || echo "0"
wc -l ~/.claude/CLAUDE.md 2>/dev/null || echo "0"

# Rules directory
ls .claude/rules/*.md 2>/dev/null | wc -l
```

### Шаг 2: Проанализируйте пропускную способность { #step-2-analyze-capacity }

| Метрика | Здоровый | Предупреждение | Критический |
|--------|---------|---------|----------|
| MEMORY.md линии | < 120 | 120-180 | > 180 |
| CLAUDE.md линии | < 150 | 150-200 | > 200 |
| Файлы тем | 0-3 | 4-6 | > 6 |
| Устаревшие записи | 0 | 1-3 | > 3 |

### Шаг 3: Быстрая проверка на устаревание { #step-3-quick-stale-check }

Для каждого MEMORY.md запись, ссылающаяся на путь к файлу:
```bash
# Verify referenced files still exist
grep -oE '[a-zA-Z0-9_/.-]+\.(ts|js|py|md|json|yaml|yml)' "$MEMORY_DIR/MEMORY.md" | while read f; do
  [ ! -f "$f" ] && echo "STALE: $f"
done
```

### Шаг 4: Вывод { #step-4-output }

```
📊 Memory Status

  Auto-Memory (MEMORY.md):
    Lines:        {{n}}/200 ({{bar}}) {{emoji}}
    Topic files:  {{count}} ({{names}})
    Last updated: {{date}}

  Project Rules:
    CLAUDE.md:    {{n}} lines
    Rules:        {{count}} files in .claude/rules/
    User global:  {{n}} lines (~/.claude/CLAUDE.md)

  Health:
    Capacity:     {{healthy/warning/critical}}
    Stale refs:   {{count}} (files no longer exist)
    Duplicates:   {{count}} (entries repeated across files)

  {{if recommendations}}
  💡 Recommendations:
    - {{recommendation}}
  {{endif}}
```

### Краткий режим { #brief-mode }

```
/si:status --brief
```

Выход: `📊 Memory: {{n}}/200 lines | {{count}} rules | {{status_emoji}} {{status_word}}`

## Интерпретация { #interpretation }

- **Зеленый (< 60%)**: Много места. Автоматическая память работает хорошо.
- ** Желтый (60-90%)**: Насыщается. Подумайте о том, чтобы бежать `/si:review` для продвижения по службе или наведения порядка.
- **Красный (> 90%)**: Почти полная мощность. Автоматическая память может начать удалять старые записи. Бежать `/si:review` сейчас.

## Советы { #tips }

- Бежать `/si:status --brief` в качестве быстрой проверки в любое время
- Если емкость желтая+, запустите `/si:review` для определения кандидатов на продвижение по службе
- Устаревшие записи занимают много места — удаляются ссылки на файлы, которые больше не существуют
- Файлы тем в порядке — Клод создает их, чтобы сохранить MEMORY.md менее 200 строк
