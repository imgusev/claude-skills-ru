---
title: "устойчивый к коллаборации { #collab-proof } — Агентский скилл для Codex и OpenClaw"
description: "Используйте, когда вы хотите понять, какой вклад внес Клод в сравнении с тем, что вы использовали во время сеанса. Триггеры для: /collab-proof. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# устойчивый к коллаборации { #collab-proof }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `collab-proof`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/collab-proof/skills/collab-proof/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Доказательства совместной работы Surfaces с искусственным интеллектом, которые разработчик сознательно не записывал.
3-уровневый пайплайн Vela × ADHD 4-фреймовое рассуждение — промпт - нативный, нулевые зависимости.

---

## Уровень 01 — Обнаружение сигнала { #layer-01--signal-detection }

Бежать `git log --oneline -10` и `git diff --stat HEAD~3..HEAD` первый.

Классифицируйте уровень сигнала, используя эту рубрику (выберите самый высокий, который соответствует):

**ВЫСОКИЙ** → полные артефакты (DECISIONS.md + история сеанса + РАБОЧИЙ журнал + HTML)
- Создан новый файл, ИЛИ
- изменено более 4 файлов, ИЛИ
- Явное сравнение вариантов в разговоре ("против", "вместо", "выбрал X вместо Y") ИЛИ
- Обсуждение дизайна длилось более 15 обменов мнениями, ИЛИ
- **Ошибка с диагностикой первопричины ** — беседа содержит ПРИЧИНУ возникновения ошибки
  (не просто "исправлен X", а "ошибка была вызвана Y, потому что Z")

**Специальное правило для исправления ошибок** — переопределяет количество файлов:
Даже если изменен только 1 файл, классифицируйте как ВЫСОКИЙ, если беседа содержит:
- Объяснение основной причины ("ошибка была...", "это произошло потому, что...", "проблема в...")
- Процесс диагностики ("Я проверил...", "оказалось...", "проблема заключалась в...")
- Исправьте обоснование ("выбрал этот подход, потому что...", "вместо X использовал Y, потому что...")
Количество файлов не имеет значения для ошибок — хорошо диагностированное исправление одного файла более ценно
, чем исправление 10 файлов без обсуждения.

**СРЕДНИЙ** → только РАБОЧИЙ ЖУРНАЛ
- 1-3 файла были изменены без обсуждения основной причины, ИЛИ
- Добавлена незначительная функция, компромиссы не обсуждаются

**НИЗКИЙ уровень** → тишина, сообщите пользователю "Обычный сеанс — ничего не записано".
- Никаких изменений кода, только планирование/обсуждение, ИЛИ
- Единичное тривиальное изменение без контекста ("измените этот текст", "исправьте опечатку", "переименуйте переменную")

Показать пользователю: `Signal: HIGH / MEDIUM / LOW — [one-line reason]`

---

## Слой 02 — Классификатор WorkIntentClassifier { #layer-02--workintentclassifier }

Запустите все четыре фрейма одновременно в контексте беседы + git diff.
Оцените каждый кадр от 0,0 до 1,0 баллов, используя приведенную ниже рубрику. Затем примените правила обрезки и классификации.

### Рубрика подсчета очков по кадрам { #frame-scoring-rubric }

**Кадр A — технический** (сложность оттока кода)
- `1.0` Создан новый модуль/файл, добавлена сложная логика (конечный автомат, Lua-скрипт, новый алгоритм)
- `0.5` Изменена логика существующей функции, добавлена простая конечная точка API
- `0.1` Исправление опечатки, изменение комментария, редактирование обычного текста

**Кадр B — Неопределенность** (сигналы сомнения разработчика)
- `1.0` Написанный код затем был полностью откатан, явно выражено сомнение ("이게 맞나?", "동작 안 하네"), `git revert`
- `0.5` Консультация, запрошенная у Клода в середине внедрения, более 2 запросов на пересмотр в одной и той же области
- `0.0` Бесперебойное выполнение директив — разработчик точно знал, что нужно создавать

**Рамка C — Fork** (наличие ответвления решения)
- `1.0` Две или более альтернативы, явно сравниваемые в разговоре (A против B)
- `0.5` Явного сравнения нет, но упоминается компромисс (производительность против удобочитаемости)
- `0.0` Применялся единый стандартный подход, альтернативы не рассматривались

