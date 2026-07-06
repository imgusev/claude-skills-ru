---
title: "/cs-litreview — слэш-команда для ИИ-агентов разработки"
description: "/cs:litreview <исследовательский вопрос> — ориентация на академическую литературу. Прием с помощью Grill-me (вопрос + фреймворк + глубина), поиск по. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-litreview

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/research/litreview/commands/cs-litreview.md">Источник</a></span>
</div>


**Команда:** `/cs:litreview <research question>`

Тот `cs-litreview` персона выпускает стратегически спланированный мини-ревью литературы в виде 8 разделов `.docx` руководство по исследованию.

## Когда запускать { #when-to-run }

- Начинаю исследование в незнакомой области
- Написание статьи, которая нуждается в изучении современной литературы
- Составление карты "рельефа местности" перед тем, как определиться с направлением исследований
- Нужен составленный куратором список литературы с ключевыми авторами + основополагающими статьями + пробелами

## Когда не запускать (прямой поиск) { #when-not-to-run-search-directly }

- Ищете ОДНУ конкретную статью (просто найдите PubMed / OpenAlex — или Консенсус, если вы им пользуетесь)
- Быстрый поиск без необходимости синтеза
- Область, которую вы уже хорошо знаете, и вам просто нужен список последних работ

## Принудительный прием пищи (3 вопроса, по одному за раз) { #forcing-intake-3-questions-one-at-a-time }

| Вопрос | Спрашивает | Значение по умолчанию, если принудительный выбор |
|---|---|---|
| Вопрос 1 | Исследовательский вопрос (1-2 предложения, конкретные) | отказывается расплывчато; "Искусственный интеллект в медицине" один раз отодвигается на второй план. |
| Q2 | Фреймворк: PICO / SPIDER / Декомпозиция / гибрид / на ваш выбор | "выбирай сам" (рекомендации по скиллу из Q1) |
| Вопрос 3 | Ориентировочная глубина: Быстрая (5) / стандартная (10) / Глубокая (20) | повторно подтверждено на контрольно-пропускном пункте после этапа 2 |

## Что Вы получаете { #what-you-get }

После приема на этапе 0 + разведки на этапе 1 + фреймворка на этапе 2 + интерактивной контрольной точки + поиска на этапе 3:

**`research_guide_<topic>_<date>.docx`** с 8 секциями:

1. ** Обзор темы ** — один сжатый абзац
2. ** Начните здесь — Порядок чтения в приоритетном порядке ** — 5-7 статей с гиперссылками (лучший- ревью → основополагающий → пограничный → пробел)
3. ** Как поле попало сюда ** — хронологическое повествование + таблица временных рамок
4. ** Руководства по подразделам** — по одному на подраздел (по 4 части в каждом: обобщение / ключевые статьи / поисковые термины / логические строки)
5. **Ключевые исследовательские группы** — 3-5 лучших авторов/groups с представительными документами
6. **Открытые вопросы и пробелы** — методологические / демографические / концептуальные
7. ** Библиография** — в алфавитном порядке, с гиперссылками, каждая встроенная цитата соответствует
8. ** Журнал аудита** — таблица поиска + количество использованных полос поиска (бесплатно / free+консенсус)

## Интерактивная контрольная точка (в середине выполнения) { #interactive-checkpoint-mid-run }

После фазы 2 (выбран фреймворк, сгенерированы подобласти) скилл ** останавливается** с промптом принудительных настроек:

```
Framework breakdown:
| {Component} | How it maps to your topic | Proposed sub-area |
|---|---|---|
| Population | ... | Sub-area 1: ... |
| Intervention | ... | Sub-area 2: ... |
| Comparison | ... | Sub-area 3: ... |
| Outcome | ... | Sub-area 4: ... |
| Cross-cutting | ... | Sub-area 5: ... |

Confirm depth (search lane: free — PubMed + OpenAlex, ~20 results per query per source):
  1. Quick scan (5 searches)
  2. Standard review (10 searches)
  3. Deep dive (20 searches)

Sub-area options:
  - Looks good — proceed
  - Adjust: add sub-area on [X]
  - Adjust: replace [Y] with [Z]
  - Restart with different framework
```

Это ** последний дешевый момент ** скорректировать курс до того, как будет израсходован бюджет поиска. Скилл отказывается запускать фазу 3 без явного выбора пользователя.

