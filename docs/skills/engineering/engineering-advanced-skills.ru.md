---
title: "Продвинутые инженерные скиллы (МОЩНЫЙ уровень) { #engineering-advanced-skills-powerful-tier } — Агентский скилл для Codex и OpenClaw"
description: "Список из 37 скилл продвинутых инженерных агентов для Claude Code, Codex, Gemini CLI, Cursor, OpenClaw. Используйте при просмотре или выборе среди."
---

# Продвинутые инженерные скиллы (МОЩНЫЙ уровень) { #engineering-advanced-skills-powerful-tier }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `engineering-advanced-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/engineering-advanced-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


37 продвинутых инженерных скилл для сложной архитектуры, автоматизации, надежности и работы на платформе.

## Быстрый старт { #quick-start }

### Код Клода { #claude-code }
```
/read engineering/skills/agent-designer/SKILL.md
```

### Codex CLI { #codex-cli }
```bash
npx agent-skills-cli add imgusev/claude-skills-ru/engineering
```

## Обзор скиллы { #skills-overview }

| Скилл | Папка | Сосредоточься |
|-------|--------|-------|
| Дизайнер-агент | `agent-designer/` | Архитектура с несколькими агентами: планирование, создание схемы, оценка |
| Дизайнер воркфлоу агента | `agent-workflow-designer/` | Каркасы оркестрации воркфлоу |
| Рецензент дизайна API | `api-design-reviewer/` | Компоновка REST/GraphQL, критические изменения |
| Разработчик набора тестов API | `api-test-suite-builder/` | Генерация теста API |
| Автоматизация браузера | `browser-automation/` | Шаблоны автоматизации драматурга/Selenium |
| Генератор списка изменений | `changelog-generator/` | Списки изменений, семантические сбои в версиях, исправление/rollback дисциплина |
| Инженерия хаоса | `chaos-engineering/` | Схема эксперимента, радиус взрыва, вскрытия |
| Конструктор пайплайнов CI/CD | `ci-cd-pipeline-builder/` | Генерация пайплайна |
| Онбординг кодовой базы | `codebase-onboarding/` | Новые руководства по онбордингу для разработчиков |
| Разработчик базы данных | `database-designer/` | Анализ схем, оптимизация индексов, миграции |
| Разработчик схемы базы данных | `database-schema-designer/` | ERD, нормализация |
| Аудитор зависимостей | `dependency-auditor/` | Проверка безопасности зависимостей |
| Менеджер секретов Env | `env-secrets-manager/` | Ротация секретов, хранилище |
| Архитектор фич-флагов | `feature-flags-architect/` | Отмечать задолженность, планы раскатки, kill Switch |
| Сфокусированное исправление | `focused-fix/` | Систематический признак/module ремонт |
| Скриншот всей страницы | `full-page-screenshot/` | Инструмент для захвата всей страницы |
| Менеджер рабочего дерева Git | `git-worktree-manager/` | Параллельная ветвь воркфлоу |
| Разработчик системы собеседований | `interview-system-designer/` | Проектирование пайплайна по найму |
| Оператор Kubernetes | `kubernetes-operator/` | Проверка CRD, согласование прокладок |
| Конструктор MCP-серверов | `mcp-server-builder/` | Создание инструмента MCP |
| Архитектор миграции | `migration-architect/` | Планирование миграции системы |
| Навигатор Monorepo | `monorepo-navigator/` | Инструмент для монорепо |
| Дизайнер наблюдаемости | `observability-designer/` | Дашборд, шум оповещения (SLOs → slo-архитектор) |
| Профилировщик производительности | `performance-profiler/` | Процессор, память, профилирование нагрузки |
| Эксперт по ревью в области PR | `pr-review-expert/` | Анализ запроса на извлечение |
| ТРЯПИЧНЫЙ архитектор | `rag-architect/` | Дизайн тряпки, разбивка на части, оценка поиска |
| Генератор рансбуков | `runbook-generator/` | Операционные рансбуки |
| Менеджер хранилища секретов | `secrets-vault-manager/` | Узоры сводов, HCL |
| Самооценка | `self-eval/` | Честная работа - оценка качества |
| Корабельные гейты | `ship-gate/` | Аудит перед производством (89 проверок) |
| Скилл аудитора безопасности | `skill-security-auditor/` | Сканирование уязвимостей с помощью скилла |
| Тестировщик скилла | `skill-tester/` | Оценка качества скилла |
| Архитектор SLO | `slo-architect/` | Проектирование SLO/SLI, бюджеты ошибок, оповещения о скорости выгорания |
| Управляемый спецификациями воркфлоу | `spec-driven-workflow/` | Спецификация-первые гейты для разработки |
| Помощник по работе с базой данных SQL | `sql-database-assistant/` | Оптимизация запросов, 4 диалекта |
| Трекер TC | `tc-tracker/` | Жизненный цикл контекста задачи + хэндоффы |
| Технический отслеживатель долгов | `tech-debt-tracker/` | Проверка задолженности → определение приоритетов → Дашборд |

Примечание: управление выпусками объединено в `changelog-generator/` (бампер версии + исправление/rollback процедуры сейчас живут там).

## Правила { #rules }

- Загружайте только определенный скилл SKILL.md вам нужно
- Это продвинутые скиллы — при необходимости сочетайте с инженерными командными/ основными скиллами
