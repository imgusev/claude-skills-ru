---
title: "/cs:decide — Зарегистрировать решение { #csdecide--log-the-decision } — Агентский скилл для руководителей"
description: "/cs:decide <memo> — Заносит решение в двухуровневую память с помощью регистратора решений. Утвержденная памятка становится долговечной. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:decide — Зарегистрировать решение { #csdecide--log-the-decision }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `decide`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/decide/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:decide <memo-path>`

Регистрирует решение основателя через `decision-logger` скилл. Это тот гейт, где обсуждение во время сессии становится долговременной памятью компании.

## Положение пайплайна { #pipeline-position }

```
/cs:office-hours  →  /cs:brief  →  /cs:boardroom  →  /cs:decide  →  /cs:execute  →  /cs:post-mortem
                                                       ↑ you are here
```

## Двухслойная модель памяти { #two-layer-memory-model }

Тот `decision-logger` скилл состоит из двух слоев:

1. ** Необработанные стенограммы** — каждое заседание совета директоров, позиция каждого консультанта на этапе 2, каждое несогласие. Хранящийся под `~/.claude/decisions/raw/`. Только ссылка, никогда не возвращается автоматически.
2. **Утвержденные решения** — служебные записки, подписанные только учредителем. Хранящийся под `~/.claude/decisions/approved/`. Вкладывается в будущее `/cs:office-hours` и `/cs:founder-mode` звонки.

Это разделение не позволяет системе "запоминать" неразрешенные дебаты, как если бы они были решениями.

## Входной сигнал { #input }

Файл памятки на доске (выходные данные `/cs:boardroom`).

## Воркфлоу { #workflow }

1. Прочитайте путь к памятке
2. Убедитесь, что он одобрен учредителем (статус: ОДОБРЕНО)
3. Извлеките структурированную запись о принятии решения:
   - Название решения
   - Дата определена
   - Выбранный вариант
   - Критерии успеха + уничтожения
   - Несогласие (сохранено)
   - Дата контрольной точки Ревью
4. Добавить к `~/.claude/decisions/approved/<YYYY-MM-DD>-<slug>.md`
5. Обновите указатель необработанной расшифровки
6. Если мост llm-wiki настроен, выполните запись в vault (`~/company-vault/10-decisions/`)
7. Запланируйте автоматический повторный просмотр (90 дней)

## Формат выходной записи { #output-record-format }

```markdown
# Decision: <title>
**Decided:** YYYY-MM-DD
**By:** <founder name>
**Memo:** <link to boardroom memo>
**Brief:** <link to original brief>
**Review checkpoint:** YYYY-MM-DD (90d default)

## Decision
**Chose:** <option>
**Rejected:** <other options + one-line why>

## Success Criteria (binding)
- <metric, threshold, timeframe>

## Kill Criteria (binding)
- <metric, threshold, action>

## Preserved Dissent
- **<dissenter>:** <unresolved concern>
- (preserved verbatim; dissent never erased)

## Next Action
- `/cs:execute` → 90-day plan due <date>

## Status History
- YYYY-MM-DD: APPROVED
```

## Почему сохранилось инакомыслие { #why-preserved-dissent }

Самый большой риск при принятии одобренных решений - это забыть, почему кто-то не согласился. Когда триггер "критерии уничтожения" срабатывает, несогласие часто оказывается правильным. Сохранение этого дословно, а не в кратком изложении, позволяет компании оставаться честной во время вскрытия.

## Маршрутизация { #routing }

- `/cs:execute <decision>` — составьте 90-дневный план
- `/cs:freeze <decision> <days>` — блокировка, если она необратима
- (Автоматическое планирование) `/cs:post-mortem <decision>` — на 90-дневном контрольно-пропускном пункте

## Аудит устаревших решений { #stale-decision-audit }

`cs-chief-of-staff` проводит еженедельный устаревший аудит:
- Решения > 90 дней без повторного рассмотрения → пометить для `/cs:post-mortem`
- Решения с критериями уничтожения триггера → немедленно помечаются
- Решения, чьи company-context.md основа изменена → флаг для повторной проверки

## Связанный { #related }

- Скилл: [`decision-logger`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/decision-logger/SKILL.md)
- Агент: [`cs-chief-of-staff`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/agents/cs-chief-of-staff.md)
- Мост: [[`references/llm-wiki-bridge.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md)](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md)

---

**Версия:** 1.0.0
