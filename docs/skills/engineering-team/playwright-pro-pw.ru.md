---
title: "Профессиональный драматург { #playwright-pro } — Агентский скилл и плагин Codex"
description: "Набор инструментов для тестирования драматурга производственного уровня. Используйте, когда пользователь упоминает тесты драматурга, сквозное. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Профессиональный драматург { #playwright-pro }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `pw`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/playwright-pro/skills/pw/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Производственный набор инструментов для тестирования драматурга для агентов по кодированию искусственного интеллекта.

## Доступные команды { #available-commands }

При установке в качестве плагина Claude Code они доступны в виде `/pw:` команды:

| Команда | Что он делает |
|---|---|
| `/pw:init` | Настройка драматурга — обнаруживает фреймворк, генерирует конфигурацию, CI, первый тест |
| `/pw:generate <spec>` | Генерируйте тесты из пользовательской истории, URL-адреса или компонента |
| `/pw:review` | Ревью-тесты на наличие антишаблонов и пробелов в покрытии |
| `/pw:fix <test>` | Диагностируйте и устраняйте неудачные или неаккуратные тесты |
| `/pw:migrate` | Перейти с Cypress или Selenium на Druggy |
| `/pw:coverage` | Проанализируйте, что протестировано по сравнению с другими чего не хватает |
| `/pw:testrail` | Синхронизация с TestRail — считывание обращений, отправка результатов |
| `/pw:browserstack` | Запускайте в BrowserStack, извлекайте кроссбраузерные отчеты |
| `/pw:report` | Сгенерируйте отчет о тестировании в предпочитаемом вами формате |

## Быстрый запуск воркфлоу { #quick-start-workflow }

Рекомендуемая последовательность для большинства проектов:

```
1. /pw:init          → scaffolds config, CI pipeline, and a first smoke test
2. /pw:generate      → generates tests from your spec or URL
3. /pw:review        → validates quality and flags anti-patterns      ← always run after generate
4. /pw:fix <test>    → diagnoses and repairs any failing/flaky tests  ← run when CI turns red
```

**Контрольные точки проверки:**
- После `/pw:generate` — всегда беги `/pw:review` перед фиксацией; он автоматически перехватывает анти-шаблоны локатора и пропущенные утверждения.
- После `/pw:fix` — повторно запустите полный пакет локально (`npx playwright test`) чтобы подтвердить, что исправление не приводит к регрессиям.
- После `/pw:migrate` — беги `/pw:coverage` чтобы подтвердить паритет со старым набором перед выводом из эксплуатации тестов Cypress/Selenium.

### Пример: Сгенерировать → Ревью → Исправить { #example-generate--review--fix }

```bash
# 1. Generate tests from a user story
/pw:generate "As a user I can log in with email and password"

# Generated: tests/auth/login.spec.ts
# → Playwright Pro creates the file using the auth template.

# 2. Review the generated tests
/pw:review tests/auth/login.spec.ts

# → Flags: one test used page.locator('input[type=password]') — suggests getByLabel('Password')
# → Fix applied automatically.

# 3. Run locally to confirm
npx playwright test tests/auth/login.spec.ts --headed

# 4. If a test is flaky in CI, diagnose it
/pw:fix tests/auth/login.spec.ts
# → Identifies missing web-first assertion; replaces waitForTimeout(2000) with expect(locator).toBeVisible()
```

## Золотые правила { #golden-rules }

1. `getByRole()` поверх CSS/XPath — устойчивость к изменениям разметки
2. Никогда `page.waitForTimeout()` — используйте веб-первые утверждения
3. `expect(locator)` автоматические повторные попытки; `expect(await locator.textContent())` не делает
4. Изолируйте каждый тест — нет общего состояния между тестами
5. `baseURL` в конфигурации — ноль жестко закодированных URL-адресов
6. Повторные попытки: `2` в КИ, `0` локально
7. Следы: `'on-first-retry'` — расширенная отладка без замедления
8. Привязки к глобальным сетям — `test.extend()` для общего состояния
9. Одно поведение для каждого теста — несколько связанных утверждений в порядке вещей
10. Имитируйте только внешние сервисы — никогда не имитируйте свое собственное приложение

## Приоритет локатора { #locator-priority }

```
1. getByRole()        — buttons, links, headings, form elements
2. getByLabel()       — form fields with labels
3. getByText()        — non-interactive text
4. getByPlaceholder() — inputs with placeholder
5. getByTestId()      — when no semantic option exists
6. page.locator()     — CSS/XPath as last resort
```

## Что входит в комплект { #whats-included }

- ** 9 скилл** с подробными пошаговыми инструкциями
- **3 специализированных агента**: разработчик тестов, отладчик тестов, планировщик миграции
- ** 55 тестовых шаблонов**: авторизация, CRUD, оформление заказа, поиск, формы, дашборд, настройки, онбординг, уведомления, API, специальные возможности
- **2 сервера MCP** (TypeScript): интеграция TestRail и BrowserStack
- ** Интеллектуальные перехватчики**: автоматическая проверка качества теста, автоматическое определение проектов драматурга
- ** 6 справочных материалов**: золотые правила, локаторы, утверждения, приспособления, подводные камни, сложные тесты
- **Руководства по миграции**: Таблицы сопоставления Cypress и Selenium

## Настройка интеграции { #integration-setup }

### Испытательный поручень (опционально) { #testrail-optional }
```bash
export TESTRAIL_URL="https://your-instance.testrail.io"
export TESTRAIL_USER="your@email.com"
export TESTRAIL_API_KEY="your-api-key"
```

### BrowserStack (необязательно) { #browserstack-optional }
```bash
export BROWSERSTACK_USERNAME="your-username"
export BROWSERSTACK_ACCESS_KEY="your-access-key"
```

## Краткий справочник { #quick-reference }

Видишь `reference/` каталог для:
- `golden-rules.md` — 10 правил, не подлежащих обсуждению
- `locators.md` — Полный приоритет локатора со шпаргалкой
- `assertions.md` — Ссылка на веб-первые утверждения
- `fixtures.md` — Пользовательские приспособления и шаблоны состояния хранилища
- `common-pitfalls.md` — Топ-10 ошибок и исправлений
- `flaky-tests.md` — Команды диагностики и быстрые исправления

Видишь `templates/README.md` для получения полного индекса шаблона.
