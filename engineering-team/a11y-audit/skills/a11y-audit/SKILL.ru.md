---
name: "a11y-audit"
description: "Скилл аудита доступности для сканирования, исправления и проверки соответствия требованиям WCAG 2.2 уровня A и AA в React, Next.js , Vue, Angular, Svelte и простые кодовые базы HTML. Используется при аудите доступности, устранении нарушений a11y, проверке цветового контраста, создании отчетов о соответствии требованиям или интеграции проверок доступности в пайплайны CI/CD."
---

# Аудит доступности { #accessibility-audit }

WCAG 2.2 Аудит доступности и скиллы по исправлению ошибок

## Описание { #description }

Скилл a11y-аудит обеспечивает полный пайплайн аудита доступности для современных веб-приложений. В нем реализован трехэтапный воркфлоу - сканирование, исправление, проверка, - который выявляет нарушения уровня A и AA WCAG 2.2, генерирует точный код исправления для каждого фреймворка и подготавливает отчеты о соответствии, готовые для стейкхолдеров.

Для каждого обнаруженного нарушения он предоставляет точное исправление кода до / после, адаптированное к вашему фреймворку (React, Next.js , Vue, Angular, Svelte или обычный HTML).

**Что делает этот скилл:**

1. ** Сканирует** вашу кодовую базу на наличие каждого нарушения WCAG 2.2 уровней A и AA, классифицированного по степени серьезности (Критическое, серьезное, незначительное).
2. ** Исправляет** каждое нарушение с помощью специфичных для фреймворка шаблонов кода до/после
3. **Проверяет**, что исправления устраняют исходные нарушения и не приводят к регрессиям
4. ** Отчеты** выводы в структурированном формате, подходящем для разработчиков, руководителей подразделений и стейкхолдеров, заинтересованных в соблюдении требований
5. **Интегрируется ** в пайплайны CI/CD для предотвращения регрессий доступности

## Особенности { #features }

| Особенность | Описание |
|---------|-------------|
| **Полное сканирование WCAG 2.2** | Проверяет все критерии успешности уровней A и AA в вашей кодовой базе |
| **Обнаружение фреймворка** | Автоматически определяет реакцию, Next.js , Vue, Angular, Svelte или обычный HTML |
| **Классификация степени тяжести** | Классифицирует каждое нарушение как критическое, серьезное или незначительное |
| ** Исправлена генерация кода** | Создает различия в коде до/после каждой проблемы |
| **Проверка цветового контраста** | Проверяет пары передний план/фон на соответствие соотношениям AA и AAA |
| **Отчетность о соблюдении требований** | Генерирует отчеты стейкхолдеров с краткими сведениями о пройденных испытаниях/неудачах |
| **Интеграция CI/CD** | Действия на GitHub, GitLab CI, конфигурации для пайплайна Azure DevOps |
| **Аудит навигации по клавиатуре** | Обнаруживает отсутствующие проблемы с управлением фокусом и порядком вкладок |
| **Проверка ARIA** | Проверяет наличие неправильных, избыточных или отсутствующих атрибутов ARIA |

### Определения серьезности { #severity-definitions }

| Серьезность | Определение | Пример | Соглашение об уровне обслуживания |
|----------|-----------|---------|-----|
| **Критический** | Блокирует доступ для целых групп пользователей | Отсутствует текст alt, нет доступа к навигации с клавиатуры | Исправление перед выпуском |
| **Основные** | Значительный барьер, который ухудшает восприятие | Недостаточный цветовой контраст, отсутствуют надписи на форме | Исправлено в рамках текущего спринта |
| **Незначительный** | Проблема удобства использования, вызывающая трения | Избыточные роли ARIA, неоптимальная иерархия заголовков | Исправьте в течение следующих 2-х спринтов |

## Использование { #usage }

### Быстрый старт { #quick-start }

