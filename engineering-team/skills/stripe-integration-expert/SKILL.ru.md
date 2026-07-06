---
name: "stripe-integration-expert"
description: "Интеграция Stripe производственного уровня: подписки с пробными версиями и пропорциональной оплатой, единовременные платежи, выставление счетов на основе использования, сеансы оформления заказа, идемпотентные обработчики webhook, клиентский портал и выставление счетов-фактур. Обложки Next.js , Express и шаблоны Django. Используйте при первой интеграции Stripe, устранении проблем с надежностью webhook, переходе от другого поставщика платежей или добавлении выставления счетов на основе использования к существующему продукту подписки."
---

# Эксперт по интеграции Stripe { #stripe-integration-expert }

**Уровень:** МОЩНЫЙ  
**Категория:** Инженерная команда  
**Домен:** Инфраструктура платежей / выставления счетов

---

## Обзор { #overview }

Внедрите интеграцию Stripe производственного уровня: подписки с пробными версиями и пропорциональной оплатой, единовременные платежи, выставление счетов на основе использования, сеансы оформления заказа, идемпотентные обработчики webhook, клиентский портал и выставление счетов-фактур. Обложки Next.js , Express и шаблоны Django.

---

## Основные возможности { #core-capabilities }

- Управление жизненным циклом подписки (создание, обновление, понижение версии, отмена, пауза)
- Обработка пробных версий и отслеживание конверсий
- Расчет пропорциональности и заявка на получение кредита
- Выставление счетов на основе использования с фиксированной ценой
- Идемпотентные обработчики webhook с проверкой подписи
- Интеграция с клиентским порталом
- Создание счета-фактуры и доступ к PDF-файлам
- Полная настройка локального тестирования Stripe CLI

---

## Когда использовать { #when-to-use }

- Добавление выставления счетов за подписку в любое веб-приложение
- Внедрение обновлений плана/downgrades с пропорциональным распределением
- Выставление счетов на основе использования здания или места
- Отладка сбоев доставки webhook
- Переход с одной модели выставления счетов на другую

---

## Конечный автомат жизненного цикла подписки { #subscription-lifecycle-state-machine }

```
FREE_TRIAL ──paid──► ACTIVE ──cancel──► CANCEL_PENDING ──period_end──► CANCELED
     │                  │                                                    │
     │               downgrade                                            reactivate
     │                  ▼                                                    │
     │             DOWNGRADING ──period_end──► ACTIVE (lower plan)           │
     │                                                                        │
     └──trial_end without payment──► PAST_DUE ──payment_failed 3x──► CANCELED
                                          │
                                     payment_success
                                          │
                                          ▼
                                        ACTIVE
```

### Значения статуса подписки на базу данных: { #db-subscription-status-values }
`trialing | active | past_due | canceled | cancel_pending | paused | unpaid`

---

## Настройка клиента Stripe { #stripe-client-setup }

```typescript
// lib/stripe.ts
import Stripe from "stripe"

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-04-10",
  typescript: true,
  appInfo: {
    name: "myapp",
    version: "1.0.0",
  },
})

// Price IDs by plan (set in env)
export const PLANS = {
  starter: {
    monthly: process.env.STRIPE_STARTER_MONTHLY_PRICE_ID!,
    yearly: process.env.STRIPE_STARTER_YEARLY_PRICE_ID!,
    features: ["5 projects", "10k events"],
  },
  pro: {
    monthly: process.env.STRIPE_PRO_MONTHLY_PRICE_ID!,
    yearly: process.env.STRIPE_PRO_YEARLY_PRICE_ID!,
    features: ["Unlimited projects", "1M events"],
  },
} as const
```

---

## Сеанс оформления заказа (Next.js Маршрутизатор приложений) { #checkout-session-nextjs-app-router }

```typescript
// app/api/billing/checkout/route.ts
import { NextResponse } from "next/server"
import { stripe } from "@/lib/stripe"
import { getAuthUser } from "@/lib/auth"
import { db } from "@/lib/db"

export async function POST(req: Request) {
  const user = await getAuthUser()
  if (!user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })

  const { priceId, interval = "monthly" } = await req.json()

  // Get or create Stripe customer
  let stripeCustomerId = user.stripeCustomerId
  if (!stripeCustomerId) {
    const customer = await stripe.customers.create({
      email: user.email,
      name: "username-undefined"
      metadata: { userId: user.id },
    })
    stripeCustomerId = customer.id
    await db.user.update({ where: { id: user.id }, data: { stripeCustomerId } })
  }

  const session = await stripe.checkout.sessions.create({
    customer: stripeCustomerId,
    mode: "subscription",
    payment_method_types: ["card"],
    line_items: [{ price: priceId, quantity: 1 }],
    allow_promotion_codes: true,
    subscription_data: {
      trial_period_days: user.hasHadTrial ? undefined : 14,
      metadata: { userId: user.id },
    },
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { userId: user.id },
  })

  return NextResponse.json({ url: session.url })
}
```

