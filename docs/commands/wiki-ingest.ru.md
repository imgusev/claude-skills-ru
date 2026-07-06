---
title: "/wiki-ingest — слэш-команда для ИИ-агентов разработки"
description: "Загрузите исходный файл из raw/ в LLM Wiki — прочитайте, обсудите, напишите сводную страницу, обновите перекрестные ссылки на 5-15 страницах. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /wiki-ingest

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/wiki-ingest.md">Источник</a></span>
</div>

<!-- canonical copy: engineering/llm-wiki/commands/wiki-ingest.md — keep in sync (root copy uses repo-root-relative script paths) -->

# /вики-проглатывание { #wiki-ingest }

Добавьте новый источник в LLM Wiki. Это наиболее часто используемая команда.

Последовательность действий: прочитайте источник → обсудите с вами TL; DR и ключевые утверждения → напишите страницу с кратким изложением источника → обновите страницу каждой соответствующей сущности и концепции → отметьте противоречия → обновите `index.md` → добавить к `log.md`.

Типичный прием затрагивает ** 5-15 страниц вики**. Вы (пользователь) находитесь в цикле: отправитель предлагает изменения и ждет вашего подтверждения, прежде чем писать.

## Использование { #usage }

```
/wiki-ingest <path>
/wiki-ingest raw/papers/monosemanticity.pdf
/wiki-ingest raw/articles/2026-04-01-interpretability-post.md
```

## Что происходит { #what-happens }

1. **Подготовка** — запуски `engineering/llm-wiki/skills/llm-wiki/scripts/ingest_source.py` чтобы получить заголовок, предварительный просмотр и предлагаемый краткий путь
2. **Читать** — считывает исходный код напрямую
3. **Обсудить** — отчеты TL;DR, ключевые претензии, какие страницы будут затронуты, любые противоречия
4. **Подтвердить** — ожидает вашего разрешения (или перенаправляет)
5. **Написать** — создает резюме источника, обновляет 5-15 страниц, помечает противоречия
6. **Индекс** — запускается `engineering/llm-wiki/skills/llm-wiki/scripts/update_index.py` или редактирует `wiki/index.md` встроенный
7. **Log** — запускается `engineering/llm-wiki/skills/llm-wiki/scripts/append_log.py --op ingest --title "<title>"`
8. **Отчет** — маркированные викилинки на каждую затронутую страницу

## Саб-агент { #sub-agent }

Эта команда отправляет `wiki-ingestor` саб-агент для тяжелой работы. Видишь `agents/wiki-ingestor.md`.

## Сценарии { #scripts }

- `engineering/llm-wiki/skills/llm-wiki/scripts/ingest_source.py` — подготовка исходного кода (метаданные + предварительный просмотр)
- `engineering/llm-wiki/skills/llm-wiki/scripts/update_index.py` — восстановить индекс
- `engineering/llm-wiki/skills/llm-wiki/scripts/append_log.py` — регистрируйте прием

## Правила { #rules }

- Источник должен находиться внутри хранилища `raw/` слой. Если это не так, команда попросит вас сначала переместить ее.
- `raw/` является неизменяемым — потребитель только читает.
- Если страница сводки уже существует, пользователь переходит в режим **слияния** и добавляет раздел для повторного ввода.

## Ссылка на Скилл { #skill-reference }

→ `engineering/llm-wiki/skills/llm-wiki/SKILL.md`
→ `engineering/llm-wiki/skills/llm-wiki/references/ingest-workflow.md`