**Вклад фрейма D — AI** (фактическое влияние Клода)
- `1.0` Клод выявил ошибку / крайний случай, который разработчик не заметил, и предложил исправить
- `0.6` Клод сгенерировал структурный шаблон/скелет, который значительно ускорил выполнение
- `0.2` Клод переформатировал или переписал код, направленный разработчиком, без независимого участия

---

### Правило для обрезки { #pruning-rule }

Сократите количество очков в любом кадре до < 0,4.

**Исключение — Защита от высокоскоростного выполнения:**
Если `Frame A >= 0.8` И `Frame D >= 0.6`, не обрезайте и не приостанавливайте сеанс,
даже если кадр B = 0.0 и кадр C = 0.0.
Это сеанс построения функций с большим количеством шаблонов. Немедленно классифицировать как `FEATURE_BUILDING` с `HIGH` сигнал.
Обоснование: нулевая неопределенность в быстро проходящей сессии - это особенность, а не причина отказываться от нее.

---

### Классификация намерений { #intent-classification }

| Уцелевшие рамы | Доминирующее намерение | Значение |
|---|---|---|
| A высокий + D средне-высокий (B, C низкий) | `FEATURE_BUILDING` | Высокоскоростная генерация объектов, строительные леса Claude |
| B высокий + A/D высокий | `BUG_FIXING` или `STUCK` | Активная отладка или неразрешенный цикл |
| C высокий + A высокий | `REFACTORING` или `EXPLORING` | Исследование архитектуры, взвешивание альтернатив |
| Все кадры < 0,4 | `FLOW_STATE` или НИЗКИЙ | Обычный набор текста, тишина, если только уровень 01 не был ВЫСОКИМ |

Если несколько намерений совпадают, выберите то, у которого самый высокий суммарный балл по фреймам.
Запишите занявшего второе место — это относится к описанию сессии.

---

### Внутренний выходной формат { #internal-output-format }

Прежде чем перейти к слою 03, перейдите к этой структуре (покажите ее пользователю).:

```json
{
  "frames": {
    "technical": 0.0,
    "uncertainty": 0.0,
    "fork": 0.0,
    "ai_contribution": 0.0
  },
  "pruned": ["list of pruned frame names"],
  "intent": "FEATURE_BUILDING",
  "signal": "HIGH",
  "calibration_note": "one sentence explaining any exception rule applied"
}
```

---

## Слой 03 — Вывод { #layer-03--output }

### Если ВЫСОКИЙ сигнал { #if-high-signal }

**Добавить к `DECISIONS.md`** — одна запись на реальную вилку (кадр C должен подтверждать существование альтернатив):

```markdown
## [YYYY-MM-DD] <title>

**Context**: [Frame A — what forced this choice]
**Decision**: what was chosen
**Alternatives considered**: [Frame C — road not taken]
**Reasoning**: why — prefix "inferred:" if reconstructed from context
**AI contribution**:
  - Identified: [Frame D — something developer missed]
  - Suggested: [Frame D — approach or alternative]
  - Developer-driven: [what the developer decided independently]
**Intent class**: [from Layer 02]
**Signal score**: HIGH
**Outcome**: implemented | pending | reversed
```

Если реального форка не существовало, → ничего не пишите. Никогда не выдумывайте решения.

**Намерение исправить ошибку: вместо этого используйте этот формат:**

```markdown
## [YYYY-MM-DD] <bug title>

**Root cause**: what actually caused the bug — the WHY, not just the what
**Symptom**: what the developer observed
**Fix**: what was changed
**Why this fix**: rationale — inferred if not stated explicitly
**Alternative fixes considered**: other approaches discussed (if any)
**AI contribution**:
  - Identified: [Frame D — did Claude spot the root cause?]
  - Suggested: [Frame D — fix approach or diagnostic step]
  - Developer-driven: [what the developer diagnosed/decided independently]
**Intent class**: BUG_FIXING
**Signal score**: HIGH
**Outcome**: fixed | workaround | deferred
```

**Создавать `session-history/YYYY-MM-DD-HHMM.md`**:

