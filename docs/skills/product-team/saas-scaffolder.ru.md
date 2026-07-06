---
title: "Держатель строительных лесов SaaS { #saas-scaffolder } — Агентский скилл для продуктовых команд"
description: "Генерирует полный, готовый к производству шаблон SaaS-проекта, включая аутентификацию, схемы баз данных, интеграцию с биллингом, маршруты API и. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Держатель строительных лесов SaaS { #saas-scaffolder }

<div class="page-meta" markdown>
<span class="meta-badge">:material-lightbulb-outline: Продукт</span>
<span class="meta-badge">:material-identifier: `saas-scaffolder`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/product-team/skills/saas-scaffolder/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install product-skills</code>
</div>


**Уровень:** МОЩНЫЙ  
**Категория:** Команда разработчиков  
**Домен:** Разработка с полным стеком / Начальная загрузка проекта

---

## Формат ввода { #input-format }

```
Product: [name]
Description: [1-3 sentences]
Auth: nextauth | clerk | supabase
Database: neondb | supabase | planetscale
Payments: stripe | lemonsqueezy | none
Features: [comma-separated list]
```

---

## Вывод дерева файлов { #file-tree-output }

```
my-saas/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/page.tsx
│   │   ├── settings/page.tsx
│   │   ├── billing/page.tsx
│   │   └── layout.tsx
│   ├── (marketing)/
│   │   ├── page.tsx
│   │   ├── pricing/page.tsx
│   │   └── layout.tsx
│   ├── api/
│   │   ├── auth/[...nextauth]/route.ts
│   │   ├── webhooks/stripe/route.ts
│   │   ├── billing/checkout/route.ts
│   │   └── billing/portal/route.ts
│   └── layout.tsx
├── components/
│   ├── ui/
│   ├── auth/
│   │   ├── login-form.tsx
│   │   └── register-form.tsx
│   ├── dashboard/
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── stats-card.tsx
│   ├── marketing/
│   │   ├── hero.tsx
│   │   ├── features.tsx
│   │   ├── pricing.tsx
│   │   └── footer.tsx
│   └── billing/
│       ├── plan-card.tsx
│       └── usage-meter.tsx
├── lib/
│   ├── auth.ts
│   ├── db.ts
│   ├── stripe.ts
│   ├── validations.ts
│   └── utils.ts
├── db/
│   ├── schema.ts
│   └── migrations/
├── hooks/
│   ├── use-subscription.ts
│   └── use-user.ts
├── types/index.ts
├── middleware.ts
├── .env.example
├── drizzle.config.ts
└── next.config.ts
```

---

## Шаблоны ключевых компонентов { #key-component-patterns }

### Конфигурация аутентификации (NextAuth) { #auth-config-nextauth }

```typescript
// lib/auth.ts
import { NextAuthOptions } from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import { DrizzleAdapter } from "@auth/drizzle-adapter"
import { db } from "./db"

export const authOptions: NextAuthOptions = {
  adapter: DrizzleAdapter(db),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    session: async ({ session, user }) => ({
      ...session,
      user: {
        ...session.user,
        id: user.id,
        subscriptionStatus: user.subscriptionStatus,
      },
    }),
  },
  pages: { signIn: "/login" },
}
```

### Схема базы данных (Drizzle + NeonDB) { #database-schema-drizzle--neondb }

```typescript
// db/schema.ts
import { pgTable, text, timestamp, integer } from "drizzle-orm/pg-core"

export const users = pgTable("users", {
  id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
  name: text("name"),
  email: text("email").notNull().unique(),
  emailVerified: timestamp("emailVerified"),
  image: text("image"),
  stripeCustomerId: text("stripe_customer_id").unique(),
  stripeSubscriptionId: text("stripe_subscription_id"),
  stripePriceId: text("stripe_price_id"),
  stripeCurrentPeriodEnd: timestamp("stripe_current_period_end"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
})

export const accounts = pgTable("accounts", {
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  type: text("type").notNull(),
  provider: text("provider").notNull(),
  providerAccountId: text("provider_account_id").notNull(),
  refresh_token: text("refresh_token"),
  access_token: text("access_token"),
  expires_at: integer("expires_at"),
})
```

