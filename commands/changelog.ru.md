---
name: changelog
description: "Генерируйте списки изменений из истории git и проверяйте обычные фиксации. Использование: /журнал изменений <сгенерировать|lint> [параметры]"
argument-hint: "<generate|lint> [options]"
---

# /список изменений { #changelog }

Сгенерируйте записи журнала изменений из истории git и подтвердите формат сообщения о фиксации.

## Использование { #usage }

```
/changelog generate [--from-tag <tag>] [--to-tag <tag>]    Generate changelog entries
/changelog lint [--from-ref <ref>] [--to-ref <ref>]       Lint commit messages
```

## Примеры { #examples }

```
/changelog generate --from-tag v2.0.0
/changelog lint --from-ref main --to-ref dev
/changelog generate --from-tag v2.0.0 --to-tag v2.1.0 --format markdown
```

## Сценарии { #scripts }
- `engineering/skills/changelog-generator/scripts/generate_changelog.py` — Разбор коммитов, рендеринг журнала изменений (`--from-tag`, `--to-tag`, `--from-ref`, `--to-ref`, `--format markdown|json`)
- `engineering/skills/changelog-generator/scripts/commit_linter.py` — Проверка обычного формата фиксации (`--from-ref`, `--to-ref`, `--strict`, `--format text|json`)

## Ссылка на Скилл { #skill-reference }
→ `engineering/skills/changelog-generator/SKILL.md`
