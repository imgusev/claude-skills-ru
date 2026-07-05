---
title: "/si:ревью — Автоматический анализ памяти { #sireview--analyze-auto-memory } — Агентский скилл и плагин Codex"
description: "Проанализируйте автоматическую память на предмет кандидатов на повышение, устаревших записей, возможностей консолидации и показателей. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /si:ревью — Автоматический анализ памяти { #sireview--analyze-auto-memory }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/self-improving-agent/skills/review/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Выполняет всесторонний аудит автоматической памяти Claude Code и выдает практические рекомендации.

## Использование { #usage }

```
/si:review                    # Full review
/si:review --quick            # Summary only (counts + top 3 candidates)
/si:review --stale            # Focus on stale/outdated entries
/si:review --candidates       # Show only promotion candidates
```

## Что он делает { #what-it-does }

### Шаг 1: Найдите каталог памяти { #step-1-locate-memory-directory }

```bash
# Find the project's auto-memory directory
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"

# Fallback: check common path patterns
# ~/.claude/projects/<user>/<project>/memory/
# ~/.claude/projects/<absolute-path>/memory/

# List all memory files
ls -la "$MEMORY_DIR"/
```

Если каталог памяти не существует, сообщите, что автоматическое запоминание может быть отключено. Предлагаю проконсультироваться с `/memory`.

### Шаг 2: Прочитайте и проанализируйте MEMORY.md { #step-2-read-and-analyze-memorymd }

Прочитайте полный текст `MEMORY.md` файл. Подсчитайте строки и проверьте, соответствует ли ограничение на запуск в 200 строк.

Проанализируйте каждую запись на предмет:

1. **Показатели повторяемости**
   - Одно и то же понятие встречается несколько раз (разные формулировки)
   - Ссылки на "снова", или "все еще", или "продолжает происходить"
   - Похожие записи в файлах тем

2. **Индикаторы несвежести**
   - Ссылается на файлы, которые больше не существуют (`find` для проверки)
   - Упоминает устаревшие инструменты, версии или команды
   - Противоречит текущему CLAUDE.md правила

3. **Возможности консолидации**
   - Несколько записей на одну и ту же тему (например, три строки о тестировании)
   - Записи, которые можно было бы объединить в одно краткое правило

4. **Кандидаты на повышение по службе** — заявки, соответствующие ВСЕМ критериям:
   - Появлялось более чем на 2 сессиях (проверьте шаблоны формулировок)
   - Не относящиеся к конкретному проекту мелочи (в целом полезные)
   - Применимый к действию (может быть записан в виде конкретного правила)
   - Еще не в CLAUDE.md или `.claude/rules/`

### Шаг 3: Прочитайте файлы тем { #step-3-read-topic-files }

Если `MEMORY.md` ссылки или каталог содержит дополнительные файлы (`debugging.md`, `patterns.md` и т.д.):
- Прочтите каждый из них
- Перекрестная ссылка с MEMORY.md для дубликатов
- Проверьте, нет ли записей, которые принадлежат основному файлу (высокое значение), в сравнении с файлами тем (подробности).

### Шаг 4: Перекрестная ссылка с CLAUDE.md { #step-4-cross-reference-with-claudemd }

Ознакомьтесь с проектом `CLAUDE.md` (если он существует) и сравните:
- Есть ли там MEMORY.md записи, которые дублируют друг друга CLAUDE.md правила? (→ удалить из памяти)
- Есть ли там MEMORY.md записи, которые противоречат CLAUDE.md ? (→ конфликт флагов)
- Есть ли там MEMORY.md паттерны, которых еще нет в CLAUDE.md так и должно быть? (→ кандидат на повышение по службе)

Также проверьте `.claude/rules/` каталог для существующих правил с ограниченной областью действия.

### Шаг 5: Сгенерируйте отчет { #step-5-generate-report }

Выходной формат:

```
📊 Auto-Memory Review

Memory Health:
  MEMORY.md:        {{lines}}/200 lines ({{percent}}%)
  Topic files:      {{count}} ({{names}})
  CLAUDE.md:        {{lines}} lines
  Rules:            {{count}} files in .claude/rules/

🎯 Promotion Candidates ({{count}}):
  1. "{{pattern}}" — seen {{n}}x, applies broadly
     → Suggest: {{target}} (CLAUDE.md / .claude/rules/{{name}}.md)
  2. ...

🗑️ Stale Entries ({{count}}):
  1. Line {{n}}: "{{entry}}" — {{reason}}
  2. ...

🔄 Consolidation ({{count}} groups):
  1. Lines {{a}}, {{b}}, {{c}} all about {{topic}} → merge into 1 entry
  2. ...

⚠️ Conflicts ({{count}}):
  1. MEMORY.md line {{n}} contradicts CLAUDE.md: {{detail}}

💡 Recommendations:
  - {{actionable suggestion}}
  - {{actionable suggestion}}
```

## Когда использовать { #when-to-use }

- После завершения основной функции или сеанса отладки
- Когда `/si:status` показывает MEMORY.md составляет более 150 строк
- Еженедельно во время активной разработки
- Перед началом нового этапа проекта
- После онбординга с новым членом команды (ревью к тому, чему научился Клод)

## Советы { #tips }

- Бежать `/si:review --quick` часто (низкие накладные расходы)
- Полный ревью наиболее ценен, когда MEMORY.md становится многолюдно
- Действуйте в отношении кандидатов на повышение оперативно — это проверенные методы
- Не стесняйтесь удалять устаревшие записи — при необходимости автоматическая память выполнит повторное обучение
