---
title: "Автоматизация браузера - МОЩНАЯ { #browser-automation---powerful } — Агентский скилл для Codex и OpenClaw"
description: "Используйте, когда пользователь просит автоматизировать задачи браузера, очищать веб-сайты, заполнять формы, делать скриншоты, извлекать. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Автоматизация браузера - МОЩНАЯ { #browser-automation---powerful }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `browser-automation`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


## Обзор { #overview }

Скилл по автоматизации браузера предоставляет комплексные инструменты и знания для построения воркфлоу веб-автоматизации производственного уровня с использованием Druggy. Этот скилл охватывает извлечение данных, заполнение форм, захват скриншотов, управление сеансами и шаблоны защиты от обнаружения для надежной масштабной автоматизации браузера.

**Когда использовать этот скилл:**
- Сбор структурированных данных с веб-сайтов (таблицы, списки, результаты поиска)
- Автоматизация многоэтапных воркфлоу-процессов в браузере (вход в систему, заполнение форм, загрузка файлов)
- Захват скриншотов или PDF-файлов веб-страниц
- Извлечение данных из SPA-центров и сайтов, использующих JavaScript
- Построение воспроизводимых пайплайнов данных на основе браузера

**Когда не следует использовать этот скилл:**
- Написание браузерных тестов или наборов тестов E2E — вместо этого используйте **драматург-pro**
- Тестирование конечных точек API — вместо этого используйте ** api-test-suite-builder**
- Нагрузочное тестирование или сравнительный анализ производительности — вместо этого используйте **performance-profiler**

** Почему драматург предпочтительнее Селена или кукловода:**
- **Встроенное автоматическое ожидание ** — нет явного `sleep()` или `waitForElement()` необходим для большинства действий
- ** Мульти-браузер с одним API** — Chromium, Firefox, WebKit с нулевыми изменениями конфигурации
- ** Сетевой перехват ** — блокируйте рекламу, имитируйте ответы, перехватывайте вызовы API изначально
- **Контексты браузера** — изолированные сеансы без запуска новых экземпляров браузера
- **Кодеген** — `playwright codegen` записывает ваши действия и генерирует сценарии
- **Асинхронный-сначала** — Python async/await для высокопроизводительного выскабливания

## Основные компетенции { #core-competencies }

### 1. Узоры соскабливания полотна { #1-web-scraping-patterns }

**Приоритет выбора (от наиболее надежного к наименее надежному):**
1. `data-testid`, `data-id`, или пользовательские атрибуты данных — стабильны при перепроектировании
2. `#id` селекторы — уникальны, но могут изменяться при деплою
3. Семантические селекторы: `article`, `nav`, `main`, `section` — устойчивость к изменениям CSS
4. Основанный на классе: `.product-card`, `.price` — хрупкий, если генерируются классы (например, CSS-модули)
5. Позиционный: `nth-child()`, `nth-of-type()` — в крайнем случае, перерывы при изменении макета

Используйте XPath только тогда, когда CSS не может выразить связь (например, обход предков, выделение на основе текста).

** Стратегии разбивки на страницы: ** кнопка "Далее", основанная на URL-адресе (`?page=N`), бесконечная прокрутка, кнопка "Загрузить еще". Видишь [data_extraction_recipes.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/references/data_extraction_recipes.md) для полных обработчиков разбивки на страницы и шаблонов прокрутки.

### 2. Заполнение форм и многоступенчатый воркфлоу { #2-form-filling--multi-step-workflows }

Разбейте многоступенчатые формы на отдельные функции для каждого шага. Каждая функция заполняет поля, нажимает "Далее"/"Продолжить" и ожидает загрузки следующего шага (изменение URL-адреса или элемента DOM).

Ключевые шаблоны: потоки входа в систему, многостраничные формы, загрузка файлов (включая зоны перетаскивания), встроенная и пользовательская обработка выпадающих списков. Видишь [playwright_browser_api.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/references/playwright_browser_api.md) для получения полной ссылки на API на `fill()`, `select_option()`, `set_input_files()`, и `expect_file_chooser()`.

### 3. Снимок экрана и PDF-файл { #3-screenshot--pdf-capture }

