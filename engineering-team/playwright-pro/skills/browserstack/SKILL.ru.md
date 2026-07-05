---
name: "browserstack"
description: >-
  Run tests on BrowserStack. Use when user mentions "browserstack",
  "cross-browser", "cloud testing", "browser matrix", "test on safari",
  "test on firefox", or "browser compatibility".
---

# Интеграция с BrowserStack { #browserstack-integration }

Запустите тесты драматурга в облачной сетке BrowserStack для кроссбраузерного тестирования и тестирования на разных устройствах.

## Предварительные условия { #prerequisites }

Должны быть установлены переменные окружения:
- `BROWSERSTACK_USERNAME` — ваше имя пользователя BrowserStack
- `BROWSERSTACK_ACCESS_KEY` — ваш ключ доступа

Если не задано, сообщите пользователю, как получить их из [browserstack.com/accounts/settings](https://www.browserstack.com/accounts/settings) и остановись.

## Возможности { #capabilities }

### 1. Настройка для BrowserStack { #1-configure-for-browserstack }

```
/pw:browserstack setup
```

Шаги:
1. Проверьте ток `playwright.config.ts`
2. Добавить параметры подключения к BrowserStack:

```typescript
// Add to playwright.config.ts
import { defineConfig } from '@playwright/test';

const isBS = !!process.env.BROWSERSTACK_USERNAME;

export default defineConfig({
  // ... existing config
  projects: isBS ? [
    {
      name: "chromelatestwindows-11",
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(JSON.stringify({
            'browser': 'chrome',
            'browser_version': 'latest',
            'os': 'Windows',
            'os_version': '11',
            'browserstack.username': process.env.BROWSERSTACK_USERNAME,
            'browserstack.accessKey': process.env.BROWSERSTACK_ACCESS_KEY,
          }))}`,
        },
      },
    },
    {
      name: "firefoxlatestwindows-11",
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(JSON.stringify({
            'browser': 'playwright-firefox',
            'browser_version': 'latest',
            'os': 'Windows',
            'os_version': '11',
            'browserstack.username': process.env.BROWSERSTACK_USERNAME,
            'browserstack.accessKey': process.env.BROWSERSTACK_ACCESS_KEY,
          }))}`,
        },
      },
    },
    {
      name: "webkitlatestos-x-ventura",
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(JSON.stringify({
            'browser': 'playwright-webkit',
            'browser_version': 'latest',
            'os': 'OS X',
            'os_version': 'Ventura',
            'browserstack.username': process.env.BROWSERSTACK_USERNAME,
            'browserstack.accessKey': process.env.BROWSERSTACK_ACCESS_KEY,
          }))}`,
        },
      },
    },
  ] : [
    // ... local projects fallback
  ],
});
```

3. Добавить скрипт npm: `"test:e2e:cloud": "npx playwright test --project='chrome@*' --project='firefox@*' --project='webkit@*'"`

### 2. Запустите тесты в BrowserStack { #2-run-tests-on-browserstack }

```
/pw:browserstack run
```

Шаги:
1. Проверьте, установлены ли учетные данные
2. Запускайте тесты с проектами BrowserStack:
   ```bash
   BROWSERSTACK_USERNAME=$BROWSERSTACK_USERNAME \
   BROWSERSTACK_ACCESS_KEY=$BROWSERSTACK_ACCESS_KEY \
   npx playwright test --project='chrome@*' --project='firefox@*'
   ```
3. Контролировать выполнение
4. Отчет о результатах для каждого браузера

### 3. Получите результаты сборки { #3-get-build-results }

```
/pw:browserstack results
```

Шаги:
1. Вызов `browserstack_get_builds` Инструмент MCP
2. Получите сеансы последней сборки
3. Для каждого сеанса:
   - Статус (пройден/сбой)
   - Браузер и операционная система
   - Продолжительность
   - URL-АДРЕС видео
   - URL-адреса журналов
4. Формат в виде сводной таблицы

### 4. Проверьте доступные браузеры { #4-check-available-browsers }

```
/pw:browserstack browsers
```

Шаги:
1. Вызов `browserstack_get_browsers` Инструмент MCP
2. Фильтр для браузеров, совместимых с драматургом
3. Отображать доступные комбинации браузера и операционной системы

### 5. Локальное тестирование { #5-local-testing }

```
/pw:browserstack local
```

Для тестирования локального хостинга или промежуточной установки за брандмауэром:
1. Установите BrowserStack локально: `npm install -D browserstack-local`
2. Добавьте локальный туннель в конфигурацию
3. Предоставьте инструкции по настройке

## Используемые инструменты MCP { #mcp-tools-used }

| Инструмент | Когда |
|---|---|
| `browserstack_get_plan` | Проверьте лимиты по счету |
| `browserstack_get_browsers` | Список доступных браузеров |
| `browserstack_get_builds` | Список последних сборок |
| `browserstack_get_sessions` | Получать сеансы в сборке |
| `browserstack_get_session` | Получить подробную информацию о сеансе (видео, журналы) |
| `browserstack_update_session` | Отметьте прохождение/неудачу |
| `browserstack_get_logs` | Получать текстовые/сетевые журналы |

## Выход { #output }

- Таблица результатов кроссбраузерного тестирования
- Статус прохождения/сбоя для каждого браузера
- Ссылки на дашборд BrowserStack для получения видео/скриншотов
- Выделены любые сбои, связанные с конкретным браузером
