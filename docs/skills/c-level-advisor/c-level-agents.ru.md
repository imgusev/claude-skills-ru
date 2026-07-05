---
title: "c-уровень - агенты — Команда руководителей в режиме основателя { #c-level-agents--founder-mode-executive-team } — Агентский скилл для руководителей"
description: "Команда руководителей в режиме основателя. 13 агентов cs-* C-suite (финансовый директор, CMO, CRO, CPO, исполнительный директор, CHRO, CISO. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# c-уровень - агенты — Команда руководителей в режиме основателя { #c-level-agents--founder-mode-executive-team }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `c-level-agents`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/c-level-agents/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


Виртуальный C-suite, предоставляемый с помощью слэш-команд и агентов персоны.

## Ключевые слова { #keywords }

режим основателя, виртуальный c-suite, команда руководителей, зал заседаний, рабочее время, ревью финансового директора, ревью cmo, стратегический спринт, регистрация решений, консенсус между моделями, персоны агентов, начальник штаба, форсирующие вопросы

## Что предоставляет этот плагин { #what-this-plugin-provides }

### 13 Агентов cs-* (в `agents/`) { #13-cs--agents-in-agents }

Каждый агент использует существующий скилл уровня c и добавляет:
- Отчетливый когнитивный голос (числовой скептик, повествователь в первую очередь и т.д.)
- Форсирующие вопросы, относящиеся к конкретной роли
- Оркестрация воркфлоу, привязанная к инструментам Python для работы с скиллами
- Выходной шаблон: Итог → Что → Почему → Как действовать → Ваше решение

Видишь [`references/persona-voices.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/persona-voices.md) для голосовых характеристик.

### 21 /cs:* Слэш-команды (в `skills/`) { #21-cs-slash-commands-in-skills }

**Принуждение-вопрос о времени работы офиса (12):**
- `/cs:office-hours` — Прием 6 вопросов в стиле YC
- `/cs:cfo-review` — удельная экономичность, взлетно-посадочная полоса, разбавление
- `/cs:cmo-review` — ICP, окупаемость CAC, позиционирование
- `/cs:cpo-review` — РАЙС, JTBD, Северная звезда, PMF
- `/cs:cro-review` — охват пайплайна, коэффициент выигрыша, NRR
- `/cs:cto-review` — архитектурный риск, масштабирование утеса
- `/cs:ciso-review` — модель угрозы, радиус поражения, соответствие требованиям
- `/cs:gc-review` — контракты, интеллектуальная собственность, нормативные акты, временные таблицы
- `/cs:cdo-review` — обучение - права на данные, информационные продукты, информационные активы
- `/cs:caio-review` — выбор модели, оценки, риск ИИ, затраты на ИИ
- `/cs:cco-review` — Разложение GRR/NRR, первопричина оттока, охват CS
- `/cs:vpe-review` — Показатели DORA, время цикла, воронка найма на английском языке, структура команды

**Пайплайн стратегического спринта (5):**
- `/cs:brief` → `/cs:boardroom` → `/cs:decide` → `/cs:execute` → `/cs:post-mortem`

**Мета + безопасность (4):**
- `/cs:founder-mode` — автоматические маршруты к нужной C-роли
- `/cs:onboard` — интервью с основателем → `company-context.md`
- `/cs:cross-eval` — консенсус по нескольким моделям
- `/cs:freeze` — блокировка времени восстановления при принятии решения

## Быстрый старт { #quick-start }

```
/cs:onboard                          # populate company context first
/cs:office-hours "should we hire a VP Sales?"
/cs:founder-mode "runway pressure"   # auto-routes to CFO
/cs:boardroom briefs/pricing-v3.md   # full panel
```

## Архитектура { #architecture }

```
User question
   │
   ├─ Single-role? → cs-{role}-advisor agent
   │                     ↓
   │                  /cs:{role}-review command (forcing Qs)
   │                     ↓
   │                  Skill tools + references
   │                     ↓
   │                  Bottom Line + Memo
   │
   └─ Multi-role?  → /cs:boardroom
                        ↓
                     6-phase deliberation (Phase 2 isolation)
                        ↓
                     /cs:decide → decision-logger (two-layer memory)
                        ↓
                     /cs:execute → 90-day plan
```

## Точки интеграции { #integration-points }

- ** Существующие 33 скилла уровня c** — перенесены, не заменены
- **регистратор решений** — каждый `/cs:decide` пишет здесь
- **начальник штаба** — уровень маршрутизации, которым управляет агент
- **заседание правления** — протокол заседания `/cs:boardroom` выполняется команда
- **llm-wiki** — дополнительный мост постоянной памяти (см. [`references/llm-wiki-bridge.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md))
- **руководитель-наставник** — состязательный `/em:*` команды аккуратно складываются сверху

## Принципы проектирования { #design-principles }

1. ** Голос записан, анализ нейтральный.**
2. **Артефакты в чате.** Каждая команда создает артефакт Markdown, который использует следующая команда.
3. **Изоляция фазы 2 в зале заседаний.** Независимое мышление перед перекрестным допросом.
4. ** Постепенная деградация.** `/cs:cross-eval` возвращается только к Клоду.
5. ** Никаких платных зависимостей.** Все инструменты Python доступны только для stdlib.

## Ссылки { #references }

- [persona-voices.md](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/persona-voices.md)
- [llm-wiki-bridge.md](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md)
- [Родительский уровень c CLAUDE.md](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/CLAUDE.md)
- [Существующий брат-руководитель-наставник](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/executive-mentor)

---

**Версия:** 1.0.0
** Последнее обновление:** 2026-05-12
**Статус:** Производство готово
