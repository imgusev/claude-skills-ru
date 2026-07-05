---
name: "senior-qa"
description: Генерирует модульные тесты, интеграционные тесты и E2E-тесты для React/Next.js приложения. Сканирует компоненты для создания тестовых заготовок библиотеки тестирования Jest + React, анализирует отчеты о покрытии Istanbul/LCOV на наличие пробелов в поверхности, использует тестовые файлы scaffolds Драматурга из Next.js маршрутизирует, имитирует вызовы API с помощью MSW, создает тестовые приложения и настраивает средства выполнения тестов. Используйте, когда пользователь просит "сгенерировать тесты", "написать модульные тесты", "проанализировать тестовое покрытие", "скаффолд E2E-тестов", "настроить драматург", "настроить Jest", "внедрить шаблоны тестирования" или "улучшить качество тестирования".
---

# Старший инженер по контролю качества { #senior-qa-engineer }

Автоматизация тестирования, анализ покрытия и шаблоны обеспечения качества для React и Next.js приложения.

---

## Быстрый старт { #quick-start }

```bash
# Generate Jest test stubs for React components
python scripts/test_suite_generator.py src/components/ --output __tests__/

# Analyze test coverage from Jest/Istanbul reports
python scripts/coverage_analyzer.py coverage/coverage-final.json --threshold 80

# Scaffold Playwright E2E tests for Next.js routes
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/
```

---

## Обзор инструментов { #tools-overview }

### 1. Генератор набора тестов { #1-test-suite-generator }

Сканирует компоненты React/TypeScript и генерирует тестовые заглушки библиотеки тестирования Jest + React с надлежащей структурой.

**Входные данные:** Исходный каталог, содержащий компоненты React
** Выходные данные:** Тестовые файлы с блоками описания, тестами рендеринга, тестами взаимодействия

**Использование:**
```bash
# Basic usage - scan components and generate tests
python scripts/test_suite_generator.py src/components/ --output __tests__/

# Include accessibility tests
python scripts/test_suite_generator.py src/ --output __tests__/ --include-a11y

# Generate with custom template
python scripts/test_suite_generator.py src/ --template custom-template.tsx
```

**Поддерживаемые шаблоны:**
- Функциональные компоненты с крючками
- Компоненты с поставщиками контекста
- Компоненты с выборкой данных
- Компоненты формы с проверкой

---

### 2. Анализатор покрытия { #2-coverage-analyzer }

Анализирует отчеты о охвате Jest/Istanbul и выявляет пробелы, выявленные ответвления, а также предоставляет практические рекомендации.

**Входные данные:** Отчет о покрытии (формат JSON или LCOV)
**Результат:** Анализ охвата с рекомендациями

**Использование:**
```bash
# Analyze coverage report
python scripts/coverage_analyzer.py coverage/coverage-final.json

# Enforce threshold (exit 1 if below)
python scripts/coverage_analyzer.py coverage/ --threshold 80 --strict

# Generate HTML report
python scripts/coverage_analyzer.py coverage/ --format html --output report.html
```

---

### 3. Испытательный каркас E2E { #3-e2e-test-scaffolder }

Сканирование Next.js каталог pages/app и генерирует тестовые файлы драматурга с общими взаимодействиями.

**Входные данные:** Next.js страницы или каталог приложений
** Выходные данные:** Тестовые файлы драматурга, организованные по маршруту

**Использование:**
```bash
# Scaffold E2E tests for Next.js App Router
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/

# Include Page Object Model classes
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/ --include-pom

# Generate for specific routes
python scripts/e2e_test_scaffolder.py src/app/ --routes "/login,/dashboard,/checkout"
```

---

## Воркфлоу контроля качества { #qa-workflows }

### Воркфлоу генерации модульных тестов { #unit-test-generation-workflow }

Используйте при настройке тестов для новых или существующих компонентов React.

**Шаг 1: Просканируйте проект на наличие непроверенных компонентов**
```bash
python scripts/test_suite_generator.py src/components/ --scan-only
```

**Шаг 2: Создание тестовых заготовок**
```bash
python scripts/test_suite_generator.py src/components/ --output __tests__/
```

**Шаг 3: Ревью и настройка сгенерированных тестов**
```typescript
// __tests__/Button.test.tsx (generated)
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../src/components/Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  // TODO: Add your specific test cases
});
```