```bash
# Scan entire project
python scripts/a11y_scanner.py /path/to/project

# Scan with JSON output for tooling
python scripts/a11y_scanner.py /path/to/project --json

# Check color contrast for specific values
python scripts/contrast_checker.py --fg "#777777" --bg "#ffffff"

# Check contrast across a CSS/Tailwind file
python scripts/contrast_checker.py --file /path/to/styles.css
```

### Слэш-команда { #slash-command }

```
/a11y-audit                    # Audit current project
/a11y-audit --scope src/       # Audit specific directory
/a11y-audit --fix              # Audit and auto-apply fixes
/a11y-audit --report           # Generate stakeholder report
/a11y-audit --ci               # Output CI-compatible results
```

### Трехфазный воркфлоу { #three-phase-workflow }

** Фаза 1: Сканирование** -- Прохождение по дереву исходных текстов, обнаружение фреймворка, применение набора правил.

```bash
python scripts/a11y_scanner.py /path/to/project --format table
```

** Этап 2: Исправление ** -- Применяйте исправления, специфичные для фреймворка, для каждого нарушения.

> Видишь [ссылки/фреймворк-a11y-patterns.md](references/framework-a11y-patterns.md) для получения полного каталога шаблонов исправлений.

**Этап 3: Проверка** -- Повторно запустите сканер, чтобы подтвердить исправления и проверить наличие регрессий.

```bash
python scripts/a11y_scanner.py /path/to/project --baseline audit-baseline.json
```

## Пример: Аудит компонента React { #example-react-component-audit }

```tsx
// BEFORE: src/components/ProductCard.tsx
function ProductCard({ product }) {
  return (
    <div onClick={() => navigate(`/product/${product.id}`)}>
      <img src={product.image} />
      <div style={{ color: '#aaa', fontSize: '12px' }}>{product.name}</div>
      <span style={{ color: '#999' }}>${product.price}</span>
    </div>
  );
}
```

| # | WCAG | Суровость | Проблема |
|---|------|----------|-------|
| 1 | 1.1.1 | Критический | `<img>` пропавший без вести `alt` атрибут |
| 2 | 2.1.1 | Критический | `<div onClick>` недоступна клавиатура |
| 3 | 1.4.3 | Майор | Цвет `#aaa` на белом не хватает контрастности (2,32:1, требуется 4,5:1) |
| 4 | 1.4.3 | Майор | Цвет `#999` на белом не хватает контрастности (2,85:1, требуется 4,5:1) |
| 5 | 4.1.2 | Майор | Интерактивный элемент, в котором отсутствует роль и доступное имя |

```tsx
// AFTER: src/components/ProductCard.tsx
function ProductCard({ product }) {
  return (
    <a href={`/product/${product.id}`} className="product-card"
       aria-label={`View ${product.name} - $${product.price}`}>
      <img src={product.image} alt={product.imageAlt || product.name} />
      <div style={{ color: '#595959', fontSize: '12px' }}>{product.name}</div>
      <span style={{ color: '#767676' }}>${product.price}</span>
    </a>
  );
}
```

> Видишь [ссылки/примеры по фреймворкам.md](references/examples-by-framework.md) для Vue, Angular, Next.js , и стройные примеры.

## Ссылка на инструменты { #tools-reference }

### a11y_scanner.py { #a11y_scannerpy }

```
Usage: python scripts/a11y_scanner.py <path> [options]

Options:
  --json                  Output results as JSON
  --format {table,csv}    Output format (default: table)
  --severity {critical,major,minor}  Filter by minimum severity
  --framework {react,vue,angular,svelte,html,auto}  Force framework (default: auto)
  --baseline FILE         Compare against previous scan results
  --report                Generate stakeholder report
  --output FILE           Write results to file
  --quiet                 Suppress output, exit code only
  --ci                    CI mode: non-zero exit on critical issues
```

### contrast_checker.py { #contrast_checkerpy }

```
Usage: python scripts/contrast_checker.py [options]

Options:
  --fg COLOR              Foreground color (hex)
  --bg COLOR              Background color (hex)
  --file FILE             Scan CSS file for color pairs
  --tailwind DIR          Scan directory for Tailwind color classes
  --json                  Output results as JSON
  --suggest               Suggest accessible alternatives for failures
  --level {aa,aaa}        Target conformance level (default: aa)
```

