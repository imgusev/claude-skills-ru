---
name: pipeline
description: "Обнаруживайте стек и генерируйте конфигурации пайплайна CI/CD. Использование: /пайплайн <обнаружение|генерация> [параметры]"
argument-hint: "<detect|generate> [options]"
---

# /пайплайн { #pipeline }

Обнаруживайте стек проекта и генерируйте конфигурации пайплайна CI/CD для GitHub Actions или GitLab CI.

## Использование { #usage }

```
/pipeline detect [--repo <project-dir>]               Detect stack, tools, and services
/pipeline generate --platform github|gitlab [--repo <project-dir>]  Generate pipeline YAML
```

## Примеры { #examples }

```
/pipeline detect --repo ./my-project
/pipeline generate --platform github --repo .
/pipeline generate --platform gitlab --repo .
```

## Сценарии { #scripts }
- `engineering/skills/ci-cd-pipeline-builder/scripts/stack_detector.py` — Обнаружение штабеля и оснастки (`--repo <path>`, `--format text|json`)
- `engineering/skills/ci-cd-pipeline-builder/scripts/pipeline_generator.py` — Сгенерировать пайплайн YAML (`--platform github|gitlab`, `--repo <path>`, `--input <stack.json>`, `--output <file>`)

## Ссылка на Скилл { #skill-reference }
→ `engineering/skills/ci-cd-pipeline-builder/SKILL.md`
