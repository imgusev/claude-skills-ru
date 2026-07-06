---
title: "/wiki-log — слэш-команда для ИИ-агентов разработки"
description: "Показывать последние записи из вики-журнала LLM (wiki/log.md). Использует стандартизированный формат заголовка ## [ГГГГ-ММ-ДД], поэтому работает grep. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /wiki-log

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/wiki-log.md">Источник</a></span>
</div>

<!-- canonical copy: engineering/llm-wiki/commands/wiki-log.md — keep in sync -->

# /wiki-log { #wiki-log }

Показывать последние записи из `wiki/log.md`. Каждая операция LLM в вики оставляет стандартизированную запись:

```
## [YYYY-MM-DD] <op> | <title>
<optional detail>
```

## Использование { #usage }

```
/wiki-log                            # last 10 entries
/wiki-log --last 20
/wiki-log --op ingest --last 10      # only ingest entries
/wiki-log --op lint                  # recent lint passes
/wiki-log --since 2026-04-01
```

## Что он делает { #what-it-does }

Разбирает `wiki/log.md` и печатает соответствующие записи. Участие LLM не требуется — это, по сути,:

```bash
grep "^## \[" wiki/log.md | tail -N
```

...плюс дополнительные фильтры для типа операции и диапазона дат.

## Допустимые операции { #valid-ops }

- `ingest` — источник был прочитан и интегрирован
- `query` — на вопрос был дан ответ (при отправке обратно)
- `lint` — проведена проверка работоспособности
- `create` — новая страница была создана вне процесса загрузки
- `update` — страница была обновлена вне процесса загрузки
- `delete` — страница была удалена
- `note` — примечание в свободной форме (отмечены противоречия, изменения в тезисах и т.д.)

## Пример вывода { #example-output }

```
## [2026-04-11] lint | weekly health check
3 contradictions, 12 orphans, 2 broken links. Fixed broken links; left contradictions for next session.

## [2026-04-10] ingest | Anthropic Monosemanticity
Added sources/monosemanticity.md. Updated concepts/sparse-autoencoder, concepts/polysemanticity, entities/anthropic.

## [2026-04-09] query | SAE vs probing
Filed back to comparisons/sae-vs-probing.md.
```

## Сценарии { #scripts }

- Использует `grep` + `tail` непосредственно на `wiki/log.md`. Специальный скрипт не требуется; в этом смысл стандартизированного формата заголовка.

## Ссылка на Скилл { #skill-reference }

→ `engineering/llm-wiki/skills/llm-wiki/SKILL.md`
