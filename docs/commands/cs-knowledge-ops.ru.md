---
title: "/cs-knowledge-ops — слэш-команда для ИИ-агентов разработки"
description: "Разработка рансбука компании SOP+ с проверкой полноты 5W2H. НЕ личный PKM (это llm-wiki). НЕ рансбуки, относящиеся к инженерной тематике. Прямое. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-knowledge-ops

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/business-operations/commands/cs-knowledge-ops.md">Источник</a></span>
</div>


Запустите `knowledge-ops` скилл на основе этого ввода:

**$АРГУМЕНТЫ**

## Воркфлоу с тремя инструментами { #three-tool-workflow }

1. **`sop_generator.py`** — Стандартная процедура работы со строительными лесами 5W2H (Кто/что/Когда/Где/Почему/Как/Почем). Отраслевая настройка `--profile {ops,support,finance,hr,it,regulated}` для строительных лесов высокого уровня соответствия требованиям.

2. **`runbook_validator.py`** — Проверка полноты работы рансбука: у каждого шага есть владелец, ожидаемая продолжительность, наблюдаемый сигнал успеха/неудачи, путь отката. Указывает на неоднозначность ("убедитесь, что служба запущена" → "какова команда проверки?").

3. **`kb_ingester.py`** — Использование Markdown KB: обнаружение перекрестных ссылок, смещение глоссария, обнаружение потерянных страниц.

## Отличный от { #distinct-from }

- `engineering/llm-wiki` — персональный ПК (ваш второй мозг). Knowledge-ops - это вики-сайт **компании**.
- `engineering-team/runbook-generator` — рансбуки для инженерных целей (system ops). Knowledge-ops распространяется на всю организацию.
- `project-management/*` — Отслеживание доставки Jira /Confluence, а не авторство.
- `business-operations/skills/process-mapper` (родственник) — процесс *проектирования*, а не документация.
