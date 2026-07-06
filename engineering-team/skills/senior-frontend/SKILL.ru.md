---
name: "senior-frontend"
description: "Скилл разработки интерфейса для React, Next.js , TypeScript и CSS-приложения Tailwind. Используйте при создании компонентов React, оптимизируя Next.js производительность, анализ размеров пакетов, построение каркасов интерфейсных проектов, внедрение доступности или ревью качества интерфейсного кода."
---

# Старший интерфейс { #senior-frontend }

Шаблоны разработки интерфейса, оптимизация производительности и инструменты автоматизации для React/Next.js приложения.

## Оглавление { #table-of-contents }

- [Строительные леса проекта](#project-scaffolding)
- [Генерация компонентов](#component-generation)
- [Анализ пакетов](#bundle-analysis)
- [Паттерны реагирования](#react-patterns)
- [Next.js Оптимизация](#nextjs-optimization)
- [Доступность и тестирование](#accessibility-and-testing)

---

## Строительные леса проекта { #project-scaffolding }

Сгенерировать новый Next.js или проект React с использованием TypeScript, Tailwind CSS и конфигураций best practice.

### Воркфлоу: Создайте новый интерфейсный проект { #workflow-create-new-frontend-project }

1. Запустите scaffolder с названием вашего проекта и шаблоном:
   ```bash
   python scripts/frontend_scaffolder.py my-app --template nextjs
   ```

2. Добавить дополнительные функции (аутентификация, api, формы, тестирование, сборник рассказов):
   ```bash
   python scripts/frontend_scaffolder.py dashboard --template nextjs --features auth,api
   ```

3. Перейдите к проекту и установите зависимости:
   ```bash
   cd my-app && npm install
   ```

4. Запустите сервер разработки:
   ```bash
   npm run dev
   ```

### Варианты строительных лесов { #scaffolder-options }

| Вариант | Описание |
|--------|-------------|
| `--template nextjs` | Next.js 14+ с маршрутизатором приложений и серверными компонентами |
| `--template react` | React + Vite с помощью TypeScript |
| `--features auth` | Добавить NextAuth.js аутентификация |
| `--features api` | Добавить запрос React + API-клиент |
| `--features forms` | Добавить форму React Hook + проверка Zod |
| `--features testing` | Добавить библиотеку тестирования Vitest + |
| `--dry-run` | Предварительный просмотр файлов без их создания |

### Сгенерированная структура (Next.js ) { #generated-structure-nextjs }

```
my-app/
├── app/
│   ├── layout.tsx        # Root layout with fonts
│   ├── page.tsx          # Home page
│   ├── globals.css       # Tailwind + CSS variables
│   └── api/health/route.ts
├── components/
│   ├── ui/               # Button, Input, Card
│   └── layout/           # Header, Footer, Sidebar
├── hooks/                # useDebounce, useLocalStorage
├── lib/                  # utils (cn), constants
├── types/                # TypeScript interfaces
├── tailwind.config.ts
├── next.config.js
└── package.json
```

---

## Генерация компонентов { #component-generation }

Создавайте компоненты React с помощью TypeScript, тестов и сборников рассказов.

### Воркфлоу: Создайте новый компонент { #workflow-create-a-new-component }

1. Создайте клиентский компонент:
   ```bash
   python scripts/component_generator.py Button --dir src/components/ui
   ```

2. Создайте серверный компонент:
   ```bash
   python scripts/component_generator.py ProductCard --type server
   ```

3. Генерировать с помощью файлов тестов и историй:
   ```bash
   python scripts/component_generator.py UserProfile --with-test --with-story
   ```

4. Сгенерируйте пользовательский хук:
   ```bash
   python scripts/component_generator.py FormValidation --type hook
   ```

### Варианты генератора { #generator-options }

| Вариант | Описание |
|--------|-------------|
| `--type client` | Клиентский компонент с "использовать клиента" (по умолчанию) |
| `--type server` | Асинхронный серверный компонент |
| `--type hook` | Пользовательский крючок React hook |
| `--with-test` | Включить тестовый файл |
| `--with-story` | Включите историю из сборника рассказов |
| `--flat` | Создать в выходном каталоге без подкаталога |
| `--dry-run` | Предварительный просмотр без создания файлов |

### Пример сгенерированного компонента { #generated-component-example }

```tsx
'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps {
  className?: string;
  children?: React.ReactNode;
}

export function Button({ className, children }: ButtonProps) {
  return (
    <div className={cn('', className)}>
      {children}
    </div>
  );
}
```

---

## Анализ пакетов { #bundle-analysis }

Проанализируйте package.json и структуру проекта на предмет возможностей оптимизации пакета.

### Воркфлоу: Оптимизация размера пакета { #workflow-optimize-bundle-size }

1. Запустите анализатор в вашем проекте:
   ```bash
   python scripts/bundle_analyzer.py /path/to/project
   ```

2. Ревью оценку состояния здоровья и проблемы:
   ```
   Bundle Health Score: 75/100 (C)

   HEAVY DEPENDENCIES:
     moment (290KB)
       Alternative: date-fns (12KB) or dayjs (2KB)

     lodash (71KB)
       Alternative: lodash-es with tree-shaking
   ```

3. Примените рекомендуемые исправления, заменив тяжелые зависимости.

4. Повторно запустите в подробном режиме, чтобы проверить шаблоны импорта:
   ```bash
   python scripts/bundle_analyzer.py . --verbose
   ```

### Интерпретация результатов набора { #bundle-score-interpretation }

| Оценка | Класс | Действие |
|-------|-------|--------|
| 90-100 | А | Пакет хорошо оптимизирован |
| 80-89 | B | Доступны незначительные оптимизации |
| 70-79 | C | Замените тяжелые зависимости |
| 60-69 | D | Множество вопросов требуют внимания |
| 0-59 | F | Критические проблемы с размером пакета |

### Обнаружены тяжелые зависимости { #heavy-dependencies-detected }

Анализатор идентифицирует эти распространенные тяжелые упаковки:

| Упаковка | Размер | Альтернатива |
|---------|------|-------------|
| момент | 290КБ | дата-fns (12 КБ) или dayjs (2 КБ) |
| Lodash | 71КБ | Lodash-ы с встряхиванием деревьев |
| аксиос | 14 КБАЙТ | Собственная выборка или ky (3 КБ) |
| jquery - запрос | 87КБ | Собственные API-интерфейсы DOM |
| @муи/material | Большой | тень/ui или пользовательский интерфейс Radix |

---

## Паттерны реагирования { #react-patterns }

Ссылка: `references/react_patterns.md`

### Составные компоненты { #compound-components }

Совместное использование состояния между связанными компонентами:

```tsx
const Tabs = ({ children }) => {
  const [active, setActive] = useState(0);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabList;
Tabs.Panel = TabPanel;

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab>One</Tabs.Tab>
    <Tabs.Tab>Two</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel>Content 1</Tabs.Panel>
  <Tabs.Panel>Content 2</Tabs.Panel>
</Tabs>
```

### Изготовленные на заказ крючки { #custom-hooks }

Извлекать логику повторного использования:

```tsx
function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 300);
```

### Рендеринг реквизита { #render-props }

Общая логика рендеринга:

```tsx
function DataFetcher({ url, render }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, [url]);

  return render({ data, loading });
}

// Usage
<DataFetcher
  url="/api/users"
  render={({ data, loading }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
/>
```

---

## Next.js Оптимизация { #nextjs-optimization }

Ссылка: `references/nextjs_optimization_guide.md`

### Серверные и клиентские компоненты { #server-vs-client-components }

По умолчанию используются серверные компоненты. Добавляйте "использовать клиент" только тогда, когда вам это нужно:
- Обработчики событий (onClick, onChange)
- Состояние (useState, useReducer)
- Эффекты (useEffect)
- API-интерфейсы браузера

```tsx
// Server Component (default) - no 'use client'
async function ProductPage({ params }) {
  const product = await getProduct(params.id);  // Server-side fetch

  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} />  {/* Client component */}
    </div>
  );
}

// Client Component
'use client';
function AddToCartButton({ productId }) {
  const [adding, setAdding] = useState(false);
  return <button onClick={() => addToCart(productId)}>Add</button>;
}
```

### Оптимизация изображения { #image-optimization }

```tsx
import Image from 'next/image';

// Above the fold - load immediately
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
/>

// Responsive image with fill
<div className="relative aspect-video">
  <Image
    src="/product.jpg"
    alt="Product"
    fill
    sizes="(max-width: 768px) 100vw, 50vw"
    className="object-cover"
  />
</div>
```

### Шаблоны выборки данных { #data-fetching-patterns }

```tsx
// Parallel fetching
async function Dashboard() {
  const [user, stats] = await Promise.all([
    getUser(),
    getStats()
  ]);
  return <div>...</div>;
}

// Streaming with Suspense
async function ProductPage({ params }) {
  return (
    <div>
      <ProductDetails id={params.id} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>
    </div>
  );
}
```

---

## Доступность и тестирование { #accessibility-and-testing }

Ссылка: `references/frontend_best_practices.md`

### Чек-лист по доступу к веб-сайтам. { #accessibility-checklist }

1. **Семантический HTML**: Используйте правильные элементы (`<button>`, `<nav>`, `<main>`)
2. ** Навигация с клавиатуры**: Все интерактивные элементы можно сфокусировать
3. **Ярлыки ARIA**: Предоставляют ярлыки для значков и сложных виджетов
4. **Цветовой контраст**: Минимум 4,5:1 для обычного текста
5. **Индикаторы фокусировки**: Видимые состояния фокусировки

```tsx
// Accessible button
<button
  type="button"
  aria-label="Close dialog"
  onClick={onClose}
  className="focus-visible:ring-2 focus-visible:ring-blue-500"
>
  <XIcon aria-hidden="true" />
</button>

// Skip link for keyboard users
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### Стратегия тестирования { #testing-strategy }

```tsx
// Component test with React Testing Library
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('button triggers action on click', async () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click me</Button>);

  await userEvent.click(screen.getByRole('button'));
  expect(onClick).toHaveBeenCalledTimes(1);
});

// Test accessibility
test('dialog is accessible', async () => {
  render(<Dialog open={true} title="Confirm" />);

  expect(screen.getByRole('dialog')).toBeInTheDocument();
  expect(screen.getByRole('dialog')).toHaveAttribute('aria-labelledby');
});
```

---

## Краткий справочник { #quick-reference }

### Общий Next.js Конфигурация { #common-nextjs-config }

```js
// next.config.js
const nextConfig = {
  images: {
    remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com' }],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizePackageImports: ['lucide-react', '@heroicons/react'],
  },
};
```

### Утилиты Tailwind CSS { #tailwind-css-utilities }

```tsx
// Conditional classes with cn()
import { cn } from '@/lib/utils';

<button className={cn(
  'px-4 py-2 rounded',
  variant === 'primary' && 'bg-blue-500 text-white',
  disabled && 'opacity-50 cursor-not-allowed'
)} />
```

### Шаблоны машинописного текста { #typescript-patterns }

```tsx
// Props with children
interface CardProps {
  className?: string;
  children: React.ReactNode;
}

// Generic component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

---

## Ресурсы { #resources }

- Паттерны реагирования: `references/react_patterns.md`
- Next.js Оптимизация: `references/nextjs_optimization_guide.md`
- Лучшие практики: `references/frontend_best_practices.md`
- Библиотека форсирующих вопросов (Мэтт Покок Грилл): `references/forcing_questions.md`
- Карта состава (на какого специалиста раскошелиться): `references/composition_map.md`

---

## Допущения и поддающиеся проверке критерии успеха (дисциплина Карпатии) { #assumptions-and-verifiable-success-criteria-karpathy-discipline }

Прежде чем этот скилл сформирует компонент, порекомендует фреймворк или проведет аудит пакета, необходимо выполнить следующие четыре допущения.

1. ** Основное пользовательское устройство + сеть ** — мобильная-4G, настольная-оптоволоконная, недорогая-Android или корпоративная-сеть. Определяет каждое совершенное решение.
2. **Целевой показатель LCP в миллисекундах** — одиночное число, а не "быстрое". Определяет бюджет пакета и выбор рендеринга.
3. **Зависит от SEO и не зависит от auth-walled** — управляет рендерингом (SSR/SSG/RSC против SPA).
4. **Цель WCAG + названный владелец a11y** — AA, AAA или наилучший результат. Стимулирует инвестиции в 11 лет и гейты CI.

**Поддающиеся проверке критерии успеха** (Карпатия №4) — каждая рекомендация должна включать:

- Основные цели Web Vitals (LCP, INP, CLS) на p75 на основном устройстве
- Бюджет пакета JS для каждого маршрута в KB-gzip
- Маяк a11y этаж + улучшенный этаж

Если какой—либо из этих трех параметров не указан, рекомендация является неполной - вернитесь к Q2 библиотеки принудительных вопросов.

Тот `scripts/frontend_decision_engine.py` инструмент кодирует эти проверки: он отказывается рекомендовать профиль без четырех исходных данных и печатает поддающиеся проверке пороговые значения для соответствующего профиля.

---

## Профили настройки { #customization-profiles }

Четыре встроенных профиля в `profiles/` откалибруйте каждую рекомендацию:

| Профиль | Когда выбирать | Цель LCP (мобильный телефон-4G p75) | Бюджет пакета |
|---|---|---|---|
| `next-app-router` | SaaS ориентирован на клиента, SEO + динамика, RSC-first | 2000 мс | 150 КБ-gzip / маршрут |
| `remix-or-sveltekit` | Мобильная связь-4G первичная, с низким уровнем JS-в первую очередь, прогрессивное усовершенствование | 1500 мс | 80 КБ-gzip / маршрут |
| `vite-spa` | Приложение с авторизацией на стене, рабочий стол/corporate первичный | 2500 мс | 200 КБ init + 80 КБ / маршрут |
| `astro-or-static` | Маркетинг / документы / блог, почти нулевой уровень написания, SEO-критичен | 1200 мс | 30 КБ JS / страница |

Выберите профиль с помощью:

```bash
python scripts/frontend_decision_engine.py \
  --primary-device mobile-4g --lcp-target-ms 2000 \
  --seo-dependent true --auth-walled false --team-size 5
```

Инструмент возвращает наиболее подходящий профиль, компромисс, занявший второе место (если он находится в пределах 15%), выбор стека, антишаблоны, которых следует избегать в этом профиле, и требуемые гейты CI.

Чтобы добавить пользовательский профиль (например, настройки внутреннего инструмента вашей организации по умолчанию): скопируйте `profiles/vite-spa.json` к `profiles/<your-org>.json` и настраивать `constraints` + `success_thresholds`.

---

## Карта композиции { #composition-map }

Этот скилл не переопределяет область применения, которой владеют специалисты высокого уровня. Она разветвляется на них. Видишь `references/composition_map.md` для получения полной таблицы маршрутизации. Ключевые вилки:

| Беспокойство | Раскошелиться на |
|---|---|
| Аудит WCAG, контрастность, программа для чтения с экрана | `engineering-team/skills/a11y-audit/` |
| Профилирование пакета + улучшение во время выполнения | `engineering/skills/performance-profiler/` |
| Кинематографическая посадка / скролл-сторителлинг | `engineering-team/skills/epic-design/` |
| Apple HIG (iOS / macOS / visionOS) | `product-team/skills/apple-hig-expert/` |
| Ревью перед совершением Карпатии | `engineering/karpathy-coder/` |
| Предполетный архитектурный гриль | `engineering/grill-me/` |

Тот `cs-frontend-engineer` агент управляет этими разветвлениями с помощью `context: fork`. Вызовите его у другого агента с помощью `Agent({subagent_type: "cs-frontend-engineer", prompt: "..."})` или через `/cs:frontend-review <your problem>`.

---

## Библиотека форсирующих вопросов (Мэтт Покок Грилл) { #forcing-question-library-matt-pocock-grill }

Прежде чем блокировать какой-либо фреймворк или принимать решение о рендеринге, ответьте на семь форсирующих вопросов в `references/forcing_questions.md` Дисциплина:

1. По одному вопросу за ход. Никакого связывания.
2. Всегда рекомендуйте ответ с цитируемым каноном.
3. Отслеживайте ответы в `/tmp/frontend-grill-<date>.md`.
4. Если сработает критерий уничтожения, остановитесь. Не возводите каркасы вокруг неразрешенного пробела.
5. После Q7 запустите `frontend_decision_engine.py` с семью ответами.

Краткое содержание:

1. Основное устройство + сеть?
2. Цель LCP в ms (и INP, CLS)?
3. RSC / SPA / SSR / SSG — выбирать и защищать?
4. Бюджет пакета JS для каждого маршрута?
5. Зависимый от SEO или защищенный от авторизации?
6. Дизайн-система - источник истины?
7. Цель WCAG + назван владелец a11y?

---

## Обращение к другим агентам и скиллам { #invocation-from-other-agents-and-skills }

Три поверхности:

1. **Слэш-команда:** `/cs:frontend-review <prompt>` — полный гриль + механизм принятия решений + маршрутизация состава.
2. **Агент-субагент:** `Agent({subagent_type: "cs-frontend-engineer", prompt: "..."})` — разветвляет контекст, возвращает дайджест из ≤ 200 слов.
3. **Прямой вызов инструмента:** `python scripts/frontend_decision_engine.py ...` — детерминированное совпадение профилей, когда известны входные данные.

Видишь `agents/engineering/cs-frontend-engineer.md` для полного контракта на вызов.
