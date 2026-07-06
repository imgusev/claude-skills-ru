---
name: "agent-protocol"
description: "Протокол межагентной связи для команд агентов C-suite. Протокол межагентной связи для команд агентов C-suite. Определяет синтаксис вызова, предотвращение цикла, правила изоляции и форматы ответов. Используйте, когда агентам C-suite необходимо запрашивать друг у друга, координировать межфункциональный анализ или проводить заседания правления с несколькими ролями агентов."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: agent-orchestration
  updated: 2026-03-05
  frameworks: invocation-patterns
---

# Протокол взаимодействия между агентами { #inter-agent-protocol }

Как агенты C-suite общаются друг с другом. Правила, которые предотвращают хаос, циклы и круговые рассуждения.

## Ключевые слова { #keywords }
протокол агента, межагентская связь, вызов агента, оркестрация агента, мультиагентный агент, координация c-suite, цепочка агентов, предотвращение цикла, изоляция агента, протокол заседания совета директоров., изоляция между агентами., изоляция между агентами.

## Синтаксис вызова { #invocation-syntax }

Любой агент может запросить другого, используя:

```
[INVOKE:role|question]
```

**Примеры:**
```
[INVOKE:cfo|What's the burn rate impact of hiring 5 engineers in Q3?]
[INVOKE:cto|Can we realistically ship this feature by end of quarter?]
[INVOKE:chro|What's our typical time-to-hire for senior engineers?]
[INVOKE:cro|What does our pipeline look like for the next 90 days?]
```

**Допустимые роли:** `ceo`, `cfo`, `cro`, `cmo`, `cpo`, `cto`, `chro`, `coo`, `ciso`, `gc`, `cdo`, `caio`, `cco`, `vpe`

| Ролевой токен | Скилл советника |
|---|---|
| `gc` | генеральный юрисконсульт-консультант (юридические вопросы, контракты, временные рамки) |
| `cdo` | руководитель-специалист по обработке данных-консультант (стратегия обработки данных, обучение - права на данные) |
| `caio` | руководитель-специалист по ИИ-советник (стратегия ИИ, оценки, риски ИИ) |
| `cco` | руководитель-сотрудник по работе с клиентами-консультант (удержание, успех клиентов) |
| `vpe` | vpe-консультант (инженерное обеспечение, DORA, подбор персонала) |

## Формат ответа { #response-format }

Вызванные агенты отвечают, используя эту структуру:

```
[RESPONSE:role]
Key finding: [one line — the actual answer]
Supporting data:
  - [data point 1]
  - [data point 2]
  - [data point 3 — optional]
Confidence: [high | medium | low]
Caveat: [one line — what could make this wrong]
[/RESPONSE]
```

**Пример:**
```
[RESPONSE:cfo]
Key finding: Hiring 5 engineers in Q3 extends runway from 14 to 9 months at current burn.
Supporting data:
  - Current monthly burn: $280K → increases to ~$380K (+$100K fully loaded)
  - ARR needed to offset: ~$1.2M additional within 12 months
  - Current pipeline covers 60% of that target
Confidence: medium
Caveat: Assumes 3-month ramp and no change in revenue trajectory.
[/RESPONSE]
```

## Предотвращение цикла (Жесткие правила) { #loop-prevention-hard-rules }

Эти правила соблюдаются безоговорочно. Никаких исключений.

### Правило 1: Никакого самозванства { #rule-1-no-self-invocation }
Агент не может вызвать сам себя.
```
❌ CFO → [INVOKE:cfo|...] — BLOCKED
```

### Правило 2: Максимальная глубина = 2 { #rule-2-maximum-depth--2 }
Цепочки могут идти A→B→C. Третий переход заблокирован.
```
✅ CRO → CFO → COO (depth 2)
❌ CRO → CFO → COO → CHRO (depth 3 — BLOCKED)
```

### Правило 3: Никаких циклических вызовов { #rule-3-no-circular-calls }
Если агент A вызвал агента B, агент B не может вызвать агента A в той же цепочке.
```
✅ CRO → CFO → CMO
❌ CRO → CFO → CRO (circular — BLOCKED)
```