## Распространенные подводные камни { #common-pitfalls }

| Ловушка | Правильный подход |
|---------|------------------|
| `role="button"` на `<div>` | Используйте собственный `<button>` -- включает в себя бесплатное управление клавиатурой |
| `tabindex="0"` обо всем | Фокус нужен только интерактивным элементам; используйте собственные элементы |
| `aria-label` о неинтерактивных элементах | Использование `aria-labelledby` указывающий на видимый текст |
| `display: none` для скрытия программы чтения с экрана | Использование `.sr-only` класс вместо этого |
| Только цвет может передать смысл | Добавляйте значки, текстовые надписи или узоры наряду с цветом |
| Заполнитель в качестве единственной метки | Всегда обеспечивайте видимый `<label>` |
| `outline: none` без замены | Всегда обеспечивайте видимый индикатор фокусировки с помощью `focus-visible` |
| Пустой `alt=""` на информационных изображениях | Информационные изображения нуждаются в описательном альтернативном тексте |
| Пропуск уровней курса (h1 -> h3) | Уровни заголовка должны быть последовательными |
| `onClick` без `onKeyDown` | Добавьте поддержку клавиатуры или отдайте предпочтение встроенным элементам |
| Игнорируя `prefers-reduced-motion` | Перенос анимации в `@media (prefers-reduced-motion: no-preference)` |

## Связанные скиллы { #related-skills }

| Скилл | Отношения |
|-------|-------------|
| **старший-интерфейс** | Шаблоны интерфейса, используемые в исправлениях a11y |
| **специалист по проверке кода** | Включите проверки a11y в воркфлоу-процессы ревью кода |
| **старший специалист по контролю качества** | Интеграция тестирования a11y в процессы контроля качества |
| **драматург-профессионал** | Автоматическое тестирование браузера с утверждениями о специальных возможностях |
| **эпический дизайн** | Анимация, совместимая с WCAG 2.1 AA, и прокрутка повествования |
| **tdd-руководство** | Шаблоны разработки, управляемые тестированием, для тестовых примеров a11y |

## Справочная документация { #reference-documentation }

| Ссылка | Описание |
|-----------|-------------|
| [wcag-quick-ref.md](references/wcag-quick-ref.md) | Краткий справочник по критериям WCAG 2.2 уровня A и AA |
| [wcag-22-new-criteria.md](references/wcag-22-new-criteria.md) | Новые критерии успеха WCAG 2.2 (внешний вид фокуса, размер цели и т.д.) |
| [aria-patterns.md](references/aria-patterns.md) | Паттерны ARIA, взаимодействие с клавиатурой и живые области |
| [framework-a11y-patterns.md](references/framework-a11y-patterns.md) | Шаблоны исправлений, специфичные для фреймворка (React, Vue, Angular, Svelte, HTML) |
| [color-contrast-guide.md](references/color-contrast-guide.md) | Детали проверки цветового контраста, отображение палитры попутного ветра, класс только для sr |
| [ci-cd-integration.md](references/ci-cd-integration.md) | Действия на GitHub, GitLab CI, Azure DevOps, настройки перехвата перед фиксацией |
| [audit-report-template.md](references/audit-report-template.md) | Готовый шаблон отчета по аудиту для стейкхолдеров |
| [testing-checklist.md](references/testing-checklist.md) | Чек-лист ручного тестирования (клавиатура, программа для чтения с экрана, визуальные средства, формы) |
| [examples-by-framework.md](references/examples-by-framework.md) | Полные примеры аудита для Vue, Angular, Next.js , и стройная |

## Ресурсы { #resources }

- [Спецификация WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Авторские практики WAI-ARIA 1.2](https://www.w3.org/WAI/ARIA/apg/)
- [Deque axe-основные правила](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [eslint-плагин-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)
