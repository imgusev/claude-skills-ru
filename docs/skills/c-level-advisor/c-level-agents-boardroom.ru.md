---
title: "/cs:зал заседаний — Многоцелевое обсуждение в зале заседаний { #csboardroom--multi-role-boardroom-deliberation } — Агентский скилл для руководителей"
description: "/cs: зал заседаний <краткое описание> — 6-фазное многоцелевое обсуждение в C-suite с выделением фазы 2, предварительным просмотром критики и. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:зал заседаний — Многоцелевое обсуждение в зале заседаний { #csboardroom--multi-role-boardroom-deliberation }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `boardroom`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/boardroom/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:boardroom <brief-path>`

Запускает `board-meeting` протокол скилл для всего C-suite для получения единой стратегической информации. Это **сердце плагина** — многоцелевое обсуждение, к которому цепочка ревью gstack только приближается.

## Положение пайплайна { #pipeline-position }

```
/cs:office-hours  →  /cs:brief  →  /cs:boardroom  →  /cs:decide  →  /cs:execute  →  /cs:post-mortem
                                     ↑ you are here
```

## 6 этапов (начиная с скилла на заседании правления) { #the-6-phases-from-board-meeting-skill }

### Этап 1 — Брифинг { #phase-1--briefing }
- Руководитель аппарата рассылает краткое описание всем консультантам, отмеченным в **Соответствующих ролях**.
- Каждый советник читает company-context.md + краткое изложение.
- Пока никакого обсуждения.

### Фаза 2 — Независимое мышление (ИЗОЛЯЦИЯ) { #phase-2--independent-thinking-isolation }
- **Важно:** каждый советник формирует свою позицию ** независимо**, не видя позиций других.
- Это предотвращает групповое мышление и выявляет инакомыслие.
- Каждый пишет: вступительное слово своего голоса, рекомендацию, топ-3 проблем, топ-3 поддержки.

### Этап 3 — Перекрестный допрос { #phase-3--cross-examination }
- Позиции раскрываются одновременно.
- Каждый консультант критикует позиции других по тем измерениям, которыми они владеют:
  - финансовый директор-консультант критикует математику
  - cs-ciso-советник критикует риск
  - cs-cpo-advisor критикует JTBD
  - cs-cmo-советник критикует позиционирование
  - cs-cro-advisor критикует математику доходов
  - и так далее.

### Фаза 4 — Прохождение Адвоката дьявола { #phase-4--devils-advocate-pass }
- `executive-mentor/devils-advocate` агент запускает `/em:challenge` по ведущему варианту.
- Выявляет три проблемы с оценками серьезности.

### Фаза 5 — Синтез { #phase-5--synthesis }
- Глава администрации обобщает: какой вариант пользуется большинством в команде, какие разногласия остаются нерешенными.
- Подготавливает ** памятку правления** с рекомендацией + несогласием.

### Этап 6 — Передача решения { #phase-6--decision-hand-off }
- Памятка вручается учредителю.
- Основатель принимает, изменяет или отклоняет.
- Утвержденные памятные маршруты к `/cs:decide` для ведения журнала.

## Результат: Памятка на доске { #output-board-memo }

Сохранено в `~/.claude/boardroom/YYYY-MM-DD-<slug>.md`:

```markdown
# Board Memo: <topic>
**Date:** YYYY-MM-DD
**Brief:** <link to /cs:brief file>
**Status:** AWAITING FOUNDER DECISION | APPROVED | REJECTED

## Question
[One sentence from the brief]

## Recommended Option
**<Option name>** — chosen because <synthesis reasoning>

## Vote Tally
| Advisor | Vote | One-Sentence Reason |
|---|---|---|
| cs-ceo-advisor | A | <reason> |
| cs-cfo-advisor | A | <reason> |
| cs-cto-advisor | B | <reason> |
| ... | | |

## Dissent
- **<dissenter>:** <unresolved concern>

## Devil's Advocate Concerns
1. **CRITICAL** — <concern> — Mitigation: <plan>
2. **HIGH** — <concern> — Mitigation: <plan>
3. **MEDIUM** — <concern> — Mitigation: <plan>

## Success & Kill Criteria
[Copied from brief, refined by the panel]

## Recommended Decision Path
- `/cs:decide` → log the decision
- `/cs:execute` → 90-day plan
- `/cs:cross-eval` → multi-model sanity check (optional, high-stakes)
- `/cs:freeze N` → cooldown lock (optional, irreversible)
```

## Почему важна изоляция фазы 2 { #why-phase-2-isolation-matters }

Если советники видят позиции друг друга, прежде чем сформировать свою собственную, они закрепляются. Изоляция на этапе 2 является единственной наиболее эффективной практикой в протоколе заседаний правления - она выявляет несогласие, которое было бы подавлено подхалимажем.

## Почему это превосходит цепочку ревью gstack { #why-this-beats-gstacks-review-chain }

| | gstack - пакет `/autoplan` | `/cs:boardroom` |
|---|---|---|
| Роли | Генеральный директор → дизайн → английский (3) | До 10 C-ролей |
| Порядок | Последовательный | Изоляция фазы 2, затем одновременное |
| Захват инакомыслящих | Неявный | Колонка с явным несогласием |
| Состязательный проход | Нет | Фаза 4 адвокат дьявола |
| Выход | План ревью | Проголосовавшая записка с критериями несогласия + уничтожения |

## Воркфлоу { #workflow }

1. Прочитайте краткое изложение из `~/.claude/briefs/<file>`
2. Определите затронутые роли
3. Вызывайте каждый советник cs-* независимо (фаза 2)
4. Собирайте позиции
5. Провести раунд перекрестного допроса (фаза 3)
6. Бежать `/em:challenge` по ведущему варианту (фаза 4)
7. Синтез памятки (фаза 5)
8. Передача основателю (фаза 6)

## Маршрутизация { #routing }

- `/cs:decide` — запись утвержденной памятки в журнал
- `/cs:cross-eval` — второе мнение с высокими ставками
- `/cs:freeze` — блокировка перезарядки

## Связанный { #related }

- Агент: [`cs-chief-of-staff`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/agents/cs-chief-of-staff.md)
- Скиллы: [`board-meeting`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/board-meeting/SKILL.md), [`executive-mentor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/executive-mentor)

---

**Версия:** 1.0.0
