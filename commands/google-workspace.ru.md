---
name: google-workspace
description: "Операции с интерфейсом Google Workspace CLI: диагностика настроек, аудит безопасности, поиск рецептов и анализ выходных данных. Использование: /google-workspace <настройка|аудит|рецепт|анализ> [параметры]"
argument-hint: "<setup|audit|recipe|analyze> [options]"
---

# /google-рабочее пространство { #google-workspace }

Администрирование CLI Google Workspace с помощью `gws` CLI. Запускайте диагностику установки, аудит безопасности, просматривайте и выполняйте рецепты, а также анализируйте выходные данные команд.

## Использование { #usage }

```
/google-workspace setup [--json]
/google-workspace audit [--services gmail,drive,calendar] [--json]
/google-workspace recipe list [--persona <role>] [--json]
/google-workspace recipe search <keyword> [--json]
/google-workspace recipe run <name> [--dry-run]
/google-workspace recipe describe <name>
/google-workspace analyze [--filter <field=value>] [--group-by <field>] [--stats <field>] [--format table|csv|json]
```

## Примеры { #examples }

```
/google-workspace setup
/google-workspace audit --services gmail,drive --json
/google-workspace recipe list --persona pm
/google-workspace recipe search "email"
/google-workspace recipe run standup-report --dry-run
/google-workspace recipe describe morning-briefing
/google-workspace analyze --filter "mimeType=pdf" --select "name,size" --format table
```

## Сценарии { #scripts }

- `engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/gws_doctor.py` — Предполетная диагностика
- `engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/auth_setup_guide.py` — Руководство по настройке авторизации
- `engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/gws_recipe_runner.py` — Каталог рецептов и бегунок
- `engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/workspace_audit.py` — Аудит безопасности
- `engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/output_analyzer.py` — Анализатор JSON/NDJSON

## Подкоманды { #subcommands }

### настройка { #setup }
Запустите предполетную диагностику и проверку подлинности.
```bash
python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/gws_doctor.py [--json]
python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/auth_setup_guide.py --validate [--json]
```

### аудит { #audit }
Запустите аудит безопасности и конфигурации.
```bash
python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/workspace_audit.py [--services gmail,drive,calendar] [--json]
```

### рецепт { #recipe }
Просматривайте, ищите и выполняйте 43 встроенных рецепта gws.
```bash
python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/gws_recipe_runner.py --list [--persona <role>] [--json]
python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/gws_recipe_runner.py --search <keyword> [--json]
python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/gws_recipe_runner.py --describe <name>
python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/gws_recipe_runner.py --run <name> [--dry-run]
```

### анализировать { #analyze }
Анализируйте, фильтруйте и агрегируйте выходные данные JSON из любой команды gws.
```bash
gws <command> --json | python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/output_analyzer.py [options]
python3 engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/output_analyzer.py --demo --format table
```

## Ссылка на Скилл { #skill-reference }
-> `engineering-team/google-workspace-cli/skills/google-workspace-cli/SKILL.md`

## Связанные команды { #related-commands }
- Нет прямых зависимостей (автономный скилл Google Workspace)
