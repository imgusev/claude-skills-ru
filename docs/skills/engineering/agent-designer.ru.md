---
title: "Конструктор агентов — Архитектура мультиагентной системы для агентов { #agent-designer--multi-agent-system-architecture } — Агентский скилл для Codex и OpenClaw"
description: "Использовать, когда пользователь просит конструкция мульти-агент системы, выбрать оркестрация оркестровки (трубопровод руководителем/Рой пайплайн). Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Конструктор агентов — Архитектура мультиагентной системы для агентов { #agent-designer--multi-agent-system-architecture }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `agent-designer`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/agent-designer/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Проектируйте, генерируйте схемы и оценивайте мультиагентные системы с помощью трех детерминированных инструментов. ...Агент Сценарии — это воркфлоу - не создавайте архитектуру от руки, когда планировщик может выбрать ее из требований.

## Когда использовать { #when-to-use }

- Проектирование нового мульти-агент системы от потребностей (выбор шаблона, ролей, коммуникаций)
- Создание готовых к использованию поставщиком схем инструментов (форматы Anthropic + OpenAI) на основе простых описаний инструментов
- Оценка журналов выполнения: показатель успешности, распределение задержек, стоимость, узкие места

**Когда не следует использовать:** Воркфлоу Claude Code-автоматизация инструментов → `workflow-builder`; каркасы воркфлоу с одним агентом → `agent-workflow-designer`; разветвление мультиагентного агента во время выполнения → `agenthub`.

## Таблица принятия решений по шаблону { #pattern-decision-table }

| Выбирай | Когда | Следите за |
|---|---|---|
| Единый агент | Одна ограниченная задача, < ~5 инструментов | Не добавляйте агентов, которые вам не нужны |
| Руководитель | Центральное разложение, специалисты отчитываются | Супервайзер становится узким местом |
| Пайплайн | Строго последовательные этапы с хэндоффами | Жесткий порядок; пропускная способность гейтов самой низкой ступени |
| Иерархический | Несколько организационных уровней, > ~8 агентов | Накладные расходы на связь на каждом уровне |
| Рой | Параллельные одноранговые узлы, отказоустойчивость превыше предсказуемости | Трудно поддается отладке; нужны согласованные правила |

Планировщик применяет эту оценку детерминированно — запускает ее, а не выбирает на ощупь.

## Воркфлоу { #workflow }

Все пути относительно этой папки с скиллами. Выходные данные JSON каждого шага являются входными данными для проектирования следующего шага.

### 1. Спроектируйте архитектуру { #1-design-the-architecture }

Напишите JSON-файл требований (скопируйте `assets/sample_system_requirements.json` — ключи: `goal`, `tasks[]`, `constraints{max_response_time, budget_per_task, concurrent_tasks}`, `team_size`):

```bash
python3 agent_planner.py requirements.json --format json -o arch
```

Испускает `arch.json` с `architecture_design` (шаблон, агенты, каналы связи), `mermaid_diagram`, и `implementation_roadmap`. Читать `architecture_design.pattern` и список ролей для каждого агента; представьте пользователю диаграмму mermaid.

### 2. Создайте схемы инструментов { #2-generate-tool-schemas }

Опишите инструменты каждого агента в обычном формате JSON (скопируйте `assets/sample_tool_descriptions.json`), затем:

```bash
python3 tool_schema_generator.py tool_descriptions.json --validate -o tools
```

Испускает `tools.json` (`tool_schemas`, `validation_summary`) плюс специфичный для поставщика `tools_anthropic.json` / `tools_openai.json`. **Гейт: каждый инструмент должен печатать `✓ Valid`.** Исправьте любую недопустимую схему, прежде чем продолжить — никогда не передавайте агенту непроверенную схему.

### 3. Оцените журналы выполнения { #3-evaluate-execution-logs }

Как только система запустится (или против `assets/sample_execution_logs.json` для пробного прогона):

```bash
python3 agent_evaluator.py execution_logs.json --detailed -o eval
```

Испускает `eval.json` с `summary`, `agent_metrics`, `bottleneck_analysis`, `error_analysis`, `cost_breakdown`, `sla_compliance`, и `optimization_recommendations`, плюс разделенные файлы (`eval_errors.json`, `eval_recommendations.json`).

### 4. цикл проверки { #4-verification-loop }

Дизайн не будет завершен до тех пор, пока:

1. `tool_schema_generator.py --validate` сообщает о 0 недопустимых схемах.
2. `agent_evaluator.py` при пилотном запуске сообщает **о 0 критических проблемах** (инструмент печатает `CRITICAL: N critical issues` когда будет найден). Если N > 0, примените верхний элемент в `eval_recommendations.json`, повторно запустите пилотный проект и повторите оценку.
3. Сравните ваши результаты с `expected_outputs/` чтобы убедиться, что форма схемы, которую вы используете, не изменилась.

## Ссылки { #references }

- `references/agent_architecture_patterns.md` — глубинные компромиссы по шаблону
- `references/tool_design_best_practices.md` — схема, идемпотентность, правила обработки ошибок
- `references/evaluation_methodology.md` — определения показателей, которые реализует оценщик
