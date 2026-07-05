---
title: "Cursor Agent Skills & Rules Guide (2026)"
description: "Установите и используйте скиллы 345 агента с Cursor IDE. Инженерные, маркетинговые и продуктовые плагины для агента по кодированию искусственного интеллекта Cursor."
---

# Руководство по скиллам курсора для агента { #cursor-agent-skills-guide }

Используйте скиллы агента 345, готовые к работе, с Cursor IDE. Каждый скилл преобразуется в формат правил курсора и устанавливается с помощью `.cursor/skills/` каталог.

---

## Быстрая установка { #quick-install }

```bash
# Clone the repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Convert all skills to Cursor format
./scripts/convert.sh --all --tool cursor

# Or convert individual skills
./scripts/convert.sh --skill frontend-design --tool cursor
./scripts/convert.sh --skill pr-review-expert --tool cursor
```

### Как это работает { #how-it-works }

Курсор считывает правила агента из `.cursor/rules/` и `.cursorrules` файлы. Сценарий преобразования преобразует SKILL.md файлы преобразуются в наборы правил, совместимые с курсором, с сохранением воркфлоу, фреймворков принятия решений и знаний о предметной области.

---

## Лучшие скиллы для пользователей Cursor { #top-skills-for-cursor-users }

| Скилл | Что он делает | Лучше всего подходит для |
|-------|-------------|----------|
| **интерфейс-дизайн** | Пользовательский интерфейс производственного уровня с React, Tailwind, shadcn/ui. | Создание отточенных интерфейсов |
| **pr-ревью-эксперт** | Многоходовой ревью кода, выявляющий пробелы в логике, безопасности и тестировании. | Качество кода |
| **старший-полный комплект** | Шаблоны полного стека: разработка API, аутентификация, управление состоянием. | Архитектура приложения |
| **tdd-руководство** | Разработка на основе тестирования с красно-зеленым рефакторингом. | Сначала пишем тесты |
| **создатель контента** | SEO-оптимизированный контент с фреймворками brand voice. | Маркетинговый контент |
| **agile-владелец продукта** | Истории пользователей, критерии приемлемости, планирование спринта. | Работа с продуктом |
| **технический директор-консультант** | Анализ технического долга, масштабирование команды, архитектурные решения. | Техническое лидерство |
| **разработчик баз данных** | Разработка схемы, миграция, индексация, оптимизация запросов. | Работа с базой данных |

---

## Интеграция, зависящая от курсора { #cursor-specific-integration }

### Использование с субагентами курсора { #using-with-cursors-subagents }

Многомодельная субагентская система Cursor хорошо работает с скиллами:

```
# In Cursor's Composer, reference a skill:
@skill frontend-design Build a dashboard with charts and data tables

# Or use slash commands from the skill:
/design:component Create a pricing card with toggle for monthly/annual
```

### Правила проекта { #project-rules }

Добавляйте скиллы к своим `.cursorrules` для обеспечения доступности в рамках всего проекта:

```bash
# Append skill instructions to cursor rules
cat .cursor/skills/frontend-design/SKILL.md >> .cursorrules
```

---

## Полный каталог { #full-catalog }

Все 345 скилл в 17 областях. Увидеть [полное ПРОЧТЕНИЕ](https://github.com/alirezarezvani/claude-skills) для получения полного списка.

** Также работает с: ** Кодом Клода · OpenAI Codex · Gemini CLI · OpenClaw · Aider · Виндсерфинг · Kilo Code · OpenCode · Дополнение · Антигравитация

---

* Последнее обновление: март 2026 · [алирезарезвани/Клод-скиллы](https://github.com/alirezarezvani/claude-skills)*