- **Полная страница:** `await page.screenshot(path="full.png", full_page=True)`
- **Элемент:** `await page.locator("div.chart").screenshot(path="chart.png")`
- **PDF (только для Chromium):** `await page.pdf(path="out.pdf", format="A4", print_background=True)`
- ** Визуальная регрессия:** Делайте скриншоты в известных состояниях, сохраняйте базовые значения в системе управления версиями с указанием имен: `{page}_{viewport}_{state}.png`

Видишь [playwright_browser_api.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/references/playwright_browser_api.md) для получения полных параметров скриншота / PDF.

### 4. Извлечение структурированных данных { #4-structured-data-extraction }

Схемы извлечения керна:
- **Таблицы в формате JSON** — Извлечение `<thead>` заголовки и `<tbody>` строки в словари
- ** Списки в массивы** — Сопоставление повторяющихся элементов карточки с помощью карты выбора полей (поддерживает `::attr()` для атрибутов)
- **Вложенный/threaded данные** — Рекурсивное извлечение комментариев с ответами, деревьев категорий

Видишь [data_extraction_recipes.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/references/data_extraction_recipes.md) для полных функций извлечения, анализа цен, утилит очистки данных и помощников по формату вывода (JSON, CSV, JSONL).

### 5. Файлы cookie и управление сеансами { #5-cookie--session-management }

- **Сохранить/restore файлы cookie:** `context.cookies()` и `context.add_cookies()`
- **Полное состояние хранилища ** (cookies + localStorage): `context.storage_state(path="state.json")` чтобы спасти, `browser.new_context(storage_state="state.json")` чтобы восстановить

** Наилучшая практика: ** Сохраняйте состояние после входа в систему, повторно используйте во всех сеансах очистки. Проверьте действительность сеанса перед началом длительной работы — сделайте легкий запрос на защищенную страницу и убедитесь, что вы не перенаправлены для входа в систему. Видишь [playwright_browser_api.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/references/playwright_browser_api.md) для получения подробной информации о файлах cookie и состоянии хранилища в API.

### 6. Схемы защиты от обнаружения { #6-anti-detection-patterns }

Современные веб-сайты обнаруживают автоматизацию по нескольким векторам. Применяйте их в приоритетном порядке:

1. **Удаление флага WebDriver** — Удалить `navigator.webdriver = true` с помощью скрипта инициализации (критично)
2. ** Пользовательский агент пользователя ** — Переключение через реальные пользовательские интерфейсы браузера; никогда не используйте безголовый пользовательский интерфейс по умолчанию
3. **Реалистичный экран просмотра** — Установите 1920x1080 или аналогичные реальные размеры (по умолчанию 800x600 - красный флажок)
4. **Запросить регулирование** — Добавить `random.uniform()` задержки между действиями
5. ** Поддержка прокси—сервера ** - Настройка прокси-сервера для каждого браузера или контекста

Видишь [anti_detection_patterns.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/references/anti_detection_patterns.md) для полного стелс-стека: усиление свойств навигатора, WebGL/canvas уклонение от отпечатков пальцев, моделирование поведения (движение мыши, скорость набора текста, шаблоны прокрутки), стратегии поворота прокси-серверов и URL-адреса для самопроверки обнаружения.

### 7. Динамическая обработка контента { #7-dynamic-content-handling }

- **Рендеринг SPA:** Дождитесь выбора содержимого (`wait_for_selector`), а не событие загрузки страницы
- **Ожидание AJAX/выборки:** Используйте `page.expect_response("**/api/data*")` для перехвата и ожидания определенных вызовов API
- ** Теневой ДОМ:** Драматург пронзает открытый Теневой ДОМ с помощью `>>` оператор: `page.locator("custom-element >> .inner-class")`
- ** Изображения с отложенной загрузкой:** Прокрутите элементы в поле зрения с помощью `scroll_into_view_if_needed()` чтобы запустить загрузку триггера

Видишь [playwright_browser_api.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/references/playwright_browser_api.md) для получения информации о стратегиях ожидания, сетевом перехвате и теневом DOM.

### 8. Логика обработки ошибок и повторных попыток { #8-error-handling--retry-logic }

