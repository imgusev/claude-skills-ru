---
name: wiki-query
description: "Запросите вики— раздел LLM - читает index.md сначала просматривает 3-10 релевантных страниц, синтезирует ответ со встроенными цитатами [[викилинка]] и предлагает отправить ответ обратно в виде новой страницы сравнения или обобщения. Использование /вики-запрос \"<вопрос>\""
---
<!-- canonical copy: engineering/llm-wiki/commands/wiki-query.md — keep in sync (root copy uses repo-root-relative script paths) -->

# /wiki-query { #wiki-query }

Задайте вопрос вики. Библиотекарь читает `index.md` сначала выбирает релевантные страницы по категориям, обобщает ответ с цитатами и предлагает отправить ответ обратно в вики, чтобы ваши исследования были более комплексными.

## Использование { #usage }

```
/wiki-query "<your question>"
/wiki-query "what does the wiki say about sparse autoencoders?"
/wiki-query "compare monosemanticity and polysemanticity across my sources"
/wiki-query "which sources disagree on scaling laws?"
/wiki-query "give me a comparison table of SAE vs linear probing"
```

## Что происходит { #what-happens }

1. **Индекс-первое чтение** — считывает `wiki/index.md` чтобы найти соответствующие страницы
2. ** Подробное описание ** — прочитывает 3-10 страниц полностью (синтез + концепции + источники + сущности)
3. **Переходить по ссылкам** — оппортунистически переходить по викилинкам между страницами
4. **Резервный поиск** — если индекса недостаточно, выполняется `engineering/llm-wiki/skills/llm-wiki/scripts/wiki_search.py` (BM25)
5. **Синтезировать** — составляет прямой ответ + вспомогательные детали + встроенный `[[sources/xxx]]` цитаты + раздел "Похожие страницы"
6. **Предложение вернуть файл обратно** — спрашивает, следует ли сохранить это как новую вики-страницу (обычно в `comparisons/` или `synthesis/`)

## Выходные форматы { #output-formats }

Формат ответа соответствует формату вопроса:

| Форма вопроса | Выход |
|---|---|
| "Что такое X?" | Объяснение Markdown с цитатами |
| "А против Б" | Сравнительная таблица |
| "Дайте мне колоду слайдов на X" | Синтез Markdown → `/wiki-marp` для рендеринга |
| "Наметьте тренд в X" | Скрипт на Python + сохраненная диаграмма в `wiki/assets/charts/` |

## Саб-агент { #sub-agent }

Эта команда отправляет `wiki-librarian` саб-агент. Видишь `agents/wiki-librarian.md`.

## Сценарии { #scripts }

- `engineering/llm-wiki/skills/llm-wiki/scripts/wiki_search.py` — Резервный поиск BM25
- `engineering/llm-wiki/skills/llm-wiki/scripts/append_log.py` — записанные в журнал ответы

## Правила { #rules }

- ** Сначала прочитайте индекс.** Никакого grep-всего.
- **В каждой заявке приводится ссылка на страницу** с `[[wikilink]]`.
- ** Предложите отправить ответ обратно ** — но только для ответов по существу, которые стоит сохранить.

## Ссылка на Скилл { #skill-reference }

→ `engineering/llm-wiki/skills/llm-wiki/SKILL.md`
→ `engineering/llm-wiki/skills/llm-wiki/references/query-workflow.md`