### Правило 4: Отслеживание цепочки { #rule-4-chain-tracking }
Каждый вызов содержит свою цепочку вызовов. Формат:
```
[CHAIN: cro → cfo → coo]
```
Агенты проверяют эту цепочку, прежде чем ответить другим вызовом.

**При блокировке:** Верните это вместо вызова:
```
[BLOCKED: cannot invoke cfo — circular call detected in chain cro→cfo]
State assumption used instead: [explicit assumption the agent is making]
```

## Правила изоляции { #isolation-rules }

### Этап 2 заседания правления (независимый анализ) { #board-meeting-phase-2-independent-analysis }
** Вызовы запрещены.** Каждая роль формирует независимые представления перед перекрестным опылением.
- Причина: предотвращение закрепления и группового мышления
- Продолжительность: весь период анализа фазы 2
- Если агенту нужны данные из другой роли: укажите явное предположение, отметьте его с помощью `[ASSUMPTION: ...]`

### Этап 3 заседания правления (роль критика) { #board-meeting-phase-3-critic-role }
Исполнительный наставник может ** ссылаться** на результаты других ролей, но **не может вызывать** их.
- Причина: критика должна быть независимой от запросов новых данных
- Разрешено: "Прогноз финансового директора предполагает X, что противоречит данным пайплайна CRO"
- Не допускается: `[INVOKE:cfo|...]` на этапе критики

### Внеочередные заседания Правления { #outside-board-meetings }
Вызовы разрешены свободно, при условии соблюдения приведенных выше правил предотвращения циклов.

## Когда вызывать, а когда предполагать { #when-to-invoke-vs-when-to-assume }

**Вызывать, когда:**
- Для ответа на этот вопрос требуются данные, относящиеся к конкретному домену, которых у вас нет
- Ошибка здесь существенно изменила бы рекомендацию
- Вопрос является межфункциональным по своей природе (например, влияние найма как на бюджет, так и на возможности).

**Предполагать, когда:**
- Данные четко ориентированы, и точность не имеет решающего значения
- Вы находитесь в изоляции фазы 2 (всегда предполагайте, никогда не вызывайте)
- Цепочка уже находится на глубине 2
- Этот вопрос незначителен по сравнению с вашим основным анализом

**Предполагая, всегда указывайте это:**
```
[ASSUMPTION: runway ~12 months based on typical Series A burn profile — not verified with CFO]
```

## Разрешение конфликтов { #conflict-resolution }

Когда два вызванных агента дают противоречивые ответы:

1. **Явно отметьте конфликт:**
   ```
   [CONFLICT: CFO projects 14-month runway; CRO expects pipeline to close 80% → implies 18+ months]
   ```
2. **Изложите подход к разрешению:**
   - Консервативный: используйте худший вариант
   - Вероятностный: вес по доверительным показателям
   - Эскалация: флаг для принятия решения человеком
3. **Никогда не выбирайте что—то одно молча ** - выставляйте конфликт на всеобщее обозрение пользователя.

## Схема вещания (кризис / генеральный директор) { #broadcast-pattern-crisis--ceo }

Генеральный директор может осуществлять трансляцию для всех ролей одновременно:
```
[BROADCAST:all|What's the impact if we miss the fundraise?]
```

Ответы возвращаются независимо (ни один агент не видит ответ другого, прежде чем сформировать свой собственный). Агрегат все-таки ответит.

## Память принятия решений (каноническая компоновка) { #decision-memory-canonical-layout }

Все скиллы класса C-suite и `/cs:*` команды считывают и записывают решения в **одном** месте — двухуровневая модель, принадлежащая `/cs:decide` и скилл регистратора решений:

```
~/.claude/decisions/
├── raw/YYYY-MM-DD-<slug>.md        # Layer 1 — full transcripts/deliberations (never auto-loaded)
├── raw/archive/YYYY/               # Raw files after 90 days
├── approved/YYYY-MM-DD-<slug>.md   # Layer 2 — one founder-approved decision record per file
└── approved/decisions.md           # Layer 2 index — append-only log of approved decisions
```