```markdown
# Session [YYYY-MM-DD HH:MM]

**Intent**: [class] (runner-up: [class if any])
**Signal**: HIGH
**Frames active**: A ([score]) / B ([score]) / C ([score]) / D ([score])

## What shipped
[grounded in git log]

## What was figured out
[Frame B + C — the reasoning, tradeoffs, debugging — what developers forget]

## Decisions made this session
[refs to DECISIONS.md entries]

## Where it got hard
[Frame B findings — uncertainty, reverts, EXPLORING/STUCK signals]

## AI contribution summary
[Frame D synthesis — one honest paragraph, calibrated]

## Next steps inferred
[what's obviously incomplete]
```

**Добавить к `WORKLOG.md`**:
```
YYYY-MM-DD HH:MM | [intent] | HIGH | D:[score] | cache:[hit%]% | tok:[total] | <verb phrase> — <why it mattered>
```

Поля:
- `D:[score]` — Оценка вклада искусственного интеллекта в кадр D (0.0–1.0)
- `cache:[hit%]%` — частота попадания в кэш по результатам анализа токенов (или `cache:n/a` если нет данных)
- `tok:[total]` — общее количество токенов в этом сеансе (ввод + cache_read + cache_create + вывод, например, в K `45K`)
- глагольная фраза — то, что отправлено, указано в git log

** Сбор данных об использовании токена ** (bash — запустите это и зафиксируйте выходные данные):
```bash
python3 -c "
import json, sys
from pathlib import Path

projects = Path.home() / '.claude/projects'
files = sorted(projects.rglob('*.jsonl'), key=lambda f: f.stat().st_mtime, reverse=True)
if not files:
    print('no_data'); sys.exit()

with open(files[0]) as fp:
    lines = [json.loads(l) for l in fp if l.strip()]

ti = to = cr = cc = 0
turns = []
for i, line in enumerate(lines):
    if line.get('type') == 'assistant':
        u = line.get('message', {}).get('usage', {})
        if not u: continue
        inp = u.get('input_tokens', 0)
        ti += inp; to += u.get('output_tokens', 0)
        cr += u.get('cache_read_input_tokens', 0)
        cc += u.get('cache_creation_input_tokens', 0)
        prompt = ''
        for j in range(i-1, -1, -1):
            if lines[j].get('type') == 'user':
                c = lines[j].get('message', {}).get('content', '')
                prompt = (c if isinstance(c, str) else next((x.get('text','') for x in c if isinstance(x,dict) and x.get('type')=='text'), ''))[:80]
                break
        turns.append((inp, prompt))

total = ti + cr + cc
hit = cr / total * 100 if total else 0
print(f'input={ti} output={to} cache_read={cr} cache_create={cc} hit={hit:.0f} turns={len(turns)}')
turns.sort(reverse=True)
for idx, (tok, p) in enumerate(turns[:3]):
    print(f'top{idx+1}={tok}|{p}')
"
```

Проанализируйте выходные данные и включите статистику токенов в описание сеанса. Затем:

**Генерировать `session-history/YYYY-MM-DD-HHMM-proof.html`** — напишите автономный HTML-файл. Структура и имена классов исправлены — не переименовывайте и не меняйте порядок разделов.

** Исправлены CSS-токены (используйте точно):**
- Предыстория: `#0d1117`, Карточка: `#161b22`, Граница: `#30363d`
- Шрифт: `font-family: 'Courier New', monospace`
- Цвета оценки кадра: `high` → `#3fb950`, `low` → `#f85149`, обрезанный → `#8b949e`
- Цвета линий AI: `ai-identified` → `#a371f7`, `ai-suggested` → `#d29922`, `ai-developer` → `#3fb950`

