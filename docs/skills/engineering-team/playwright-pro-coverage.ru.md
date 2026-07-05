---
title: "Анализ пробелов в тестовом покрытии { #analyze-test-coverage-gaps } — Агентский скилл и плагин Codex"
description: "Analyze test coverage gaps. Use when user says 'test coverage', 'what's not tested', 'coverage gaps', 'missing tests', 'coverage report', or 'what. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Анализ пробелов в тестовом покрытии { #analyze-test-coverage-gaps }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `coverage`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/playwright-pro/skills/coverage/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Сопоставьте все тестируемые поверхности в приложении и определите, что тестируется по сравнению с другими поверхностями. чего не хватает.

## Шаги { #steps }

### 1. Поверхность нанесения карты { #1-map-application-surface }

Используйте `Explore` субагент для каталогизации:

**Маршруты/страницы:**
- Сканирование определений маршрутов (Next.js `app/`, Конфигурация маршрутизатора React, маршрутизатор Vue и т.д.)
- Перечислите все пользовательские страницы с указанием их путей

**Компоненты:**
- Определите интерактивные компоненты (формы, модалы, выпадающие списки, таблицы).
- Обратите внимание на компоненты со сложной логикой состояния

**Конечные точки API:**
- Сканировать файлы маршрутов API или серверные контроллеры
- Перечислите все конечные точки с указанием их методов

**Потоки пользователей:**
- Определите критические пути: авторизация, оформление заказа, онбординг, основные функции
- Сопоставьте многоэтапные воркфлоу

### 2. Сопоставьте существующие тесты { #2-map-existing-tests }

Сканировать все `*.spec.ts` / `*.spec.js` файлы:

- Извлеките, какие страницы/маршруты охвачены (по `page.goto()` звонки)
- Извлеките, какие компоненты тестируются (с помощью локатора)
- Извлеките, какие конечные точки API подвергаются издевательствам или попаданию
- Подсчитайте количество тестов в каждой области

### 3. Сгенерируйте матрицу покрытия { #3-generate-coverage-matrix }

```
## Coverage Matrix

| Area | Route | Tests | Status |
|---|---|---|---|
| Auth | /login | 5 | ✅ Covered |
| Auth | /register | 0 | ❌ Missing |
| Auth | /forgot-password | 0 | ❌ Missing |
| Dashboard | /dashboard | 3 | ⚠️ Partial (no error states) |
| Settings | /settings | 0 | ❌ Missing |
| Checkout | /checkout | 8 | ✅ Covered |
```

### 4. Расставьте приоритеты по пробелам { #4-prioritize-gaps }

Ранжируйте непокрытые области по влиянию на бизнес:

1. ** Критично ** — авторизация, оплата, основные функции → сначала протестируйте
2. ** Высокий уровень ** — ориентированный на пользователя CRUD, поиск, навигация
3. **Средний** — настройки, предпочтения, крайние варианты
4. **Низкий** — статические страницы, информация, термины

### 5. Предложите план тестирования { #5-suggest-test-plan }

Для каждого пробела рекомендуется:
- Количество необходимых тестов
- Какой шаблон из `templates/` для использования
- Предполагаемое усилие (быстрое/среднее/сложное)

```
## Recommended Test Plan

### Priority 1: Critical
1. /register (4 tests) — use auth/registration template — quick
2. /forgot-password (3 tests) — use auth/password-reset template — quick

### Priority 2: High
3. /settings (4 tests) — use settings/ templates — medium
4. Dashboard error states (2 tests) — use dashboard/data-loading template — quick
```

### 6. Автоматическое генерирование (необязательно) { #6-auto-generate-optional }

Спросите пользователя: "Сгенерировать тесты для верхних N пробелов? [Да/Нет/Выберите конкретный вариант]"

Если да, вызовите `/pw:generate` для каждого пробела используйте рекомендуемый шаблон.

## Выход { #output }

- Матрица покрытия (формат таблицы)
- Оценка процентного охвата
- Список приоритетных пробелов с оценкой усилий
- Возможность автоматической генерации пропущенных тестов
