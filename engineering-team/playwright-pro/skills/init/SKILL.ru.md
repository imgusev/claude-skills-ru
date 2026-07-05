---
name: "init"
description: >-
  Set up Playwright in a project. Use when user says "set up playwright",
  "add e2e tests", "configure playwright", "testing setup", "init playwright",
  or "add test infrastructure".
---

# Инициализировать проект драматурга { #initialize-playwright-project }

Создайте готовую к производству среду тестирования драматурга. Определите фреймворк, сгенерируйте конфигурацию, структуру папок, пример теста и воркфлоу CI.

## Шаги { #steps }

### 1. Проанализируйте проект { #1-analyze-the-project }

Используйте `Explore` субагент для сканирования проекта:

- Проверьте `package.json` для фреймворка (React, Next.js , Vue, Угловатая, Стройная)
- Проверьте наличие `tsconfig.json` → используйте TypeScript; в противном случае JavaScript
- Проверьте, установлен ли уже драматург (`@playwright/test` в зависимостях)
- Проверьте наличие существующих каталогов тестов (`tests/`, `e2e/`, `__tests__/`)
- Проверьте наличие существующей конфигурации CI (`.github/workflows/`, `.gitlab-ci.yml`)

### 2. Установите драматурга { #2-install-playwright }

Если он еще не установлен:

```bash
npm init playwright@latest -- --quiet
```

Или если пользователь предпочитает ручную настройку:

```bash
npm install -D @playwright/test
npx playwright install --with-deps chromium
```

### 3. Генерируйте `playwright.config.ts` { #3-generate-playwrightconfigts }

Адаптироваться к обнаруженному фреймворку:

**Next.js:**
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: "chromium", use: { ...devices['Desktop Chrome'] } },
    { name: "firefox", use: { ...devices['Desktop Firefox'] } },
    { name: "webkit", use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

**Реагировать (Vite):**
- Изменение `baseURL` к `http://localhost:5173`
- Изменение `webServer.command` к `npm run dev`

**Vue/Nuxt:**
- Изменение `baseURL` к `http://localhost:3000`
- Изменение `webServer.command` к `npm run dev`

**Угловой:**
- Изменение `baseURL` к `http://localhost:4200`
- Изменение `webServer.command` к `npm run start`

**Не обнаружен фреймворк:**
- Опустить `webServer` блокировать
- Набор `baseURL` из пользовательского ввода или оставить в качестве заполнителя

### 4. Создайте структуру папок { #4-create-folder-structure }

```
e2e/
├── fixtures/
│   └── index.ts          # Custom fixtures
├── pages/
│   └── .gitkeep          # Page object models
├── test-data/
│   └── .gitkeep          # Test data files
└── example.spec.ts       # First example test
```

### 5. Сгенерируйте пример теста { #5-generate-example-test }

```typescript
import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should load successfully', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/.+/);
  });

  test('should have visible navigation', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('navigation')).toBeVisible();
  });
});
```

### 6. Сгенерируйте CI-воркфлоу { #6-generate-ci-workflow }

Если `.github/workflows/` существует, создает `playwright.yml`:

```yaml
name: "playwright-tests"

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: lts/*
      - name: "install-dependencies"
        run: npm ci
      - name: "install-playwright-browsers"
        run: npx playwright install --with-deps
      - name: "run-playwright-tests"
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: "playwright-report"
          path: playwright-report/
          retention-days: 30
```

Если `.gitlab-ci.yml` существует, добавьте вместо этого сцену драматурга.

### 7. Обновление `.gitignore` { #7-update-gitignore }

Добавить, если его еще нет:

```
/test-results/
/playwright-report/
/blob-report/
/playwright/.cache/
```

### 8. Добавьте скрипты npm { #8-add-npm-scripts }

Добавить к `package.json` сценарии:

```json
{
  "test:e2e": "playwright test",
  "test:e2e:ui": "playwright test --ui",
  "test:e2e:debug": "playwright test --debug"
}
```

### 9. Проверьте настройку { #9-verify-setup }

Запустите пример теста:

```bash
npx playwright test
```

Сообщите о результате. Если это не удается, проведите диагностику и устраните неполадки перед завершением.

## Выход { #output }

Подтвердите, что было создано:
- Путь к конфигурационному файлу и ключевые настройки
- Тестовый каталог и пример теста
- Воркфлоу CI (если применимо)
- добавлены скрипты npm
- Как запустить: `npx playwright test` или `npm run test:e2e`