**Правила:**
- **Уровень 1 (необработанный)** хранит все, включая отклоненные аргументы. Только для справки — никогда не загружает будущие сеансы автоматически.
- **Уровень 2 (одобренный)** хранит только решения, одобренные основателем. Вот что такое заседания правления, `/cs:office-hours`, и `/cs:founder-mode` нагрузка. Предотвращает галлюцинируемый консенсус.
- Писатели: `/cs:decide` и начальник штаба (этап 5 после заседания правления). Отдельные ролевые агенты никогда не пишут решения напрямую.
- регистратор решений, руководитель аппарата и заседание правления - все они используют этот макет. Их SKILL.md файлы ссылаются здесь, а не определяют свои собственные пути.

**Миграция:** использовались более ранние версии `memory/board-meetings/` (регистратор решений, заседание правления) и `~/.claude/decision-log.md` (начальник штаба); прочитайте их для истории, если они есть, но записывайте все новые записи в `~/.claude/decisions/`.

## Краткий справочник { #quick-reference }

| Правило | Поведение |
|------|----------|
| Самозваный вызов | ❌ Всегда заблокирован |
| Глубина > 2 | ❌ Заблокировано, предположение о состоянии |
| Круговой | ❌ Заблокировано, предположение о состоянии |
| Изоляция фазы 2 | ❌ Никаких вызовов |
| Фаза 3 критика | ❌ Только ссылка, никакого вызова |
| Конфликт | ✅ Проявляйте это, не прячьте |
| Предположение | ✅ Всегда явно с `[ASSUMPTION: ...]` |

## Внутренний цикл контроля качества (до того, как что-либо дойдет до основателя) { #internal-quality-loop-before-anything-reaches-the-founder }

Ни одна роль не предоставляется основателю без прохождения этого цикла проверки. Основатель видит отшлифованный, выверенный результат, а не первые наброски.

### Шаг 1: Самопроверка (каждая роль, каждый раз) { #step-1-self-verification-every-role-every-time }

Перед представлением каждая роль выполняет этот внутренний чек-лист:

```
SELF-VERIFY CHECKLIST:
□ Source Attribution — Where did each data point come from?
  ✅ "ARR is $2.1M (from CRO pipeline report, Q4 actuals)"
  ❌ "ARR is around $2M" (no source, vague)

□ Assumption Audit — What am I assuming vs what I verified?
  Tag every assumption: [VERIFIED: checked against data] or [ASSUMED: not verified]
  If >50% of findings are ASSUMED → flag low confidence

□ Confidence Score — How sure am I on each finding?
  🟢 High: verified data, established pattern, multiple sources
  🟡 Medium: single source, reasonable inference, some uncertainty
  🔴 Low: assumption-based, limited data, first-time analysis

□ Contradiction Check — Does this conflict with known context?
  Check against company-context.md and recent decisions in decision-log
  If it contradicts a past decision → flag explicitly

□ "So What?" Test — Does every finding have a business consequence?
  If you can't answer "so what?" in one sentence → cut it
```

### Шаг 2: Одноранговая проверка (кросс-функциональная валидация) { #step-2-peer-verification-cross-functional-validation }

Когда рекомендация затрагивает домен другой роли, эта роль проходит проверку ПЕРЕД представлением.

| Если ваша рекомендация включает в себя... | Подтвердите с помощью... | Они проверяют... |
|-------------------------------------|-------------------|---------------|
| Финансовые показатели или бюджет | Финансовый директор | Математика, воздействие на взлетно-посадочную полосу, бюджетная реальность |
| Прогнозы доходов | КРО | Основа для пайплайна, историческая точность |
| Численность персонала или прием на работу | ХРО | Рыночная реальность, осуществимость проекта, временные рамки |
| Техническая осуществимость или сроки | Технический директор | Инженерный потенциал, техническая долговая нагрузка |
| Изменения в операционном процессе | ВОРКУЮЩИЙ | Емкость, зависимости, влияние на масштабирование |
| Изменения, ориентированные на клиента | CRO + CPO | Риск оттока, конфликт дорожной карты продукта |
| Требования безопасности или соответствия требованиям | CISO | Фактическая поза, нормативные требования |
| Требования к рынку или позиционированию | Исполнительный директор | Поддержка данных, конкурентная реальность |
| Юридическое сопровождение, контракты, временные рамки | GC | Риск оговорки, владение интеллектуальной собственностью, нормативные триггеры |
| Права на данные, обучение - источник данных | CDO | Основание для согласия, статья 6 GDPR, влияние данных на активы |
| Требования к модели ИИ, результаты оценки, риск ИИ | КАЙО | Покрытие Eval, SLO по галлюцинациям, уровень EU AI Act |
| Удержание, отток, претензии клиентов к здоровью | Технический директор | Разложение GRR/NRR, первопричина оттока |
| Сроки доставки, пропускная способность | ВПЕ | Показатели DORA, реальность во времени цикла, потенциал команды |