---

## Обновление/понижение уровня подписки { #subscription-upgradedowngrade }

```typescript
// lib/billing.ts
export async function changeSubscriptionPlan(
  subscriptionId: string,
  newPriceId: string,
  immediate = false
) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId)
  const currentItem = subscription.items.data[0]

  if (immediate) {
    // Upgrade: apply immediately with proration
    return stripe.subscriptions.update(subscriptionId, {
      items: [{ id: currentItem.id, price: newPriceId }],
      proration_behavior: "always_invoice",
      billing_cycle_anchor: "unchanged",
    })
  } else {
    // Downgrade: apply at period end, no proration
    return stripe.subscriptions.update(subscriptionId, {
      items: [{ id: currentItem.id, price: newPriceId }],
      proration_behavior: "none",
      billing_cycle_anchor: "unchanged",
    })
  }
}

// Preview proration before confirming upgrade
export async function previewProration(subscriptionId: string, newPriceId: string) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId)
  const prorationDate = Math.floor(Date.now() / 1000)

  const invoice = await stripe.invoices.retrieveUpcoming({
    customer: subscription.customer as string,
    subscription: subscriptionId,
    subscription_items: [{ id: subscription.items.data[0].id, price: newPriceId }],
    subscription_proration_date: prorationDate,
  })

  return {
    amountDue: invoice.amount_due,
    prorationDate,
    lineItems: invoice.lines.data,
  }
}
```

---

## Полный обработчик Webhook (идемпотентный) { #complete-webhook-handler-idempotent }

```typescript
// app/api/webhooks/stripe/route.ts
import { NextResponse } from "next/server"
import { headers } from "next/headers"
import { stripe } from "@/lib/stripe"
import { db } from "@/lib/db"
import Stripe from "stripe"

// Processed events table to ensure idempotency
async function hasProcessedEvent(eventId: string): Promise<boolean> {
  const existing = await db.stripeEvent.findUnique({ where: { id: eventId } })
  return !!existing
}

async function markEventProcessed(eventId: string, type: string) {
  await db.stripeEvent.create({ data: { id: eventId, type, processedAt: new Date() } })
}

export async function POST(req: Request) {
  const body = await req.text()
  const signature = headers().get("stripe-signature")!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch (err) {
    console.error("Webhook signature verification failed:", err)
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 })
  }

  // Idempotency check
  if (await hasProcessedEvent(event.id)) {
    return NextResponse.json({ received: true, skipped: true })
  }

  try {
    switch (event.type) {
      case "checkout.session.completed":
        await handleCheckoutCompleted(event.data.object as Stripe.Checkout.Session)
        break

      case "customer.subscription.created":
      case "customer.subscription.updated":
        await handleSubscriptionUpdated(event.data.object as Stripe.Subscription)
        break

      case "customer.subscription.deleted":
        await handleSubscriptionDeleted(event.data.object as Stripe.Subscription)
        break

      case "invoice.payment_succeeded":
        await handleInvoicePaymentSucceeded(event.data.object as Stripe.Invoice)
        break

      case "invoice.payment_failed":
        await handleInvoicePaymentFailed(event.data.object as Stripe.Invoice)
        break

      default:
        console.log(`Unhandled event type: ${event.type}`)
    }

    await markEventProcessed(event.id, event.type)
    return NextResponse.json({ received: true })
  } catch (err) {
    console.error(`Error processing webhook ${event.type}:`, err)
    // Return 500 so Stripe retries — don't mark as processed
    return NextResponse.json({ error: "Processing failed" }, { status: 500 })
  }
}

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  if (session.mode !== "subscription") return
  
  const userId = session.metadata?.userId
  if (!userId) throw new Error("No userId in checkout session metadata")

  const subscription = await stripe.subscriptions.retrieve(session.subscription as string)
  
  await db.user.update({
    where: { id: userId },
    data: {
      stripeCustomerId: session.customer as string,
      stripeSubscriptionId: subscription.id,
      stripePriceId: subscription.items.data[0].price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
      subscriptionStatus: subscription.status,
      hasHadTrial: true,
    },
  })
}

async function handleSubscriptionUpdated(subscription: Stripe.Subscription) {
  const user = await db.user.findUnique({
    where: { stripeSubscriptionId: subscription.id },
  })
  if (!user) {
    // Look up by customer ID as fallback
    const customer = await db.user.findUnique({
      where: { stripeCustomerId: subscription.customer as string },
    })
    if (!customer) throw new Error(`No user found for subscription ${subscription.id}`)
  }

  await db.user.update({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      stripePriceId: subscription.items.data[0].price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
      subscriptionStatus: subscription.status,
      cancelAtPeriodEnd: subscription.cancel_at_period_end,
    },
  })
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  await db.user.update({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      stripeSubscriptionId: null,
      stripePriceId: null,
      stripeCurrentPeriodEnd: null,
      subscriptionStatus: "canceled",
    },
  })
}

async function handleInvoicePaymentFailed(invoice: Stripe.Invoice) {
  if (!invoice.subscription) return
  const attemptCount = invoice.attempt_count
  
  await db.user.update({
    where: { stripeSubscriptionId: invoice.subscription as string },
    data: { subscriptionStatus: "past_due" },
  })

  if (attemptCount >= 3) {
    // Send final dunning email
    await sendDunningEmail(invoice.customer_email!, "final")
  } else {
    await sendDunningEmail(invoice.customer_email!, "retry")
  }
}

async function handleInvoicePaymentSucceeded(invoice: Stripe.Invoice) {
  if (!invoice.subscription) return

  await db.user.update({
    where: { stripeSubscriptionId: invoice.subscription as string },
    data: {
      subscriptionStatus: "active",
      stripeCurrentPeriodEnd: new Date(invoice.period_end * 1000),
    },
  })
}
```

