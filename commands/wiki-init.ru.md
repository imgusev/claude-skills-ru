---
name: wiki-init
description: "Загрузите свежее хранилище LLM Wiki с трехуровневой структурой, файлами схем и начальными шаблонами. Использование /wiki-init <путь> --тема \"<тема>\" [--tool all|claude-code|codex|курсор|антигравитация]"
---
<!-- canonical copy: engineering/llm-wiki/commands/wiki-init.md — keep in sync -->

# /wiki-init { #wiki-init }

Загрузите новое вики-хранилище LLM. Создает `raw/`, `wiki/{entities,concepts,sources,comparisons,synthesis}`, индекс и журнал, и устанавливает файл(ы) схемы для выбранного вами LLM CLI.

## Использование { #usage }

```
/wiki-init <path> --topic "<one-line topic>"
/wiki-init <path> --topic "<topic>" --tool <claude-code|codex|cursor|antigravity|opencode|gemini-cli|all>
/wiki-init <path> --topic "<topic>" --force    # overwrite non-empty dir
```

## Примеры { #examples }

```
/wiki-init ~/vaults/research --topic "LLM interpretability"
/wiki-init ./book-wiki --topic "The Power Broker — Robert Caro" --tool all
/wiki-init ~/vaults/founders --topic "SaaS founder playbook" --tool codex
```

## Что это создает { #what-it-creates }

```
<path>/
├── raw/
│   └── assets/
├── wiki/
│   ├── index.md              # from template
│   ├── log.md                # from template
│   ├── entities/
│   ├── concepts/
│   ├── sources/
│   ├── comparisons/
│   ├── synthesis/
│   └── .templates/           # page templates for reference
├── CLAUDE.md                 # if --tool claude-code or all
├── AGENTS.md                 # if --tool codex|cursor|antigravity|opencode|gemini-cli|all
├── .cursorrules              # if --tool cursor or all
└── .gitignore
```

## Следующие шаги { #next-steps }

После инициализации:
1. Откройте хранилище в обсидиане
2. Поместите источник в `raw/`
3. Бежать `/wiki-ingest raw/<your-file>`

## Сценарий { #script }

- `engineering/llm-wiki/skills/llm-wiki/scripts/init_vault.py`

## Ссылка на Скилл { #skill-reference }

→ `engineering/llm-wiki/skills/llm-wiki/SKILL.md`
