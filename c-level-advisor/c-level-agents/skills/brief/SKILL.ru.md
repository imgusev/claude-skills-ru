---
name: "brief"
description: "/cs:краткое изложение <тема> — Сгенерируйте одностраничное краткое изложение стратегии на основе учета рабочего времени. Первый шаг в стратегическом пайплайне спринта. Используйте, когда необходимо сформулировать стратегический вопрос перед обсуждением в зале заседаний — например, варианты фиксации, предположения и критерии успеха для изменения цен или решения о выходе на рынок."
---

# /cs:brief — Краткое изложение стратегии на одной странице { #csbrief--one-page-strategy-brief }

**Команда:** `/cs:brief <topic>` или `/cs:brief <office-hours-output>`

Превращает входную информацию (необработанный вопрос или выходные данные за рабочее время) в одностраничное стратегическое резюме, которое может обсудить зал заседаний. Это **Шаг 1** пайплайна стратегического спринта.

## Положение пайплайна { #pipeline-position }

```
/cs:office-hours  →  /cs:brief  →  /cs:boardroom  →  /cs:decide  →  /cs:execute  →  /cs:post-mortem
                       ↑ you are here
```

## Входные данные { #inputs }

- Строка темы, **или**
- Краткое описание рабочего времени (предпочтительно — более строгое)
- `~/.claude/company-context.md` (загружается автоматически)

## Выход { #output }

Один файл Markdown в разделе `~/.claude/briefs/YYYY-MM-DD-<slug>.md` с такой структурой:

```markdown
# Strategy Brief: <topic>
**Date:** YYYY-MM-DD
**Author:** cs-chief-of-staff
**Status:** DRAFT | UNDER REVIEW | APPROVED | RETIRED

## Context
[1-2 paragraphs: where the company sits today on this topic — pulled from company-context.md]

## Question
[The one sentence question the boardroom must answer]

## Options
1. **Option A:** <name> — <one-sentence summary>
2. **Option B:** <name> — <one-sentence summary>
3. **Option C:** <name> — <one-sentence summary>

(Minimum 2 options. "Do nothing" is always an option.)

## Assumptions
- <assumption 1 — explicit>
- <assumption 2>
- <assumption 3>

## Constraints
- Time: <by when must this decide>
- Money: <budget envelope>
- People: <who can / can't be reallocated>
- Reversibility: <one-way door | two-way door>

## Affected Roles
[Which cs-* advisors should weigh in. Used to route to /cs:boardroom panel composition.]

- [ ] cs-ceo-advisor
- [ ] cs-cfo-advisor
- [ ] cs-cto-advisor
- [ ] cs-cmo-advisor
- [ ] cs-cro-advisor
- [ ] cs-cpo-advisor
- [ ] cs-coo-advisor
- [ ] cs-chro-advisor
- [ ] cs-ciso-advisor
- [ ] cs-general-counsel-advisor
- [ ] cs-cdo-advisor
- [ ] cs-caio-advisor
- [ ] cs-cco-advisor
- [ ] cs-vpe-advisor
- [ ] cs-chief-of-staff

## Success Criteria
[Measurable outcomes that define success — set BEFORE the decision]
- <metric 1, threshold, timeframe>
- <metric 2, threshold, timeframe>

## Kill Criteria
[What signal would tell you in 90 days that this was the wrong call]
- <metric, threshold, action if missed>
```

## Воркфлоу { #workflow }

1. Нагрузка company-context.md через контекстный движок
2. Если входными данными являются выходные данные за рабочее время, проанализируйте 6 ответов
3. Если вводные данные - это необработанная тема, промпту основателя о недостающих фрагментах
4. Подготовьте 2-3 варианта (никогда только один — к каждому брифу требуется контрфакт)
5. Сделайте предположения и ограничения явными
6. Определение затронутых ролей → состав панели приводов для `/cs:boardroom`
7. Напишите критерии успеха + уничтожения ПЕРЕД принятием решения (это момент строгости)
8. Сохранить в `~/.claude/briefs/`

## Почему существует этот шаг { #why-this-step-exists }

Самая большая ошибка при принятии решения - это обсуждение реализации, прежде чем прийти к согласию по вопросу. В кратком изложении фиксируются вопрос, варианты и критерии успеха, чтобы зал заседаний мог обсудить их без расширения сферы охвата.

Это также ** хэндофф артефакта** — следующая команда использует этот файл, а не вашу память.

## Маршрутизация { #routing }

- `/cs:boardroom <brief>` — обсуждение с участием многих ролей
- `/cs:cross-eval <brief>` — проверка работоспособности нескольких моделей перед заседанием совета директоров (для игр с высокими ставками)
- `/cs:freeze <brief>` — блокировка перезарядки для необратимых решений

## Связанный { #related }

- Агент: [`cs-chief-of-staff`](../../agents/cs-chief-of-staff.md)
- Скиллы: [`context-engine`](../../../skills/context-engine/SKILL.md), [`board-meeting`](../../../skills/board-meeting/SKILL.md)

---

**Версия:** 1.0.0
