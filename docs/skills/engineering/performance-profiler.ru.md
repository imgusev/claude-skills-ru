---
title: "Профилировщик производительности { #performance-profiler } — Агентский скилл для Codex и OpenClaw"
description: "Систематическое профилирование производительности для Node.js , приложения Python и Go. Определяет узкие места процессора, памяти и ввода-вывода. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Профилировщик производительности { #performance-profiler }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `performance-profiler`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/performance-profiler/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Уровень:** МОЩНЫЙ  
**Категория:** Инженерия  
**Предметная область:** Разработка производительности  

---

## Обзор { #overview }

Систематическое профилирование производительности для Node.js , приложения Python и Go. Определяет узкие места процессора, памяти и ввода-вывода; генерирует flamegraphs; анализирует размеры пакетов; оптимизирует запросы к базе данных; обнаруживает утечки памяти; и запускает нагрузочные тесты с помощью k6 и Artillery. Всегда измеряйте до и после.

## Основные возможности { #core-capabilities }

- **Профилирование процессора** — графики пламени для Node.js , py-spy для Python, pprof для Go
- **Профилирование памяти** — моментальные снимки кучи, обнаружение утечек, давление GC
- **Анализ пакетов** — webpack-bundle-analyzer, Next.js анализатор пакетов
- ** Оптимизация базы данных ** — ПОЯСНИТЕЛЬНЫЙ АНАЛИЗ, медленный журнал запросов, обнаружение N+1
- **Нагрузочное тестирование** — сценарии k6, артиллерийские сценарии, схемы наращивания
- **До того, как/after измерение** — установление базовой линии, профилирование, оптимизация, проверка

---

## Когда использовать { #when-to-use }

- Приложение работает медленно, и вы не знаете, где находится узкое место
- Задержка P99 превышает SLA перед выпуском
- Использование памяти растет с течением времени (подозреваемая утечка)
- Размер пакета увеличился после добавления зависимостей
- Подготовка к скачку трафика (нагрузочный тест перед запуском)
- Запросы к базе данных занимают >100 мс

---

## Быстрый старт { #quick-start }

```bash
# Analyze a project for performance risk indicators
python3 scripts/performance_profiler.py /path/to/project

# JSON output for CI integration
python3 scripts/performance_profiler.py /path/to/project --json

# Custom large-file threshold
python3 scripts/performance_profiler.py /path/to/project --large-file-threshold-kb 256
```

---

## Золотое правило: Сначала измерьте { #golden-rule-measure-first }

```bash
# Establish baseline BEFORE any optimization
# Record: P50, P95, P99 latency | RPS | error rate | memory usage

# Wrong: "I think the N+1 query is slow, let me fix it"
# Right: Profile → confirm bottleneck → fix → measure again → verify improvement
```

---

## Node.js Профилирование { #nodejs-profiling }
→ Смотрите ссылки/profiling-recipes.md для получения подробной информации

## Ссылки { #references }

- [ссылки/profiling-recipes.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/performance-profiler/references/profiling-recipes.md) — Команды профилирования Node.js/Python/Go, генерация flamegraph, моментальные снимки кучи
- [ссылки/optimization-playbook.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/performance-profiler/references/optimization-playbook.md) — до того, как/after шаблон измерения, чек-лист для быстрой оптимизации (DB/Node)./bundle/API), распространенные подводные камни, лучшие практики

