---
title: "Рецензент кода { #code-reviewer } — Агентский скилл и плагин Codex"
description: "Автоматизация ревью кода для TypeScript, JavaScript, Python, Go, Swift, Kotlin, C#, .NET, Java, C, C++, Rust, Ruby, PHP и Dart/Flutter. Анализирует. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Рецензент кода { #code-reviewer }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `code-reviewer`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/code-reviewer/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Автоматизированные инструменты ревью кода для анализа запросов на извлечение, выявления проблем с качеством кода и создания отчетов о ревью.

---

## Как организован этот Скилл { #how-this-skill-is-organized }

```
code-reviewer/
  SKILL.md                        ← you are here (tools + dispatch table)
  rules/
    universal.md                  ← security, async, resources, exceptions, performance — all languages
  languages/
    python.md                     ← Python-specific rules + idioms
    typescript.md                 ← TypeScript / JavaScript-specific rules + idioms
    go.md                         ← Go-specific rules + idioms
    swift.md                      ← Swift-specific rules + idioms
    kotlin.md                     ← Kotlin-specific rules + idioms
    csharp.md                     ← C# / .NET-specific rules + idioms
    java.md                       ← Java-specific rules + idioms
    c.md                          ← C -specific rules + idioms
    cpp.md                        ← C++ -specific rules + idioms
    rust.md                       ← Rust -specific rules + idioms
    ruby.md                       ← Ruby -specific rules + idioms
    php.md                        ← PHP-specific rules + idioms
    dart.md                       ← Dart / Flutter-specific rules + idioms
```

### Порядок загрузки для каждого ревью { #loading-order-for-every-review }

1. Этот файл (`SKILL.md`) — инструменты и пороговые значения
2. `rules/universal.md` — всегда, для любого языка
3. Совпадающий `languages/*.md` — один файл, основанный на таблице расширений, приведенной ниже

Это всегда ровно ** 2 дополнительных файла**, независимо от области применения.

| Расширение(ы) | Нагрузка |
|---|---|
| `.py` | `languages/python.md` |
| `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs` | `languages/typescript.md` |
| `.go` | `languages/go.md` |
| `.swift` | `languages/swift.md` |
| `.kt`, `.kts` | `languages/kotlin.md` |
| `.cs`, `.csx`, `.razor`, `.cshtml` | `languages/csharp.md` |
| `.java` | `languages/java.md` |
| `.c`, `.h` | `languages/c.md` |
| `.cpp`, `.cc`, `.cxx`, `.hpp`, `.hh`, `.hxx` | `languages/cpp.md` |
| `.rs` | `languages/rust.md` |
| `.rb`, `.rake`, `.gemspec`, `.ru` | `languages/ruby.md` |
| `.php`, `.phtml` | `languages/php.md` |
| `.dart` | `languages/dart.md` |

---

## Инструменты { #tools }

### PR-анализатор { #pr-analyzer }

Анализирует разницу между ветвями git для оценки сложности ревью и выявления рисков.

```bash
# Analyze current branch against main
python scripts/pr_analyzer.py /path/to/repo

# Compare specific branches
python scripts/pr_analyzer.py . --base main --head feature-branch

# JSON output for integration
python scripts/pr_analyzer.py /path/to/repo --json
```

**Что он обнаруживает (универсальный — смотрите также языковой файл для сигналов, специфичных для конкретного языка):**
- Жестко закодированные секреты (пароли, ключи API, токены, строки подключения)
- Шаблоны ввода SQL / запросов
- Инструкции отладки, оставленные в производственном коде
- Примечания по подавлению ворса / анализатора
- Комментарии TODO/FIXME

**Специфичные для языка средства обнаружения** определены в каждом `languages/*.md` файл.

**Выходные данные включают в себя:**
- Оценка сложности (1-10)
- Классификация рисков (критический, высокий, средний, низкий)
- Определение приоритетности файлов для заказа на ревью
- Проверка сообщения о фиксации

---

### Средство проверки качества кода { #code-quality-checker }

Анализирует исходный код на предмет структурных проблем, запахов кода и серьезных нарушений.

```bash
# Analyze a directory
python scripts/code_quality_checker.py /path/to/code

# Analyze specific language
# Valid values: python, typescript, javascript, go, swift, kotlin, csharp, java, c, cpp, rust, ruby, php, dart
python scripts/code_quality_checker.py . --language java

# JSON output
python scripts/code_quality_checker.py /path/to/code --json
```

**Универсальные пороговые значения:**

| Проблема | Порог |
|-------|-----------|
| Длительная функция | >50 строк |
| Большой файл | >500 строк |
| Класс бога | >20 методов |
| Слишком много параметров | >5 |
| Глубокое гнездование | >4 уровня |
| Высокая сложность | >10 филиалов |

Проверки, зависящие от языка, определены в каждом `languages/*.md` файл.

---

### Генератор отчетов о ревью { #review-report-generator }

Объединяет PR-анализ и выводы о качестве кода в структурированные отчеты о ревью.

```bash
# Generate report for current repo
python scripts/review_report_generator.py /path/to/repo

# Markdown output
python scripts/review_report_generator.py . --format markdown --output review.md

# Use pre-computed analyses
python scripts/review_report_generator.py . \
  --pr-analysis pr_results.json \
  --quality-analysis quality_results.json
```

**Вердикты:**

| Оценка | Вердикт |
|-------|---------|
| 90+ без серьезных проблем | Одобряю |
| 75+ с ≤2 высокими проблемами | Одобрить с предложениями |
| 50-74 | Запросить изменения |
| <50 или критические проблемы | Блокировать |

---

## Добавление нового языка { #adding-a-new-language }

**Рекомендации рецензента (обязательно):**

1. Создавать `languages/<name>.md` используя любой существующий языковой файл в качестве шаблона — в нем должны быть разделы: Сигналы PR-анализатора, Проверка качества кода, Безопасность, Асинхронность, Управление ресурсами, Обработка исключений, Производительность, Идиомы.
2. Добавьте дополнительную строку в приведенную выше таблицу отправки.

Это все, что нужно для ревью, управляемого агентом.

**Поддержка детерминированного анализатора (необязательно, рекомендуется):** входящие в комплект скрипты
помечают только тот язык, который они явно знают. Чтобы сделать `code_quality_checker.py`
оцените новый язык:

3. Добавьте расширения в `LANGUAGE_EXTENSIONS` в `scripts/code_quality_checker.py` (это также добавляет `--language` выбор).
4. Добавить `function` / `class` / `method` записи регулярных выражений для языка в том же файле; в противном случае он возвращается к шаблонам Python.
5. При необходимости добавьте `check_<name>_specific_smells(...)` детектор (смотрите разделы на C#, Java и C) и вызовите его из `analyze_file`.
6. Добавить `assets/sample_<name>_smells.<ext>` + `_clean` фиксирует и фиксирует ожидаемое `--json` вывод под `expected_outputs/` как защитник от регрессии.

---

## Регрессионные приспособления { #regression-fixtures }

Помеченные светильники находятся в `assets/` с их преданными `--json` вывод в
`expected_outputs/` (C#, Java и C). Отклонение от зафиксированного JSON сигнализирует
об изменении поведения анализатора:

```bash
python scripts/code_quality_checker.py assets/sample_java_smells.java --json \
  | diff - expected_outputs/sample_java_smells_quality.json
```
