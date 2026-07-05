---
name: "migrate"
description: >-
  Migrate from Cypress or Selenium to Playwright. Use when user mentions
  "cypress", "selenium", "migrate tests", "convert tests", "switch to
  playwright", "move from cypress", or "replace selenium".
---

# Перейти к драматургу { #migrate-to-playwright }

Интерактивный переход с Cypress или Selenium на Druggy с преобразованием файла за файлом.

## Входной сигнал { #input }

`$ARGUMENTS` может быть:
- `"from cypress"` — перенести набор тестов Cypress
- `"from selenium"` — перенести тесты Selenium/WebDriver
- Путь к файлу: преобразуйте определенный тестовый файл
- Пусто: автоматическое определение исходного фреймворка

## Шаги { #steps }

### 1. Определите исходный фреймворк { #1-detect-source-framework }

Использование `Explore` субагент для сканирования:
- `cypress/` каталог или `cypress.config.ts` → Кипарис
- `selenium`, `webdriver` в `package.json` deps → Селен
- `.py` тестовые файлы с `selenium` импорт → Selenium (Python)

### 2. Оцените масштабы миграции { #2-assess-migration-scope }

Подсчитывайте файлы и классифицируйте их по категориям:

```
Migration Assessment:
- Total test files: X
- Cypress custom commands: Y
- Cypress fixtures: Z
- Estimated effort: [small|medium|large]
```

| Размер | Файлы | Подход |
|---|---|---|
| Маленький (1-10) | Преобразовывать последовательно | Прямое преобразование |
| Средний (11-30) | Разделите на группы по 5 штук | Используйте саб-агентов |
| Большой (31+) | Использование `/batch` | Параллельное преобразование с `/batch` |

### 3. Установите драматурга (если он отсутствует) { #3-set-up-playwright-if-not-present }

Бежать `/pw:init` сначала, если драматург не настроен.

### 4. Конвертируйте файлы { #4-convert-files }

Для каждого файла примените соответствующее сопоставление:

#### Кипарис → Драматург { #cypress--playwright }

Нагрузка `cypress-mapping.md` для полной справки.

Ключевые переводы:
```
cy.visit(url)           → page.goto(url)
cy.get(selector)        → page.locator(selector) or page.getByRole(...)
cy.contains(text)       → page.getByText(text)
cy.find(selector)       → locator.locator(selector)
cy.click()              → locator.click()
cy.type(text)           → locator.fill(text)
cy.should('be.visible') → expect(locator).toBeVisible()
cy.should('have.text')  → expect(locator).toHaveText(text)
cy.intercept()          → page.route()
cy.wait('@alias')       → page.waitForResponse()
cy.fixture()            → JSON import or test data file
```

**Пользовательские команды Cypress** → Приспособления для драматурга или вспомогательные функции
**Плагины Cypress** → Конфигурация драматурга или приспособления
**`before`/`beforeEach`** → `test.beforeAll()` / `test.beforeEach()`

#### Селен → Драматург { #selenium--playwright }

Нагрузка `selenium-mapping.md` для полной справки.

Ключевые переводы:
```
driver.get(url)                    → page.goto(url)
driver.findElement(By.id('x'))     → page.locator('#x') or page.getByTestId('x')
driver.findElement(By.css('.x'))   → page.locator('.x') or page.getByRole(...)
element.click()                    → locator.click()
element.sendKeys(text)             → locator.fill(text)
element.getText()                  → locator.textContent()
WebDriverWait + ExpectedConditions → expect(locator).toBeVisible()
driver.switchTo().frame()          → page.frameLocator()
Actions                            → locator.hover(), locator.dragTo()
```

### 5. Обновите локаторы { #5-upgrade-locators }

Во время преобразования обновите селекторы в соответствии с рекомендациями драматурга:
- `#id` → `getByTestId()` или `getByRole()`
- `.class` → `getByRole()` или `getByText()`
- `[data-testid]` → `getByTestId()`
- XPath → локаторы на основе ролей

### 6. Преобразуйте пользовательские команды / утилиты { #6-convert-custom-commands--utilities }

- Пользовательские команды Cypress → пользовательские приспособления драматурга с помощью `test.extend()`
- Объекты страницы Selenium → объекты страницы драматурга (сохранить структуру, обновить API)
- Общие помощники → служебные функции TypeScript

### 7. Проверьте каждый преобразованный файл { #7-verify-each-converted-file }

После преобразования каждого файла:

```bash
npx playwright test <converted-file> --reporter=list
```

Исправьте все ошибки компиляции или времени выполнения, прежде чем переходить к следующему файлу.

### 8. Наведите порядок { #8-clean-up }

После того, как все файлы будут преобразованы:
- Удалите зависимости Cypress/Selenium из `package.json`
- Удалите старые конфигурационные файлы (`cypress.config.ts` и т.д.)
- Обновите воркфлоу CI для использования драматурга
- Обновите README новыми тестовыми командами

Спросите пользователя, прежде чем что-либо удалять.

## Выход { #output }

- Сводка по преобразованию: файлы преобразованы, все тесты перенесены
- Любые тесты, которые не удалось преобразовать автоматически (требуется ручное вмешательство)
- Обновленная конфигурация CI
- Сравнение результатов тестового запуска до/после
