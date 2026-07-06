---
title: "/si:remember — Сохранять знания явно { #siremember--save-knowledge-explicitly } — Агентский скилл и плагин Codex"
description: "Явно сохраняйте важные знания в автоматической памяти с отметкой времени и контекстом. Используйте, когда обнаружение слишком важно, чтобы полагаться. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /si:remember — Сохранять знания явно { #siremember--save-knowledge-explicitly }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `remember`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/self-improving-agent/skills/remember/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Записывает явную запись в автоматическую память, когда что-то достаточно важно, и вы не хотите полагаться на то, что Клод заметит это автоматически.

## Использование { #usage }

```
/si:remember <what to remember>
/si:remember "This project's CI requires Node 20 LTS — v22 breaks the build"
/si:remember "The /api/auth endpoint uses a custom JWT library, not passport"
/si:remember "Reza prefers explicit error handling over try-catch-all patterns"
```

## Когда использовать { #when-to-use }

| Ситуация | Пример |
|-----------|---------|
| С трудом завоеванное понимание отладки | "Ошибки CORS на /api/upload вызваны CDN, а не серверной частью" |
| Соглашение о проекте, не входящее в CLAUDE.md | "Мы используем экспорт баррелей в src/components/" |
| Подвох, связанный с конкретным инструментом | "Шутка нуждается `--forceExit` флаг, или он зависает при тестировании базы данных" |
| Архитектурное решение | "Мы выбрали Drizzle вместо Prisma для типобезопасного SQL" |
| Предпочтения, которым ты хочешь научить Клода | "Не добавляйте комментарии, объясняющие очевидный код" |

## Воркфлоу { #workflow }

### Шаг 1: Проанализируйте полученные знания { #step-1-parse-the-knowledge }

Извлечение из пользовательских данных:
- **Что**: Конкретный факт или закономерность
- **Почему это важно**: Контекст (если предоставлен)
- **Сфера охвата**: Конкретный проект или глобальный?

### Шаг 2: Проверьте наличие дубликатов { #step-2-check-for-duplicates }

```bash
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"
grep -ni "<keywords>" "$MEMORY_DIR/MEMORY.md" 2>/dev/null
```

Если аналогичная запись существует:
- Покажите это пользователю
- Спросите: "Обновить существующую запись или добавить новую?"

### Шаг 3: Напишите в MEMORY.md { #step-3-write-to-memorymd }

Добавить в конец `MEMORY.md`:

```markdown
- {{concise fact or pattern}}
```

Делайте записи краткими — по возможности в одну строку. Для записей в автоматической памяти не нужны временные метки, идентификаторы или метаданные. Это заметки, а не записи в базе данных.

Если MEMORY.md составляет более 180 строк, предупредите пользователя:

```
⚠️ MEMORY.md is at {{n}}/200 lines. Consider running /si:review to free space.
```

### Шаг 4: Предложите продвижение по службе { #step-4-suggest-promotion }

Если знание звучит как правило (императивное, всегда/never, конвенция):

```
💡 This sounds like it could be a CLAUDE.md rule rather than a memory entry.
   Rules are enforced with higher priority. Want to /si:promote it instead?
```

### Шаг 5: Подтвердите { #step-5-confirm }

```
✅ Saved to auto-memory

  "{{entry}}"

  MEMORY.md: {{n}}/200 lines
  Claude will see this at the start of every session in this project.
```

## Что не следует использовать /si:remember для { #what-not-to-use-siremember-for }

- ** Временный контекст**: Используйте память сеанса или просто расскажите Клоду в разговоре
- **Принудительные правила**: Используйте `/si:promote` чтобы написать непосредственно в CLAUDE.md
- **Межпроектные знания**: Используйте `~/.claude/CLAUDE.md` для глобальных правил
- ** Конфиденциальные данные**: Никогда не храните учетные данные, токены или секреты в файлах памяти

## Советы { #tips }

- Будьте кратки — одна строка лучше абзаца
- Укажите конкретную команду или значение, а не только концепцию
  - ✅ "Стройте с помощью `pnpm build`, тесты с `pnpm test:e2e`"
  - ❌ "Проект использует pnpm для построения и тестирования"
- Если вы вспоминаете одно и то же дважды, поделитесь этим с другими CLAUDE.md