- ** Повторите попытку с отсрочкой:** Перенесите взаимодействия со страницами в логику повторных попыток с экспоненциальной отсрочкой (например, 1s, 2s, 4s).
- **Резервные селекторы:** Вкл. `TimeoutError`, попробуйте альтернативные селекторы, прежде чем потерпеть неудачу
- **Скриншоты состояния ошибки:** Захват `page.screenshot(path="error-state.png")` о неожиданных сбоях при отладке
- ** Определение ограничения скорости:** Проверьте наличие ответов HTTP 429 и соблюдайте `Retry-After` заголовки

Видишь [anti_detection_patterns.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/browser-automation/references/anti_detection_patterns.md) для полной реализации экспоненциального отката и класса ограничителей скорости.

## Воркфлоу { #workflows }

### Воркфлоу 1: Извлечение данных на одной странице { #workflow-1-single-page-data-extraction }

** Сценарий:** Извлеките данные о продукте с одной страницы с отрисованным на JavaScript контентом.

**Шаги:**
1. Запустите браузер в автономном режиме во время разработки (`headless=False`), переключитесь на безголовый режим для производства
2. Перейдите по URL-адресу и дождитесь выбора содержимого
3. Извлекать данные с помощью `query_selector_all` с отображением полей
4. Проверка извлеченных данных (проверка на наличие нулей, ожидаемых типов)
5. Вывод в формате JSON

```python
async def extract_single_page(url, selectors):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 ..."
        )
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")
        data = await extract_listings(page, selectors["container"], selectors["fields"])
        await browser.close()
    return data
```

### Воркфлоу 2: Многостраничная очистка с разбивкой на страницы { #workflow-2-multi-page-scraping-with-pagination }

** Сценарий: ** Очистите результаты поиска более чем на 50 страницах.

**Шаги:**
1. Запустите браузер с настройками защиты от обнаружения
2. Перейдите на первую страницу
3. Извлекать данные с текущей страницы
4. Проверьте, существует ли кнопка "Далее" и включена ли она
5. Нажмите далее, дождитесь загрузки нового контента (не только навигации).
6. Повторяйте до тех пор, пока не будет достигнута следующая страница или максимальное количество страниц
7. Дедуплицировать результаты по уникальному ключу
8. Записывайте выходные данные постепенно (не храните все в памяти)

```python
async def scrape_paginated(base_url, selectors, max_pages=100):
    all_data = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await (await browser.new_context()).new_page()
        await page.goto(base_url)

        for page_num in range(max_pages):
            items = await extract_listings(page, selectors["container"], selectors["fields"])
            all_data.extend(items)

            next_btn = page.locator(selectors["next_button"])
            if await next_btn.count() == 0 or await next_btn.is_disabled():
                break

            await next_btn.click()
            await page.wait_for_selector(selectors["container"])
            await human_delay(800, 2000)

        await browser.close()
    return all_data
```

### Воркфлоу 3: Автоматизация воркфлоу с проверкой подлинности { #workflow-3-authenticated-workflow-automation }

** Сценарий:** Войдите на портал, перейдите по многоэтапной форме, загрузите отчет.

**Шаги:**
1. Проверьте наличие существующего файла состояния сеанса
2. Если сеанса нет, выполните вход в систему и сохраните состояние
3. Перейдите на целевую страницу, используя сохраненный сеанс
4. Заполните многоэтапную форму с предоставленными данными
5. Дождитесь загрузки, чтобы триггер сработал
6. Сохраните загруженный файл в целевой каталог

```python
async def authenticated_workflow(credentials, form_data, download_dir):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        state_file = "session_state.json"

        # Restore or create session
        if os.path.exists(state_file):
            context = await browser.new_context(storage_state=state_file)
        else:
            context = await browser.new_context()
            page = await context.new_page()
            await login(page, credentials["url"], credentials["user"], credentials["pass"])
            await context.storage_state(path=state_file)

        page = await context.new_page()
        await page.goto(form_data["target_url"])

        # Fill form steps
        for step_fn in [fill_step_1, fill_step_2]:
            await step_fn(page, form_data)

        # Handle download
        async with page.expect_download() as dl_info:
            await page.click("button:has-text('Download Report')")
        download = await dl_info.value
        await download.save_as(os.path.join(download_dir, download.suggested_filename))

        await browser.close()
```

## Ссылка на инструменты { #tools-reference }

