---
name: "execute"
description: "/cs:выполнить <решение> — Сгенерировать 90-дневный план выполнения с еженедельными контрольными точками, DRY и частотой регистрации на основе утвержденного решения. Используйте, когда зарегистрированное решение должно стать операционным планом — например, превращение одобренного запроса о выходе на рынок в еженедельные контрольные точки с помощью DRIs."
---

# /cs:execute — 90-дневный план выполнения { #csexecute--90-day-execution-plan }

**Команда:** `/cs:execute <decision-path>`

Превращает утвержденное решение в 90-дневный план с еженедельными контрольными точками, называемыми DRIs, и периодичностью регистрации. Где большинство решений умирают: между "мы решили" и "что будет в следующий понедельник?"

## Положение пайплайна { #pipeline-position }

```
/cs:office-hours  →  /cs:brief  →  /cs:boardroom  →  /cs:decide  →  /cs:execute  →  /cs:post-mortem
                                                                       ↑ you are here
```

## Входной сигнал { #input }

Запись об утвержденном решении (выходные данные `/cs:decide`).

## Формат плана вывода { #output-plan-format }

Сохранено в `~/.claude/execution/YYYY-MM-DD-<slug>.md`:

```markdown
# Execution Plan: <decision title>
**Decision:** <link to /cs:decide record>
**Owner (Sponsor):** <founder or exec>
**Start:** YYYY-MM-DD
**Checkpoint:** YYYY-MM-DD (90d)

## Outcome (binding)
[Copied from decision: success + kill criteria]

## Workstreams
| Workstream | DRI | Success Metric | Status |
|---|---|---|---|
| <e.g., Pricing rollout> | <name> | <metric, threshold> | Not started |
| <e.g., Comms> | <name> | <metric> | Not started |
| <e.g., Eng changes> | <name> | <metric> | Not started |

## Weekly Milestones
| Week | Milestone | DRI | Definition of Done |
|---|---|---|---|
| 1 | <e.g., positioning locked> | <name> | <observable outcome> |
| 2 | <e.g., draft launched> | <name> | <observable> |
| 3 | ... | | |
| 12 | <e.g., checkpoint review> | <name> | <observable> |

## Cadence
- **Weekly:** Owner reviews status (15 min)
- **Bi-weekly:** Cross-functional sync (30 min)
- **Day 30 / 60 / 90:** Checkpoint with cs-chief-of-staff

## Dependencies
- Internal: <list>
- External: <vendors, regulators, customers>

## Risk Register
| Risk | Likelihood | Impact | Owner | Mitigation |
|---|---|---|---|---|
| <e.g., delayed legal review> | M | H | <name> | <plan> |

## Kill Criteria Watch
[Copied from decision; reviewed at every checkpoint]
- <metric, threshold, action>
```

## Воркфлоу { #workflow }

1. Ознакомьтесь с протоколом принятия решения
2. Разложите выбранный вариант на 3-6 рабочих потоков
3. Назовите DRI для каждого рабочего потока
4. Перепроектируйте 12 еженедельных этапов, начиная с даты контрольной точки
5. Установите частоту (еженедельно + раз в две недели + 30/60/90 контрольных точек)
6. Создание реестра рисков (перекрестная ссылка на первоначальную фазу 4 "Проблемы адвоката дьявола")
7. Сохранить и уведомить DRIs

## Почему именно 90 дней { #why-90-days }

- Достаточно долго, чтобы показать реальный сигнал (а не просто активность)
- Достаточно короткий, чтобы скорректировать курс до повреждения соединений
- Соответствует квартальному циклу OKR, спринтам по сбору средств и большинству каденций правления

## Маршрутизация { #routing }

- `/cs:post-mortem <decision>` — на 90-й день (или раньше, если триггер критерия уничтожения сработает)
- `/cs:boardroom` — если контрольно-пропускной пункт выявляет необходимость принятия повторного решения

## Связанный { #related }

- Скиллы: [`coo-advisor`](../../../skills/coo-advisor/SKILL.md), [`strategic-alignment`](../../../skills/strategic-alignment/SKILL.md), [`change-management`](../../../skills/change-management/SKILL.md)
- Агент: [`cs-coo-advisor`](../../agents/cs-coo-advisor.md)

---

**Версия:** 1.0.0