---

## Выставление счетов на основе использования { #usage-based-billing }

```typescript
// Report usage for metered subscriptions
export async function reportUsage(subscriptionItemId: string, quantity: number) {
  await stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
    quantity,
    timestamp: Math.floor(Date.now() / 1000),
    action: "increment",
  })
}

// Example: report API calls in middleware
export async function trackApiCall(userId: string) {
  const user = await db.user.findUnique({ where: { id: userId } })
  if (user?.stripeSubscriptionId) {
    const subscription = await stripe.subscriptions.retrieve(user.stripeSubscriptionId)
    const meteredItem = subscription.items.data.find(
      (item) => item.price.recurring?.usage_type === "metered"
    )
    if (meteredItem) {
      await reportUsage(meteredItem.id, 1)
    }
  }
}
```

---

## Клиентский портал { #customer-portal }

```typescript
// app/api/billing/portal/route.ts
import { NextResponse } from "next/server"
import { stripe } from "@/lib/stripe"
import { getAuthUser } from "@/lib/auth"

export async function POST() {
  const user = await getAuthUser()
  if (!user?.stripeCustomerId) {
    return NextResponse.json({ error: "No billing account" }, { status: 400 })
  }

  const portalSession = await stripe.billingPortal.sessions.create({
    customer: user.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/settings/billing`,
  })

  return NextResponse.json({ url: portalSession.url })
}
```

---

## Тестирование с помощью Stripe CLI { #testing-with-stripe-cli }

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local dev
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger specific events for testing
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed

# Test with specific customer
stripe trigger customer.subscription.updated \
  --override subscription:customer=cus_xxx

# View recent events
stripe events list --limit 10

# Test cards
# Success: 4242 4242 4242 4242
# Requires auth: 4000 0025 0000 3155
# Decline: 4000 0000 0000 9995
# Insufficient funds: 4000 0000 0000 9995
```

---

## Помощник по гейт-функции { #feature-gating-helper }

```typescript
// lib/subscription.ts
export function isSubscriptionActive(user: { subscriptionStatus: string | null, stripeCurrentPeriodEnd: Date | null }) {
  if (!user.subscriptionStatus) return false
  if (user.subscriptionStatus === "active" || user.subscriptionStatus === "trialing") return true
  // Grace period: past_due but not yet expired
  if (user.subscriptionStatus === "past_due" && user.stripeCurrentPeriodEnd) {
    return user.stripeCurrentPeriodEnd > new Date()
  }
  return false
}

// Middleware usage
export async function requireActiveSubscription() {
  const user = await getAuthUser()
  if (!isSubscriptionActive(user)) {
    redirect("/billing?reason=subscription_required")
  }
}
```

---

## Распространенные подводные камни { #common-pitfalls }

- ** Заказ на доставку Webhook не гарантирован ** — всегда выполняйте повторную выборку из Stripe API, никогда не доверяйте только данным о событиях для обновления базы данных
- **Веб-хуки с двойной обработкой** — Stripe повторяет попытку на 500; всегда используйте таблицу идемпотентности
- **Отслеживание пробных конверсий** — магазин `hasHadTrial: true` в базе данных для предотвращения злоупотреблений в ходе судебного разбирательства
- ** Сюрпризы с пропорциональным распределением ** — всегда просматривайте пропорциональное распределение перед обновлением; показывайте пользователю сумму перед подтверждением
- **Клиентский портал не настроен** — необходимо включить функции в Stripe дашборде в разделе Выставление счетов → Настройки клиентского портала
- **Отсутствуют метаданные при оформлении заказа** — всегда передаются `userId` в метаданных; без этого невозможно связать подписку с пользователем
