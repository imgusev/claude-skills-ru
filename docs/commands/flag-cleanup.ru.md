---
title: "/flag-cleanup — слэш-команда для ИИ-агентов разработки"
description: "Запустите воркфлоу ежеквартальной очистки флагов функций в текущем репозитории. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /flag-cleanup

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/flag-cleanup.md">Источник</a></span>
</div>


Запустите полный воркфлоу очистки флагов функций.:

1. Сканировать на наличие устаревших флагов (старше 90 дней, используется в ≤2 местах)
2. Для каждого кандидата укажите представляющего PR/проблему и текущего владельца
3. Сгенерируйте план удаления, сгруппированный по владельцу
4. Запустите аудит kill-switch для реестра flag-doc
5. Выведите отчет о Markdown, готовый для обмена с командой

## Использование { #usage }

```
/flag-cleanup
/flag-cleanup --max-age-days 60
/flag-cleanup --flag-doc runbooks/flags.md
```

## Реализация { #implementation }

Эта команда отправляется в `feature-flags-architect` скилл:

```bash
SKILL=engineering/feature-flags-architect/skills/feature-flags-architect

# Step 1: scan for debt
python "$SKILL/scripts/flag_debt_scanner.py" --repo . --max-age-days "${MAX_AGE_DAYS:-90}" --format json > .flag-debt.json

# Step 2: audit kill switches
python "$SKILL/scripts/kill_switch_audit.py" --repo . --flag-doc "${FLAG_DOC:-docs/feature-flags.md}" --format json > .kill-switch-audit.json

# Step 3: synthesize a markdown report
# (Claude reads both JSON files, groups by owner, drafts the cleanup plan)
```

## Выход { #output }

Отчет о Markdown с:

- **Кандидаты с устаревшими флагами ** сгруппированы по владельцам, с введением ссылок на фиксацию
- **Недокументированные флаги**, которые не проходят аудит kill-switch
- **Неполная документация** (отсутствуют поля для каждого флага)
- **Рекомендуемые инструкции по удалению** — по одной на каждого владельца

## Предварительные условия { #pre-conditions }

- Запуск из репозитория git с зафиксированным исходным кодом
- Существует реестр flag-doc (по умолчанию: `docs/feature-flags.md`)
- Тот `feature-flags-architect` установлен скилл

## Постусловия { #post-conditions }

- `.flag-debt.json` и `.kill-switch-audit.json` записывается в корневой каталог репозитория (игнорируется через `.gitignore`)
- Отчет Markdown, переданный потоковой передачей на терминал
- Напечатан рекомендуемый следующий шаг (с какого PR удаления начать)