** Шаг 4: Запустите тесты и проверьте покрытие**
```bash
npm test -- --coverage
python scripts/coverage_analyzer.py coverage/coverage-final.json
```

---

### Воркфлоу анализа покрытия { #coverage-analysis-workflow }

Используйте при улучшении тестового покрытия или подготовке к выпуску.

**Шаг 1: Сгенерируйте отчет о покрытии**
```bash
npm test -- --coverage --coverageReporters=json
```

**Шаг 2: Проанализируйте пробелы в охвате**
```bash
python scripts/coverage_analyzer.py coverage/coverage-final.json --threshold 80
```

**Шаг 3: Определите критические пути**
```bash
python scripts/coverage_analyzer.py coverage/ --critical-paths
```

**Шаг 4: Сгенерируйте отсутствующие тестовые заглушки**
```bash
python scripts/test_suite_generator.py src/ --uncovered-only --output __tests__/
```

**Шаг 5: Проверьте улучшение**
```bash
npm test -- --coverage
python scripts/coverage_analyzer.py coverage/ --compare previous-coverage.json
```

---

### Воркфлоу настройки тестирования E2E { #e2e-test-setup-workflow }

Используется при настройке драматурга для Next.js проект.

**Шаг 1: Инициализируйте Playground (если он не установлен)**
```bash
npm init playwright@latest
```

**Шаг 2: Тесты Scaffold E2E на основе маршрутов**
```bash
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/
```

**Шаг 3: Настройка средств аутентификации**
```typescript
// e2e/fixtures/auth.ts (generated)
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
    await use(page);
  },
});
```

**Шаг 4: Запустите тесты E2E**
```bash
npx playwright test
npx playwright show-report
```

**Шаг 5: Добавление в пайплайн CI**
```yaml
# .github/workflows/e2e.yml
- name: "run-e2e-tests"
  run: npx playwright test
- name: "upload-report"
  uses: actions/upload-artifact@v3
  with:
    name: "playwright-report"
    path: playwright-report/
```

---

## Справочная документация { #reference-documentation }

| Файл | Содержит | Используйте, когда |
|------|----------|----------|
| `references/testing_strategies.md` | Тестовая пирамида, типы тестирования, цели покрытия, интеграция CI/CD | Разработка стратегии тестирования |
| `references/test_automation_patterns.md` | Объектная модель страницы, макетирование (MSW), приспособления, асинхронные шаблоны | Написание тестового кода |
| `references/qa_best_practices.md` | Тестируемый код, слоеные тесты, отладка, показатели качества | Повышение качества тестирования |

---

## Краткий справочник по общим шаблонам { #common-patterns-quick-reference }

### Запросы библиотеки тестирования React { #react-testing-library-queries }

```typescript
// Preferred (accessible)
screen.getByRole('button', { name: /submit/i })
screen.getByLabelText(/email/i)
screen.getByPlaceholderText(/search/i)

// Fallback
screen.getByTestId('custom-element')
```

### Асинхронное тестирование { #async-testing }

```typescript
// Wait for element
await screen.findByText(/loaded/i);

// Wait for removal
await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));

// Wait for condition
await waitFor(() => {
  expect(mockFn).toHaveBeenCalled();
});
```

### Издевательство над ТБО { #mocking-with-msw }

```typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json([{ id: 1, name: "john" }]));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Поиск драматургов { #playwright-locators }

```typescript
// Preferred
page.getByRole('button', { name: "submit" })
page.getByLabel('Email')
page.getByText('Welcome')

// Chaining
page.getByRole('listitem').filter({ hasText: 'Product' })
```

### Пороговые значения охвата (jest.config.js ) { #coverage-thresholds-jestconfigjs }

```javascript
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

---

## Общие команды { #common-commands }

```bash
# Jest
npm test                           # Run all tests
npm test -- --watch                # Watch mode
npm test -- --coverage             # With coverage
npm test -- Button.test.tsx        # Single file

# Playwright
npx playwright test                # Run all E2E tests
npx playwright test --ui           # UI mode
npx playwright test --debug        # Debug mode
npx playwright codegen             # Generate tests

# Coverage
npm test -- --coverage --coverageReporters=lcov,json
python scripts/coverage_analyzer.py coverage/coverage-final.json
```