### Маршрут оформления заказа в полоску { #stripe-checkout-route }

```typescript
// app/api/billing/checkout/route.ts
import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { stripe } from "@/lib/stripe"
import { db } from "@/lib/db"
import { users } from "@/db/schema"
import { eq } from "drizzle-orm"

export async function POST(req: Request) {
  const session = await getServerSession(authOptions)
  if (!session?.user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })

  const { priceId } = await req.json()
  const [user] = await db.select().from(users).where(eq(users.id, session.user.id))

  let customerId = user.stripeCustomerId
  if (!customerId) {
    const customer = await stripe.customers.create({ email: session.user.email! })
    customerId = customer.id
    await db.update(users).set({ stripeCustomerId: customerId }).where(eq(users.id, user.id))
  }

  const checkoutSession = await stripe.checkout.sessions.create({
    customer: customerId,
    mode: "subscription",
    payment_method_types: ["card"],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?upgraded=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    subscription_data: { trial_period_days: 14 },
  })

  return NextResponse.json({ url: checkoutSession.url })
}
```

### Промежуточное программное обеспечение { #middleware }

```typescript
// middleware.ts
import { withAuth } from "next-auth/middleware"
import { NextResponse } from "next/server"

export default withAuth(
  function middleware(req) {
    const token = req.nextauth.token
    if (req.nextUrl.pathname.startsWith("/dashboard") && !token) {
      return NextResponse.redirect(new URL("/login", req.url))
    }
  },
  { callbacks: { authorized: ({ token }) => !!token } }
)

export const config = {
  matcher: ["/dashboard/:path*", "/settings/:path*", "/billing/:path*"],
}
```

### Шаблон переменных окружения { #environment-variables-template }

```bash
# .env.example
NEXT_PUBLIC_APP_URL=http://localhost:3000
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
NEXTAUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_PRO_PRICE_ID=price_...
```

---

## Чек-лист по строительным лесам (Scaffold) { #scaffold-checklist }

Следующие этапы должны быть выполнены по порядку. **Проверяйте в конце каждого этапа, прежде чем продолжить.**

### Фаза 1 — Основание { #phase-1--foundation }
- [ ] 1. Next.js инициализирован с помощью TypeScript и App Router
- [ ] 2. Tailwind CSS, настроенный с использованием пользовательских тематических токенов
- [ ] 3. тень/ui установлен и настроен
- [ ] 4. ESLint + настроен красивее
- [ ] 5. `.env.example` создан со всеми необходимыми переменными

✅ ** Проверка:** Запуск `npm run build` — не должно появляться ошибок машинописи или линта.  
🔧 ** Если сборка завершается неудачей:** Проверьте `tsconfig.json` пути, и все это затеняет/ui установлены одноранговые зависимости.

### Этап 2 — База данных { #phase-2--database }
- [ ] 6. Установлен и сконфигурирован Drizzle ORM
- [ ] 7. Написана схема (пользователи, учетные записи, сеансы, verification_tokens)
- [ ] 8. Сгенерированная и примененная первоначальная миграция
- [ ] 9. Синглтон клиента базы данных, экспортированный из `lib/db.ts`
- [ ] 10. Подключение к базе данных протестировано в локальной среде

✅ ** Проверка:** Запустите простую `db.select().from(users)` в тестовом скрипте — он должен возвращать пустой массив без выброса.  
🔧 **При сбое подключения к базе данных:** Проверьте `DATABASE_URL` формат включает в себя `?sslmode=require` для NeonDB/Supabase. Убедитесь, что миграция была применена с помощью `drizzle-kit push` (dev) или `drizzle-kit migrate` (толчок).

