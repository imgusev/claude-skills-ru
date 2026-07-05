---
title: "Скиллы инженерной команды { #engineering-team-skills } — Агентский скилл и плагин Codex"
description: "Индекс набора скилл инженерной команды для Claude Code, Codex, Gemini CLI, Cursor, OpenClaw и еще 6 инструментов. Архитектура, интерфейс, бэкенд."
---

# Скиллы инженерной команды { #engineering-team-skills }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `engineering-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/engineering-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


32 готовых к производству инженерных скилла, объединенных в основные инженерные области, безопасность, AI /ML / данные и специализированные инструменты.

## Быстрый старт { #quick-start }

### Код Клода { #claude-code }
```
/read engineering-team/skills/senior-fullstack/SKILL.md
```

### Codex CLI { #codex-cli }
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/engineering-team
```

## Обзор скиллы { #skills-overview }

### Основные инженерные знания (13 скилл) { #core-engineering-13-skills }

| Скилл | Папка | Сосредоточься |
|-------|--------|-------|
| Старший архитектор | `senior-architect/` | Системный дизайн, архитектурные паттерны |
| Старший интерфейс | `senior-frontend/` | Реагировать, Next.js , Машинопись, Попутный ветер |
| Старший серверный сервер | `senior-backend/` | Разработка API, оптимизация базы данных |
| Старший полный состав | `senior-fullstack/` | Строительные леса проекта, качество кода |
| Старший специалист по контролю качества | `senior-qa/` | Генерация тестов, анализ покрытия |
| Старший разработчик | `senior-devops/` | CI/CD, инфраструктура, контейнеры |
| Старшие секопы | `senior-secops/` | Операции по обеспечению безопасности, управление уязвимостями |
| Рецензент кода | `code-reviewer/` | PR-ревью, анализ качества кода |
| Старший сотрудник службы безопасности | `senior-security/` | Моделирование угроз, STRIDE, тестирование на проникновение |
| Архитектор решений AWS | `aws-solution-architect/` | Бессерверная, облачная информация, оптимизация затрат |
| Менеджер арендаторов MS365 | `ms365-tenant-manager/` | Администрирование Microsoft 365 |
| Руководство по TDD | `tdd-guide/` | Воркфлоу-разработки, управляемые тестированием |
| Оценщик технического стека | `tech-stack-evaluator/` | Сравнение технологий, анализ совокупной стоимости владения |

### AI/ML/Data (5 скилл) { #aimldata-5-skills }

| Скилл | Папка | Сосредоточься |
|-------|--------|-------|
| Старший специалист по обработке данных | `senior-data-scientist/` | Статистическое моделирование, экспериментирование |
| Старший инженер по обработке данных | `senior-data-engineer/` | Пайплайны, ETL, качество данных |
| Старший инженер ML | `senior-ml-engineer/` | Развертывание моделей, MLOps, интеграция с LLM |
| Старший инженер по промпту | `senior-prompt-engineer/` | Промпт-оптимизация, RAG, агенты |
| Старший специалист по компьютерному зрению | `senior-computer-vision/` | Обнаружение объектов, сегментация |

### Специализированные инструменты (5 скилл) { #specialized-tools-5-skills }

| Скилл | Папка | Сосредоточься |
|-------|--------|-------|
| Профессиональный драматург | `playwright-pro/` | Тестирование E2E (9 подпрограмм по скиллам) |
| Самосовершенствующийся агент | `self-improving-agent/` | Управление памятью (5 вспомогательных скиллы) |
| Интеграция с полосой | `stripe-integration-expert/` | Интеграция платежей, веб-хуки |
| Командир по инциденту | `incident-commander/` | Воркфлоу по реагированию на инциденты |
| Создатель шаблонов электронной почты | `email-template-builder/` | Генерация электронной почты в HTML-формате |

## Инструменты Python { #python-tools }

Более 30 скриптов, все только для stdlib. Запуск напрямую:

```bash
python3 <skill>/scripts/<tool>.py --help
```

Установка pip не требуется. Скрипты включают встроенные образцы для демонстрационного режима.

## Правила { #rules }

- Загружайте только определенный скилл SKILL.md вам нужно — не загружайте массово все 32
- Используйте инструменты Python для анализа и построения каркасов, а не для ручного суждения
- Проверьте CLAUDE.md для получения примеров использования инструментов и воркфлоу
