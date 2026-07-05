---
title: "Скиллы для управления проектами — Router { #project-management-skills--router } — Агентский скилл для управления проектами"
description: "Маршрутизатор/ индекс для 8 скилл по управлению проектами, включенных в этот плагин (senior PM quant toolkit, scrum master, Jira/JQL, Confluence. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Скиллы для управления проектами — Router { #project-management-skills--router }

<div class="page-meta" markdown>
<span class="meta-badge">:material-clipboard-check-outline: Управление проектами</span>
<span class="meta-badge">:material-identifier: `pm-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/project-management/skills/pm-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install pm-skills</code>
</div>


Этот плагин объединяет ** скиллы 8 PM** (этот маршрутизатор находится в 9-й папке под `project-management/skills/`). Каждый скилл является самодостаточным. Связанный `.mcp.json` подключает пульт дистанционного управления Atlassian MCP (`https://mcp.atlassian.com/v1/sse`, OAuth обрабатывается кодом Claude).

## Таблица маршрутизации { #routing-table }

Сопоставьте запрос, затем загрузите `project-management/skills/<skill>/SKILL.md`. Если несколько строк совпадают, сначала задайте один уточняющий вопрос.

| Сигналы запроса | Скилл | Путь |
|---|---|---|
| Работоспособность проекта, EMV риска, трехбалльная оценка | старший-премьер-министр | `skills/senior-pm/` |
| Скорость спринта, ретро-анализ, здоровье церемонии | scrum-мастер | `skills/scrum-master/` |
| Запросы JQL, воркфлоу Jira, доски объявлений | jira-эксперт | `skills/jira-expert/` |
| Пространства слияния, структура страницы, аудит контента | слияние-эксперт | `skills/confluence-expert/` |
| Администрирование пользователя/разрешений/схемы | atlassian-администратор | `skills/atlassian-admin/` |
| Многоразовые шаблоны Confluence/Jira | atlassian-шаблоны | `skills/atlassian-templates/` |
| Стенограммы заседаний, время разговора, пункты о действиях | встреча-анализатор | `skills/meeting-analyzer/` |
| Обновления статуса, обновления 3P, связь с стейкхолдерами | командные коммуникации | `skills/team-communications/` |

## Быстрый старт { #quick-start }

```bash
# Example: route a sprint-health request
cat project-management/skills/scrum-master/SKILL.md
ls project-management/skills/scrum-master/scripts/
```

## Правила { #rules }

- Текущие операции Jira/Confluence выполняются через Atlassian Remote MCP (названия инструментов camelCase, такие как `createJiraIssue`, `searchJiraIssuesUsingJql`, `createConfluencePage` — канонический список в `project-management/references/atlassian-mcp-tools.md`). Операции администратора НЕ подпадают под действие MCP — use admin.atlassian.com или REST API для каждого atlassian-администратора.
- Перейдите точно к одному скиллу, затем следуйте воркфлоу этого скилла. Этот маршрутизатор не поставляет никаких собственных инструментов.
