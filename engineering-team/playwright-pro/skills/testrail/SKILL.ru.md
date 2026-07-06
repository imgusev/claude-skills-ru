---
name: "testrail"
description: ">-"
  Sync tests with TestRail. Use when user mentions "testrail", "test management",
  "test cases", "test run", "sync test cases", "push results to testrail",
  or "import from testrail".
---

# Интеграция с TestRail { #testrail-integration }

Двунаправленная синхронизация между тестами драматурга и управлением тестами TestRail.

## Предварительные условия { #prerequisites }

Должны быть установлены переменные окружения:
- `TESTRAIL_URL` — например., `https://your-instance.testrail.io`
- `TESTRAIL_USER` — ваш адрес электронной почты
- `TESTRAIL_API_KEY` — Ключ API от TestRail

Если они не установлены, сообщите пользователю, как их настроить, и остановитесь.

## Возможности { #capabilities }

### 1. Импорт тестовых наборов → Создание тестов драматурга { #1-import-test-cases--generate-playwright-tests }

```
/pw:testrail import --project <id> --suite <id>
```

Шаги:
1. Вызов `testrail_get_cases` Инструмент MCP для выборки тестовых примеров
2. Для каждого тестового примера:
   - Прочитайте название, предварительные условия, шаги, ожидаемые результаты
   - Сопоставьте с тестом драматурга, используя соответствующий шаблон
   - Включить идентификатор случая TestRail в качестве аннотации к тесту: `test.info().annotations.push({ type: 'testrail', description: 'C12345' })`
3. Генерировать тестовые файлы, сгруппированные по разделам
4. Отчет: Импортировано X случаев, сгенерировано Y тестов

### 2. Нажмите результаты теста → TestRail { #2-push-test-results--testrail }

```
/pw:testrail push --run <id>
```

Шаги:
1. Запустите тесты драматурга с помощью JSON reporter:
   ```bash
   npx playwright test --reporter=json > test-results.json
   ```
2. Результаты анализа: сопоставьте каждый тест с его идентификатором случая TestRail (из аннотаций)
3. Вызов `testrail_add_result` Инструмент MCP для каждого теста:
   - Pass → status_id: 1
   - Ошибка → status_id: 5, включить сообщение об ошибке
   - Пропустить → status_id: 2
4. Отчет: X результатов выдано, Y пройдено, Z не выполнено

### 3. Создайте тестовый запуск { #3-create-test-run }

```
/pw:testrail run --project <id> --name "Sprint 42 Regression"
```

Шаги:
1. Вызов `testrail_add_run` Инструмент MCP
2. Включите все идентификаторы тестовых наборов, найденные в аннотациях к тестам драматурга
3. Возвращает идентификатор запуска для передачи результата

### 4. Состояние синхронизации { #4-sync-status }

```
/pw:testrail status --project <id>
```

Шаги:
1. Извлекать тестовые примеры из TestRail
2. Отсканируйте локальные тесты драматурга на предмет аннотаций к TestRail
3. Охват отчета:
   ```
   TestRail cases: 150
   Playwright tests with TestRail IDs: 120
   Unlinked TestRail cases: 30
   Playwright tests without TestRail IDs: 15
   ```

### 5. Обновите тестовые примеры в TestRail { #5-update-test-cases-in-testrail }

```
/pw:testrail update --case <id>
```

Шаги:
1. Прочтите тест драматурга для этого случая.
2. Извлеките шаги и ожидаемые результаты из тестового кода
3. Вызов `testrail_update_case` Инструмент MCP для обновления шагов

## Используемые инструменты MCP { #mcp-tools-used }

| Инструмент | Когда |
|---|---|
| `testrail_get_projects` | Список доступных проектов |
| `testrail_get_suites` | Список апартаментов в проекте |
| `testrail_get_cases` | Прочитайте тестовые примеры |
| `testrail_add_case` | Создайте новый тестовый пример |
| `testrail_update_case` | Обновить существующий случай |
| `testrail_add_run` | Создать тестовый запуск |
| `testrail_add_result` | Подтолкните индивидуальный результат |
| `testrail_get_results` | Ознакомьтесь с историческими результатами |

## Формат тестовой аннотации { #test-annotation-format }

Все тесты драматурга, связанные с TestRail, включают:

```typescript
test('should login successfully', async ({ page }) => {
  test.info().annotations.push({
    type: 'testrail',
    description: 'C12345',
  });
  // ... test code
});
```

Эта аннотация является связующим звеном между драматургом и TestRail.

## Выход { #output }

- Краткое описание операции с подсчетом
- Любые ошибки или несоответствующие случаи
- Ссылка на запуск TestRail/results