**Формат одноранговой проверки:**
```
[PEER-VERIFY:cfo]
Validated: ✅ Burn rate calculation correct
Adjusted: ⚠️ Hiring timeline should be Q3 not Q2 (budget constraint)
Flagged: 🔴 Missing equity cost in total comp projection
[/PEER-VERIFY]
```

**Пропускать одноранговую проверку, когда:**
- Вопрос из одной области без межфункционального влияния
- Проактивное оповещение, зависящее от времени (отправить оповещение, проверить после)
- Основатель недвусмысленно попросил сделать быстрый снимок

### Шаг 3: Предварительный отбор критиков (только для решений с высокими ставками) { #step-3-critic-pre-screen-high-stakes-decisions-only }

Для решений, которые являются ** необратимыми, дорогостоящими или выгодными для компании**, исполнительный наставник проводит предварительную проверку до того, как основатель увидит их.

**Триггеры для предварительного просмотра:**
- Предполагает расходование > 20% оставшейся взлетно-посадочной полосы
- Затрагивает >30% команды (увольнения, реорганизация)
- Меняет стратегию или направление деятельности компании
- Предполагает внешние обязательства (условия привлечения средств, партнерства, слияния и поглощения).
- Любая рекомендация, в которой все роли согласны (подозрительный консенсус)

**Предварительный вывод на экран:**
```
[CRITIC-SCREEN]
Weakest point: [The single biggest vulnerability in this recommendation]
Missing perspective: [What nobody considered]
If wrong, the cost is: [Quantified downside]
Proceed: ✅ With noted risks | ⚠️ After addressing [specific gap] | 🔴 Rethink
[/CRITIC-SCREEN]
```

### Шаг 4: Коррекция курса (после обратной связи с основателем) { #step-4-course-correction-after-founder-feedback }

Цикл не заканчивается при доставке. После ответа основателя:

```
FOUNDER FEEDBACK LOOP:
1. Founder approves → log decision (Layer 2), assign actions
2. Founder modifies → update analysis with corrections, re-verify changed parts
3. Founder rejects → log rejection with DO_NOT_RESURFACE, understand WHY
4. Founder asks follow-up → deepen analysis on specific point, re-verify

POST-DECISION REVIEW (30/60/90 days):
- Was the recommendation correct?
- What did we miss?
- Update company-context.md with what we learned
- If wrong → document the lesson, adjust future analysis
```

### Уровень верификации по ставкам { #verification-level-by-stakes }

| Ставки | Самопроверка | Одноранговая проверка | Предварительный просмотр критиком |
|--------|-------------|-------------|-------------------|
| Низкий (информационный) | ✅ Требуется | ❌ Пропустить | ❌ Пропустить |
| Средний (операционный) | ✅ Требуется | ✅ Требуется | ❌ Пропустить |
| Высокий (стратегический) | ✅ Требуется | ✅ Требуется | ✅ Требуется |
| Критический (необратимый) | ✅ Требуется | ✅ Требуется | ✅ Требуется + заседание правления |

### Какие изменения произошли в формате вывода { #what-changes-in-the-output-format }

Проверенный результат добавляет уверенности и исходной информации:

```
BOTTOM LINE
[Answer] — Confidence: 🟢 High

WHAT
• [Finding 1] [VERIFIED: Q4 actuals] 🟢
• [Finding 2] [VERIFIED: CRO pipeline data] 🟢  
• [Finding 3] [ASSUMED: based on industry benchmarks] 🟡

PEER-VERIFIED BY: CFO (math ✅), CTO (timeline ⚠️ adjusted to Q3)
```

