---
name: "decision-logger"
description: "Двухуровневая архитектура памяти для принятия решений на заседаниях правления. Управляет исходными расшифровками (уровень 1) и утвержденными решениями (уровень 2). Используйте при регистрации решений после заседания правления, ревью прошлых решений с помощью /cs:decisions или проверке просроченных действий с помощью /cs:ревью. Вызывается автоматически скилл-менеджментом на заседании правления после утверждения учредителем этапа 5."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: decision-memory
  updated: 2026-03-05
  python-tools: scripts/decision_tracker.py
---

# Регистратор решений { #decision-logger }

Двухуровневая система памяти. На уровне 1 хранится все. На уровне 2 хранится только то, что одобрил основатель. Будущие встречи читаются только на уровне 2 — это предотвращает появление галлюцинаторного консенсуса в прошлых дебатах, перетекающего в новые обсуждения.

## Ключевые слова { #keywords }
журнал решений, память, утвержденные решения, пункты действий, протоколы правления, /cs:решения, /cs:ревью, обнаружение конфликтов, DO_NOT_RESURFACE

## Быстрый старт { #quick-start }

```bash
python scripts/decision_tracker.py --demo             # See sample output
python scripts/decision_tracker.py --summary          # Overview + overdue
python scripts/decision_tracker.py --overdue          # Past-deadline actions
python scripts/decision_tracker.py --conflicts        # Contradiction detection
python scripts/decision_tracker.py --owner "CTO"      # Filter by owner
python scripts/decision_tracker.py --search "pricing" # Search decisions
```

---

## Команды { #commands }

| Команда | Эффект |
|---------|--------|
| `/cs:decisions` | Последние 10 утвержденных решений |
| `/cs:decisions --all` | Полная история |
| `/cs:decisions --owner CMO` | Фильтровать по владельцу |
| `/cs:decisions --topic pricing` | Поиск по ключевому слову |
| `/cs:review` | Товары по акции должны быть отправлены в течение 7 дней |
| `/cs:review --overdue` | Товары, срок доставки которых истек |

---

## Двухуровневая архитектура { #two-layer-architecture }

Хранилище соответствует канонической двухуровневой памяти принятия решений (см. `../agent-protocol/SKILL.md` → "Память принятия решений (каноническая компоновка)") — та же компоновка `/cs:decide` пишет.

### Уровень 1 — Необработанные транскрипты { #layer-1--raw-transcripts }
**Местоположение:** `~/.claude/decisions/raw/YYYY-MM-DD-<slug>.md`
- Полный вклад агентов фазы 2, критика фазы 3, обобщение фазы 4
- Все дебаты, включая отклоненные аргументы
- ** НИКОГДА не загружается автоматически.** Только по прямому запросу учредителя.
- Архив через 90 дней → `~/.claude/decisions/raw/archive/YYYY/`

### Уровень 2 — Утвержденные решения { #layer-2--approved-decisions }
**Местоположение:** `~/.claude/decisions/approved/` — одна запись за каждое решение (`YYYY-MM-DD-<slug>.md`) плюс индекс только для добавления `decisions.md`
- ТОЛЬКО одобренные учредителем решения, пункты действий, исправления пользователей
- **Загружается автоматически на этапе 1 каждого заседания правления**
- Только для добавления. Решения никогда не удаляются — только заменяются.
- Управляется начальником штаба после этапа 5. Никогда не пишется непосредственно агентами.

Миграция: наследие `memory/board-meetings/` папка может существовать в более ранних версиях; прочитайте ее для истории, но записывайте все новые записи в `~/.claude/decisions/`.

---

## Формат ввода решения { #decision-entry-format }

```markdown
## [YYYY-MM-DD] — [AGENDA ITEM TITLE]

**Decision:** [One clear statement of what was decided.]
**Owner:** [One person or role — accountable for execution.]
**Deadline:** [YYYY-MM-DD]
**Review:** [YYYY-MM-DD]
**Rationale:** [Why this over alternatives. 1-2 sentences.]

**User Override:** [If founder changed agent recommendation — what and why. Blank if not applicable.]

**Rejected:**
- [Proposal] — [reason] [DO_NOT_RESURFACE]

**Action Items:**
- [ ] [Action] — Owner: [name] — Due: [YYYY-MM-DD] — Review: [YYYY-MM-DD]

**Supersedes:** [DATE of previous decision on same topic, if any]
**Superseded by:** [Filled in retroactively if overridden later]
**Raw transcript:** ~/.claude/decisions/raw/[DATE]-<slug>.md
```

---

## Обнаружение конфликтов { #conflict-detection }

Перед регистрацией начальник штаба проверяет наличие:
1. **НЕ допускать нарушений на ПОВЕРХНОСТИ** — новое решение соответствует отклоненному предложению
2. **Противоречия по теме** — два активных решения по одной и той же теме с разными выводами
3. **Конфликты владельцев** — одно и то же действие назначается разным людям в разных решениях

При обнаружении конфликта:
```
⚠️ DECISION CONFLICT
New: [text]
Conflicts with: [DATE] — [existing text]

Options: (1) Supersede old  (2) Merge  (3) Defer to founder
```

**Принудительное выполнение действий на ПОВЕРХНОСТИ DO_NOT_RESURFACE:**
```
🚫 BLOCKED: "[Proposal]" was rejected on [DATE]. Reason: [reason].
To reopen: founder must explicitly say "reopen [topic] from [DATE]".
```

---

## Ведение журнала воркфлоу (после этапа 5) { #logging-workflow-post-phase-5 }

1. Основатель одобряет синтез
2. Запишите необработанную расшифровку уровня 1 → `~/.claude/decisions/raw/YYYY-MM-DD-<slug>.md`
3. Проверять конфликты на соответствие `~/.claude/decisions/approved/decisions.md`
4. Поверхностные конфликты → ожидание разрешения основателем
5. Запишите утвержденную запись в `~/.claude/decisions/approved/YYYY-MM-DD-<slug>.md` и добавить к индексу `decisions.md`
6. Подтверждаю: решения регистрируются, действия отслеживаются, добавлены флаги DO_NOT_RESURFACE

---

## Действия по маркировке завершены { #marking-actions-complete }

```markdown
- [x] [Action] — Owner: [name] — Completed: [DATE] — Result: [one sentence]
```

Никогда не удаляйте завершенные элементы. История - это запись.

---

## Файловая структура { #file-structure }

```
~/.claude/decisions/
├── raw/YYYY-MM-DD-<slug>.md        # Layer 1: full transcript per meeting
├── raw/archive/YYYY/               # Raw files after 90 days
├── approved/YYYY-MM-DD-<slug>.md   # Layer 2: one record per approved decision
└── approved/decisions.md           # Layer 2 index: append-only, founder-approved
```

---

## Ссылки { #references }
- `templates/decision-entry.md` — шаблон единой записи с правилами заполнения
- `scripts/decision_tracker.py` — Синтаксический анализатор CLI, отслеживание просроченных платежей, детектор конфликтов
