---
title: "/wiki-lint — слэш-команда для ИИ-агентов разработки"
description: "Запустите проверку работоспособности LLM Wiki vault — механические проверки (сироты, неработающие ссылки, устаревшие страницы, отсутствующий. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /wiki-lint

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/wiki-lint.md">Источник</a></span>
</div>

<!-- canonical copy: engineering/llm-wiki/commands/wiki-lint.md — keep in sync (root copy uses repo-root-relative script paths) -->

# /wiki-lint { #wiki-lint }

Работоспособность -проверьте вики. Всплывают бесхозные страницы, неработающие викилинки, устаревшие утверждения, отсутствующий основной материал, противоречия и структурный дрейф. **Сообщает, а не исправляет молча** — вы сами решаете, что изменить.

Выполняйте это еженедельно, после пакетного проглатывания и всегда перед тем, как поделиться wiki.

## Использование { #usage }

```
/wiki-lint
/wiki-lint --stale-days 60
/wiki-lint --log-gap-days 7
```

## Что происходит { #what-happens }

### Проход 1 — Механический (скрипты) { #pass-1--mechanical-scripts }

- `engineering/llm-wiki/skills/llm-wiki/scripts/lint_wiki.py` — сироты, неработающие ссылки, устаревшие страницы, отсутствующий заголовок, дублирующиеся заголовки, пробел в журнале
- `engineering/llm-wiki/skills/llm-wiki/scripts/graph_analyzer.py` — концентраторы, приемники, подключенные компоненты, статистика графиков

### Проход 2 — Семантический (LLM читает и думает) { #pass-2--semantic-llm-reads-and-thinks }

- Противоречия между недавно обновленными страницами
- Устаревшие утверждения заменены новыми источниками
- Концепции, упомянутые простым текстом на более чем 3 страницах без их собственной страницы
- Пробелы в перекрестных ссылках (объекты упомянуты, но не связаны викиликсом)
- Смещение индекса (index.md не синхронизирован с wiki/)

### Проход 3 — Отчет { #pass-3--report }

Отчет Markdown, сгруппированный по степени серьезности:

```markdown
# Wiki lint — <date>

**Total pages:** N  **Components:** N  **Last log:** <date>

## Found
- ⚠️ <N> contradictions (list)
- <N> orphans
- <N> broken links
- <N> stale pages
- ...

## Suggested actions
1. Investigate contradiction between [[sources/a]] and [[sources/b]]
2. Create concept page for "<name>"
3. Fix broken link in [[concepts/x]]
4. Re-ingest [[sources/c]] — stale + contradicted
5. ...
```

Затем добавляет `lint` вход в `log.md`.

## Саб-агент { #sub-agent }

Отправляет `wiki-linter` саб-агент. Видишь `agents/wiki-linter.md`.

## Сценарии { #scripts }

- `engineering/llm-wiki/skills/llm-wiki/scripts/lint_wiki.py`
- `engineering/llm-wiki/skills/llm-wiki/scripts/graph_analyzer.py`
- `engineering/llm-wiki/skills/llm-wiki/scripts/append_log.py`

## Частота { #frequency }

| Триггер | Пройти |
|---|---|
| Еженедельно | Только механический — быстрый |
| После приема партии | Полный (механический + семантический) |
| Ежемесячно | Полный + структурный ревью |
| Прежде чем поделиться | Полный + дополнительный ревью |

## Ссылка на Скилл { #skill-reference }

→ `engineering/llm-wiki/skills/llm-wiki/SKILL.md`
→ `engineering/llm-wiki/skills/llm-wiki/references/lint-workflow.md`