---

## Стандарт общения с пользователем { #user-communication-standard }

Все выходные данные C-suite для founder представлены в одном формате. Никаких исключений. Основатель - это лицо, принимающее решения, — давайте ему результаты, а не процесс.

### Стандартный вывод (ответ для одной роли) { #standard-output-single-role-response }

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 [ROLE] — [Topic]

BOTTOM LINE
[One sentence. The answer. No preamble.]

WHAT
• [Finding 1 — most critical]
• [Finding 2]
• [Finding 3]
(Max 5 bullets. If more needed → reference doc.)

WHY THIS MATTERS
[1-2 sentences. Business impact. Not theory — consequence.]

HOW TO ACT
1. [Action] → [Owner] → [Deadline]
2. [Action] → [Owner] → [Deadline]
3. [Action] → [Owner] → [Deadline]

⚠️ RISKS (if any)
• [Risk + what triggers it]

🔑 YOUR DECISION (if needed)
Option A: [Description] — [Trade-off]
Option B: [Description] — [Trade-off]
Recommendation: [Which and why, in one line]

📎 DETAIL: [reference doc or script output for deep-dive]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Проактивное оповещение (незапрашиваемое — триггер, зависящий от контекста) { #proactive-alert-unsolicited--triggered-by-context }

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚩 [ROLE] — Proactive Alert

WHAT I NOTICED
[What triggered this — specific, not vague]

WHY IT MATTERS
[Business consequence if ignored — in dollars, time, or risk]

RECOMMENDED ACTION
[Exactly what to do, who does it, by when]

URGENCY: 🔴 Act today | 🟡 This week | ⚪ Next review

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Итоги заседания Правления (обобщение информации о нескольких ролях) { #board-meeting-output-multi-role-synthesis }

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 BOARD MEETING — [Date] — [Agenda Topic]

DECISION REQUIRED
[Frame the decision in one sentence]

PERSPECTIVES
  CEO: [one-line position]
  CFO: [one-line position]
  CRO: [one-line position]
  [... only roles that contributed]

WHERE THEY AGREE
• [Consensus point 1]
• [Consensus point 2]

WHERE THEY DISAGREE
• [Conflict] — CEO says X, CFO says Y
• [Conflict] — CRO says X, CPO says Y

CRITIC'S VIEW (Executive Mentor)
[The uncomfortable truth nobody else said]

RECOMMENDED DECISION
[Clear recommendation with rationale]

ACTION ITEMS
1. [Action] → [Owner] → [Deadline]
2. [Action] → [Owner] → [Deadline]
3. [Action] → [Owner] → [Deadline]

🔑 YOUR CALL
[Options if you disagree with the recommendation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Правила общения (не подлежат обсуждению) { #communication-rules-non-negotiable }

1. **Сначала суть.** Всегда. Время основателя - самый дефицитный ресурс.
2. ** Только результаты и решения.** Никакого описания процесса ("Сначала я проанализировал..."). Никаких мыслей вслух.
3. ** Что + Почему + Как.** Каждое открытие объясняет, ЧТО это такое, ПОЧЕМУ это важно (влияние на бизнес) и КАК действовать в соответствии с этим.
4. ** Максимум 5 пуль на секцию.** Длиннее = справочный материал.
5. ** У действий есть владельцы и крайние сроки.** "Мы должны рассмотреть" запрещено. Кто что делает и когда.
6. **Решения, оформленные в виде вариантов.** Не "что вы думаете?" — "Вариант А или Б, вот компромисс, вот моя рекомендация".
7. ** Основатель принимает решение.** Роли рекомендуются. Основатель утверждает, изменяет или отклоняет. Каждый вывод соответствует этой иерархии.
8. ** Риски конкретны.** Не "могут быть риски" — "если произойдет X, Y сломается, стоимость $Z."
9. ** Никакого жаргона без объяснения причин.** Если вы используете какой-либо термин, объясните его при первом употреблении.
10. ** Молчание - это вариант.** Если сообщать не о чем, не создавайте обновления.

## Ссылка { #reference }
- `references/invocation-patterns.md` — общие кросс-функциональные шаблоны с примерами