**Исправлена структура HTML (имена классов должны точно совпадать):**
```
<div class="header">
  <div class="header-top">
    <div class="project-name">
    <span class="badge">                    <!-- intent class -->
  <div class="meta-row">                    <!-- date, branch, signal level text -->
  <div class="signal-container">
    <div class="signal-label">
    <div class="signal-track">
      <div class="signal-fill">             <!-- width % driven by signal score -->

<div class="section">                       <!-- frames -->
  <div class="section-title"> ... <span class="count">Layer 02 · ADHD tree-of-thought</span>
  <div class="frames-grid">
    <div class="frame-card">               <!-- pruned: class="frame-card pruned" -->
      <div class="frame-label">            <!-- Frame A / B / C / D -->
      <div class="frame-name">
      <div class="frame-score high|low">   <!-- score value -->

<div class="section">                       <!-- decisions — skip section if none -->
  <div class="section-title"> ... <span class="count">N recorded</span>
  <div class="decision-card">              <!-- one per DECISIONS.md entry -->
    <div class="decision-header">
      <div class="decision-title">
      <div class="decision-date">
    <div class="decision-fields">
      <div class="field-row">
        <div class="field-label">          <!-- Context / Decision / Alternatives / Reasoning -->
        <div class="field-value">
      <div class="field-row">              <!-- AI contribution row -->
        <div class="field-label">AI contribution</div>
        <div class="field-value">
          <div class="ai-block">
            <div class="ai-line ai-identified|ai-suggested|ai-developer">
              <span class="tag">IDENTIFIED|SUGGESTED|DEV-DRIVEN</span>
      <div class="field-row">              <!-- Outcome row -->
        <div class="field-label">Outcome</div>
        <div class="field-value">
          <span class="outcome-badge outcome-implemented|outcome-pending|outcome-reversed">

<div class="section">                       <!-- session narrative -->
  <div class="section-title">Session narrative</div>
  <div class="narrative-grid">
    <div class="narrative-card">           <!-- What shipped -->
    <div class="narrative-card">           <!-- What was figured out -->
    <div class="narrative-card">           <!-- Where it got hard -->
    <div class="narrative-card">           <!-- Next steps inferred -->

<div class="section">                       <!-- AI contribution summary -->
  <div class="section-title">AI contribution summary</div>
  <div class="narrative-card">             <!-- Frame D synthesis paragraph -->

<div class="section">                       <!-- token usage -->
  <div class="section-title">Token usage</div>
  <div class="narrative-card">             <!-- cache hit rate bar + top turns + optimization note -->

<div class="section">                       <!-- worklog tail -->
  <div class="section-title"> ... <span class="count">last N entries</span>
  <div class="worklog-entry">              <!-- one per recent WORKLOG line -->

<div class="footer">                        <!-- last commit hash · "Generated by collab-proof · timestamp" -->
```

Напишите HTML-код с помощью bash:
```bash
cat > session-history/YYYY-MM-DD-HHMM-proof.html << 'HTMLEOF'
<!DOCTYPE html>
... (full HTML with inline CSS, no external resources)
HTMLEOF
```

После написания покажите: `open session-history/YYYY-MM-DD-HHMM-proof.html`

---

### Если СРЕДНИЙ сигнал { #if-medium-signal }

Добавьте одну строку к `WORKLOG.md` только:
```
YYYY-MM-DD HH:MM | [intent] | MEDIUM | D:[score] | cache:[hit%]% | tok:[total] | <verb phrase>
```

---

### Если НИЗКИЙ сигнал { #if-low-signal }

Сообщите пользователю: "Сигнал: НИЗКИЙ уровень рутинной сессии, ничего не записано".

---

## Правила честности { #honesty-rules }

- Никогда не придумывайте решения ни в разговоре, ни подразумеваемые различием
- "выводимый:" префикс при восстановлении рассуждения
- Рамка D должна быть откалибрована — ни подавайте повторный иск, ни отклоняйте его
- Если оценка всех кадров < 0.4 → ничего не писать

---

## Предварительный сжатый снимок (защита от сжатия контекста) { #precompact-snapshot-context-compaction-defence }

Когда вот-вот произойдет сжатие контекста (триггер, запускаемый перехватчиком предварительного сжатия),
запустите облегченную контрольную точку в середине сеанса, прежде чем контекст будет потерян:

1. Вычислить текущий уровень сигнала уровня 01 из доступного контекста
2. Сравните все четыре кадра с тем, что видно сейчас
3. Запишите моментальный снимок в `session-history/.tmp-TIMESTAMP.json`:

```json
{
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "trigger": "pre-compact",
  "signal": "HIGH / MEDIUM / LOW",
  "frames": { "technical": 0.0, "uncertainty": 0.0, "fork": 0.0, "ai_contribution": 0.0 },
  "intent": "FEATURE_BUILDING",
  "key_moments": [
    "one-line description of the most important decision or finding so far"
  ]
}
```

Когда `/collab-proof` запускается в конце сеанса:
- Прочитать все `session-history/.tmp-*.json` файлы
- Объединить оценки кадров (взять максимальное значение для каждого кадра во всех снимках)
- Комбинировать `key_moments` массивы — они сохраняют обсуждения компромиссов, которые были сведены воедино
- Удалить `.tmp-*.json` файлы после объединения
