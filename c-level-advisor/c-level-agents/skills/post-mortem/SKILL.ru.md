---
name: "post-mortem"
description: "/cs: посмертное <решение> — честная ретроспектива принятого решения, оцениваемая с учетом первоначальных предположений и несогласия. Завершает стратегический цикл спринта. Используется, когда решение достигает 90-дневного срока ревью или триггера критерия отмены — например, при сопоставлении изменения цен за прошлый квартал с заранее установленными показателями успеха."
---

# /cs:post-mortem — Честная ретроспектива { #cspost-mortem--honest-retrospective }

**Команда:** `/cs:post-mortem <decision-path>`

Завершает стратегический цикл спринта. Оценивает решение по критериям успеха и уничтожения, написанным ** до** принятия решения (не с учетом ретро-изменений), и пересматривает сохраненное несогласие. Это строгость, которая со временем усиливается.

## Положение пайплайна { #pipeline-position }

```
/cs:office-hours  →  /cs:brief  →  /cs:boardroom  →  /cs:decide  →  /cs:execute  →  /cs:post-mortem
                                                                                       ↑ you are here
```

## Когда запускать { #when-to-run }

- На 90-дневном контрольном пункте (автоматически запланированном `/cs:decide`)
- Когда триггер критерия уничтожения срабатывает
- После отмены важного решения
- Ежеквартально по всем решениям за прошедший квартал

## Входные данные { #inputs }

- Запись решения (вывод из `/cs:decide`)
- План выполнения (выходные данные `/cs:execute`)
- Фактические результаты (показатели, события, сигналы клиентов)

## Результат: Посмертная запись { #output-post-mortem-record }

Сохранено в `~/.claude/postmortems/YYYY-MM-DD-<slug>.md`:

```markdown
# Post-Mortem: <decision title>
**Decision date:** YYYY-MM-DD
**Post-mortem date:** YYYY-MM-DD
**Status:** WIN / PARTIAL / LOSS / MIXED

## Outcome Scoring (against pre-committed criteria)

| Success Criterion | Threshold | Actual | Met? |
|---|---|---|---|
| <metric 1> | <threshold> | <actual> | ✅ / ❌ |
| <metric 2> | <threshold> | <actual> | ✅ / ❌ |

| Kill Criterion | Threshold | Actual | Triggered? |
|---|---|---|---|
| <metric> | <threshold> | <actual> | ✅ / ❌ |

**Overall:** WIN / PARTIAL / LOSS / MIXED

## What We Got Right
- <factor 1>
- <factor 2>

## What We Got Wrong
- <factor 1>
- <factor 2>

## Preserved Dissent — Revisited
[Original dissent from the boardroom memo, scored:]

- **<dissenter>:** <original concern>
  - **Did it materialize?** YES / NO / PARTIAL
  - **Cost if YES:** <quantified impact>
  - **Lesson:** <one sentence>

## Assumption Audit
[Original brief's assumptions, scored:]

- **Assumption 1:** <text>
  - **Held?** YES / NO / PARTIAL
  - **Why:** <explanation>

## Process Lessons
- **Phase 2 isolation worked?** YES / NO
- **Devil's advocate concerns played out?** YES / NO / PARTIAL
- **Cadence was right?** YES / TOO LOOSE / TOO TIGHT

## Forward Actions
- [ ] <change to operating system or routing logic>
- [ ] <new decision to make based on this learning>
- [ ] <update company-context.md>

## Status
- WIN → archive, log lesson
- LOSS → schedule follow-up boardroom: `/cs:brief` for the next call
```

## Почему важны заранее установленные критерии { #why-pre-committed-criteria-matter }

Самый большой соблазн при вскрытии - это ретроактивное оправдание: "мы всегда знали X, вот почему мы сделали Y". Заранее установленные критерии, подписанные в `/cs:decide` время, исключи этот ход. Цифры либо совпадали, либо нет.

## Зачем возвращаться к инакомыслию { #why-revisit-dissent }

Колонка "Несогласие" из `/cs:boardroom` это единственная наиболее полезная часть организационной памяти. В большинстве случаев несогласный был прав с точки зрения направления. Повторный просмотр и оценка результатов позволяют проводить калибровку на протяжении многих лет.

## Маршрутизация { #routing }

- `/cs:brief` — если в результате вскрытия будет принято новое решение
- `/cs:freeze` — если вскрытие выявит пробел в процессе, требующий принудительного восстановления
- Обновления для company-context.md через `cs-onboard`

## Связанный { #related }

- Скилл: [`decision-logger`](../../../skills/decision-logger/SKILL.md)
- Агент: [`cs-chief-of-staff`](../../agents/cs-chief-of-staff.md)
- Родной брат: [`/em:postmortem`](../../../executive-mentor/skills/postmortem/SKILL.md) — состязательное вскрытие с единоличным решением

---

**Версия:** 1.0.0