| Сценарий | Цель | Ключевые флаги | Выход |
|--------|---------|-----------|--------|
| `scraping_toolkit.py` | Сгенерировать скелет сценария, очищающий драматурга | `--url`, `--selectors`, `--paginate`, `--output` | Скрипт на Python или конфигурация JSON |
| `form_automation_builder.py` | Сгенерировать сценарий автоматизации заполнения формы на основе спецификации поля | `--fields`, `--url`, `--output` | Сценарий автоматизации на Python |
| `anti_detection_checker.py` | Аудит сценария драматурга для определения векторов | `--file`, `--verbose` | Отчет о рисках с оценкой |

Все скрипты доступны только для stdlib. Бежать `python3 <script> --help` для полноценного использования.

## Анти-паттерны { #anti-patterns }

### Жестко запрограммированные ожидания { #hardcoded-waits }
**Плохой:** `await page.wait_for_timeout(5000)` перед каждым действием.
** Хорошо:** Используйте `wait_for_selector`, `wait_for_url`, `expect_response`, или `wait_for_load_state` Жестко запрограммированные ожидания являются ненадежными и медленными.

### Нет восстановления после ошибок { #no-error-recovery }
**Плохо:** Линейный скрипт, который вылетает при первом сбое.
** Хорошо:** Оберните каждое взаимодействие со страницей в try/except. Сделайте скриншоты состояния ошибки. Реализуйте повторную попытку с экспоненциальным отступлением.

### Игнорируя robots.txt { #ignoring-robotstxt }
**Плохо:** Выскабливание без проверки robots.txt директивы.
** Хорошо:** Выборка и синтаксический анализ robots.txt перед выскабливанием. Уважение `Crawl-delay`. Пропускать запрещенные пути. Добавьте имя вашего бота в User-агент, если он работает в масштабе.

### Хранение учетных данных в скриптах { #storing-credentials-in-scripts }
** Плохо:** Жесткое кодирование имен пользователей и паролей в файлах Python.
** Хорошо:** Используйте переменные окружения, `.env` файлы (gitignored) или менеджер секретов. Передайте учетные данные с помощью аргументов CLI.

### Отсутствие ограничения скорости { #no-rate-limiting }
**Плохо:** Забивание сайта 100 запросами/second.
** Хорошо: ** Добавьте случайные задержки между запросами (1-3 секунды для вежливого выскабливания). Отслеживайте наличие 429 ответов. Реализуйте экспоненциальный откат.

### Хрупкость селектора { #selector-fragility }
** Плохо:** Полагаться на автоматически сгенерированные имена классов (`.css-1a2b3c`) или глубокое гнездование (`div > div > div > span:nth-child(3)`).
** Хорошо:** Используйте атрибуты данных, семантический HTML или текстовые локаторы. Сначала протестируйте селекторы в браузере DevTools.

### Не очищаются экземпляры браузера { #not-cleaning-up-browser-instances }
** Плохо:** Запуск браузеров без их закрытия приводит к утечке ресурсов.
** Хорошо:** Всегда используйте `try/finally` или асинхронные контекстные менеджеры для обеспечения `browser.close()` называется.

### Запущенный в производство { #running-headed-in-production }
**Плохо:** Использование `headless=False` в производстве/CI.
**Хорошо:** Разрабатывайте в режиме headed для отладки, деплою с `headless=True`. Используйте переменную окружения для переключения: `headless = os.environ.get("HEADLESS", "true") == "true"`.

## Перекрестные ссылки { #cross-references }

- ** драматург-профессионал ** — Скилл для тестирования браузера. Используйте для тестов E2E, тестовых утверждений, тестовых приспособлений. Автоматизация браузера предназначена для извлечения данных и автоматизации воркфлоу, а не для тестирования.
- **api-test-suite-builder** — Если на веб-сайте есть общедоступный API, используйте API напрямую, вместо того чтобы очищать отображаемую страницу. Быстрее, надежнее, менее обнаруживаемо.
- **профилировщик производительности** - Если ваши сценарии автоматизации работают медленно, определите узкие места, прежде чем добавлять параллелизм.
- **env-secrets-manager** — Для безопасного управления учетными данными, используемыми в аутентифицированных воркфлоу автоматизации.