## Дисциплина (Соглашение об исследовательском пакете) { #discipline-research-pack-convention }

- ** Один входной вопрос за ход. ** Никогда не связывайтесь.
- **Последовательные поисковые вызовы.** 1 вопрос/sec ограничение по ставке. НИКОГДА не распараллеливайте (любую полосу движения).
- **Проверка полосы движения в начале сеанса** — если инструменты согласованного MCP недоступны, используйте свободную полосу движения; не пытайтесь определить уровень. Лейн доложил об этом на контрольно-пропускном пункте.
- ** Остановка на контрольно-пропускном пункте.** Фаза 3 без подтверждения запрещена.
- **Дисциплина источника** — цитируйте только результаты поиска ЭТОЙ сессии. Учебные знания, помеченные `[Not from search]`.
- ** Отслеживание по трем показателям ** — поисковые запросы / уникальные статьи / цитируемые.
- **Повторите попытку один раз через 3 секунды** — затем войдите в систему. 3 последовательных сбоя → остановка.

## Воркфлоу { #workflow }

```bash
# Phase 0 intake (Q1-Q3 one at a time)
python ../skills/litreview/scripts/citation_tracker.py --action start --session NAME
python ../skills/litreview/scripts/framework_recommender.py --question "<Q1>"

# Phase 1 recon (1 free-lane search; record sent + received; add Consensus if connected)
python ../skills/litreview/scripts/free_search.py --query "<broad Q1>" --source both --max 20
# Phase 2 framework + sub-area generation
# CHECKPOINT — wait for user

# Phase 3 searches (sequential, 1 q/sec, budget per tier):
#   5/10/20 searches across sub-areas + review + era-gated + follow-up

# Phase 4 cross-search aggregation + DOCX
python ../skills/litreview/scripts/cross_search_aggregator.py --session NAME
# Generate DOCX via Node.js docx library
python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).testzip()" output.docx  # zip-integrity check; then confirm required sections present

python ../skills/litreview/scripts/citation_tracker.py --action close --session NAME
```

## Фразы-триггеры (автоматический вызов без /cs:) { #trigger-phrases-auto-invoke-without-cs }

- "litreview на [тема]"
- "ревью литературы по [тема]"
- "Я начинаю ревью литературы по X"
- "Я пишу статью о X"
- "помоги мне исследовать X"
- "Я провожу исследование по X"
- "можете ли вы помочь мне исследовать X"

** Не запускайте триггер для:** одиночных разовых поисковых запросов в документе - это обычный запрос PubMed/OpenAlex (или консенсусный).

## Отклоненные анти-паттерны { #anti-patterns-rejected }

- Распараллеливание поисковых вызовов (любая полоса)
- Пропуск интерактивной контрольной точки
- Дополнять тонкие результаты знаниями о тренировках
- Неисполнение обязательств по non-PICO без обоснования
- Цитирование статей в чате, которые не были получены в результате поиска в этой сессии
- Попытка определения уровня согласованного плана (удалено — единственная проверка заключается в том, доступны ли инструменты согласованного MCP)
- Обработка консенсуса по мере необходимости (по умолчанию используется свободная полоса)
- Пропуск поисковых запросов с гейтами, привязанных к эпохе, в стандартном/deep бюджеты
- Пропуск результатов перекрестного поиска (повторные обращения, повторяющиеся авторы)
- Усечение исходных URL-адресов

## Связанный { #related }

- Агент: [`cs-litreview`](https://github.com/imgusev/claude-skills-ru/tree/main/research/litreview/agents/cs-litreview.md)
- Скилл: [`litreview`](https://github.com/imgusev/claude-skills-ru/tree/main/research/litreview/skills/litreview/SKILL.md)
- Спецификация источника: [`megaprompts/09-litreview-megaprompt.md`](https://github.com/imgusev/claude-skills-ru/tree/main/megaprompts/09-litreview-megaprompt.md)
- Родной брат: `/cs:pulse` (исследовательский пакет)
- Будущие братья и сестры: `/cs:grants`, `/cs:patent`, `/cs:dossier`, `/cs:syllabus`

---

**Версия:** 1.0.0
**Источник:** Прямое преобразование Path-B в `megaprompts/09-litreview-megaprompt.md`