### Этап 3 — Аутентификация { #phase-3--authentication }
- [ ] 11. Установлен поставщик аутентификации (NextAuth / Clerk / Supabase)
- [ ] 12. Настроен поставщик OAuth (Google / GitHub)
- [ ] 13. Создан маршрут Auth API
- [ ] 14. Обратный вызов сеанса добавляет идентификатор пользователя и статус подписки
- [ ] 15. Промежуточное программное обеспечение защищает маршруты дашборда
- [ ] 16. Страницы входа в систему и регистрации, созданные с ошибочными состояниями

✅ ** Проверка:** Войдите в систему через OAuth, подтвердите, что пользователь сеанса имеет `id` и `subscriptionStatus`. Попытка получить доступ `/dashboard` без сеанса — вы должны быть перенаправлены на `/login`.
🔧 **Если в процессе производства возникают циклы выхода из системы:** Убедитесь, что `NEXTAUTH_SECRET` устанавливается и согласуется во всех развертываниях. Добавить `declare module "next-auth"` для расширения типов сеансов при появлении ошибок TypeScript.

### Этап 4 — Платежи { #phase-4--payments }
- [ ] 17. Клиент Stripe, инициализированный типами TypeScript
- [ ] 18. Создан маршрут сеанса оформления заказа
- [ ] 19. Создан маршрут клиентского портала
- [ ] 20. Обработчик Stripe webhook с проверкой подписи
- [ ] 21. Webhook идемпотентно обновляет статус подписки пользователя в базе данных

✅ ** Проверка:** Завершите проверку Stripe test с помощью `4242 4242 4242 4242` карточка. Подтверждаю `stripeSubscriptionId` записывается в базу данных. Воспроизведите `checkout.session.completed` событие webhook и подтвердите идемпотентность (никаких повторяющихся записей в базу данных).  
🔧 **При сбое подписи webhook:** Используйте `stripe listen --forward-to localhost:3000/api/webhooks/stripe` локально — никогда не кодируйте жестко необработанный секрет webhook. Проверить `STRIPE_WEBHOOK_SECRET` соответствует выходным данным прослушивателя.

### Фаза 5 — Пользовательский интерфейс { #phase-5--ui }
- [ ] 22. Целевая страница с героем, функциями, разделами ценообразования
- [ ] 23. Макет дашборда с боковой панелью и адаптивным заголовком
- [ ] 24. Страница выставления счета с указанием текущего тарифного плана и вариантов обновления
- [ ] 25. Страница настроек с формой обновления профиля и состояниями успеха

✅ ** Проверка:** Запуск `npm run build` для окончательной проверки производственной сборки. Пройдите по всем маршрутам вручную и убедитесь, что нет нарушенных макетов, отсутствующих данных сеанса или ошибок гидратации.

---

## Справочные файлы { #reference-files }

Для получения дополнительных указаний создайте следующие сопутствующие справочные файлы вместе с каркасом:

- **`CUSTOMIZATION.md`** — Поставщики авторизации, параметры базы данных, альтернативы ORM, поставщики платежей, темы пользовательского интерфейса и модели выставления счетов (за место, фиксированная ставка, на основе использования).
- **`PITFALLS.md`** — Распространенные режимы сбоя: отсутствует `NEXTAUTH_SECRET`, несоответствия секретов webhook, конфликты среды выполнения Edge с Drizzle, типы непродленных сеансов и различия в стратегии миграции между dev и prod.
- **`BEST_PRACTICES.md`** — Шаблон Stripe singleton, действия сервера для мутаций формы, идемпотентные обработчики webhook, `Suspense` границы для данных асинхронной дашборды, гейт-функция на стороне сервера с помощью `stripeCurrentPeriodEnd`, и ограничение скорости на аутентифицируемых маршрутах с помощью Upstash Redis + `@upstash/ratelimit`.
