---
title: "Создатель шаблонов электронной почты { #email-template-builder } — Агентский скилл и плагин Codex"
description: "Создавайте полноценные транзакционные почтовые системы: шаблоны электронной почты React, интеграция с поставщиками (повторная отправка, Postmark. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Создатель шаблонов электронной почты { #email-template-builder }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `email-template-builder`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/email-template-builder/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


**Уровень:** МОЩНЫЙ  
**Категория:** Инженерная команда  
**Домен:** Транзакционная электронная почта / коммуникационная инфраструктура

---

## Обзор { #overview }

Создавайте полноценные транзакционные почтовые системы: шаблоны электронной почты React, интеграцию с провайдером, сервер предварительного просмотра, поддержку i18n, темный режим, оптимизацию спама и отслеживание аналитики. Выведите готовый к работе код для повторной отправки, Postmark, SendGrid или AWS SES.

---

## Основные возможности { #core-capabilities }

- Шаблоны электронной почты React (приветствие, верификация, сброс пароля, счет-фактура, уведомление, дайджест)
- Шаблоны MJML для максимальной совместимости с почтовым клиентом
- Поддержка нескольких провайдеров с унифицированным интерфейсом отправки
- Локальный сервер предварительного просмотра с горячей перезагрузкой
- i18n/localization с набранными клавишами перевода
- Поддержка темного режима с использованием медиа-запросов
- Чек-лист по оптимизации количества спама для рассылки по электронной почте.
- Открытый/click отслеживание с параметрами UTM

---

## Когда использовать { #when-to-use }

- Настройка электронной почты для транзакций для нового продукта
- Переход с устаревшей системы электронной почты
- Добавление новых типов электронных писем (счет-фактура, дайджест, уведомление)
- Устранение проблем с доставкой электронной почты
- Внедрение i18n для шаблонов электронной почты

---

## Структура проекта { #project-structure }

```
emails/
├── components/
│   ├── layout/
│   │   ├── email-layout.tsx       # Base layout with brand header/footer
│   │   └── email-button.tsx       # CTA button component
│   ├── partials/
│   │   ├── header.tsx
│   │   └── footer.tsx
├── templates/
│   ├── welcome.tsx
│   ├── verify-email.tsx
│   ├── password-reset.tsx
│   ├── invoice.tsx
│   ├── notification.tsx
│   └── weekly-digest.tsx
├── lib/
│   ├── send.ts                    # Unified send function
│   ├── providers/
│   │   ├── resend.ts
│   │   ├── postmark.ts
│   │   └── ses.ts
│   └── tracking.ts                # UTM + analytics
├── i18n/
│   ├── en.ts
│   └── de.ts
└── preview/                       # Dev preview server
    └── server.ts
```

---

## Базовый макет электронной почты { #base-email-layout }

```tsx
// emails/components/layout/email-layout.tsx
import {
  Body, Container, Head, Html, Img, Preview, Section, Text, Hr, Font
} from "@react-email/components"

interface EmailLayoutProps {
  preview: string
  children: React.ReactNode
}

export function EmailLayout({ preview, children }: EmailLayoutProps) {
  return (
    <Html lang="en">
      <Head>
        <Font
          fontFamily="Inter"
          fallbackFontFamily="Arial"
          webFont={{ url: "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2", format: "woff2" }}
          fontWeight={400}
          fontStyle="normal"
        />
        {/* Dark mode styles */}
        <style>{`
          @media (prefers-color-scheme: dark) {
            .email-body { background-color: #0f0f0f !important; }
            .email-container { background-color: #1a1a1a !important; }
            .email-text { color: #e5e5e5 !important; }
            .email-heading { color: #ffffff !important; }
            .email-divider { border-color: #333333 !important; }
          }
        `}</style>
      </Head>
      <Preview>{preview}</Preview>
      <Body className="email-body" style={styles.body}>
        <Container className="email-container" style={styles.container}>
          {/* Header */}
          <Section style={styles.header}>
            <Img src="https://yourapp.com/logo.png" width={120} height={40} alt="MyApp" />
          </Section>
          
          {/* Content */}
          <Section style={styles.content}>
            {children}
          </Section>
          
          {/* Footer */}
          <Hr style={styles.divider} />
          <Section style={styles.footer}>
            <Text style={styles.footerText}>
              MyApp Inc. · 123 Main St · San Francisco, CA 94105
            </Text>
            <Text style={styles.footerText}>
              <a href="{{unsubscribe_url}}" style={styles.link}>Unsubscribe</a>
              {" · "}
              <a href="https://yourapp.com/privacy" style={styles.link}>Privacy Policy</a>
            </Text>
          </Section>
        </Container>
      </Body>
    </Html>
  )
}

const styles = {
  body: { backgroundColor: "#f5f5f5", fontFamily: "Inter, Arial, sans-serif" },
  container: { maxWidth: "600px", margin: "0 auto", backgroundColor: "#ffffff", borderRadius: "8px", overflow: "hidden" },
  header: { padding: "24px 32px", borderBottom: "1px solid #e5e5e5" },
  content: { padding: "32px" },
  divider: { borderColor: "#e5e5e5", margin: "0 32px" },
  footer: { padding: "24px 32px" },
  footerText: { fontSize: "12px", color: "#6b7280", textAlign: "center" as const, margin: "4px 0" },
  link: { color: "#6b7280", textDecoration: "underline" },
}
```

---

## Приветственное электронное письмо { #welcome-email }

```tsx
// emails/templates/welcome.tsx
import { Button, Heading, Text } from "@react-email/components"
import { EmailLayout } from "../components/layout/email-layout"

interface WelcomeEmailProps {
  name: "string"
  confirmUrl: string
  trialDays?: number
}

export function WelcomeEmail({ name, confirmUrl, trialDays = 14 }: WelcomeEmailProps) {
  return (
    <EmailLayout preview={`Welcome to MyApp, ${name}! Confirm your email to get started.`}>
      <Heading style={styles.h1}>Welcome to MyApp, {name}!</Heading>
      <Text style={styles.text}>
        We're excited to have you on board. You've got {trialDays} days to explore everything MyApp has to offer — no credit card required.
      </Text>
      <Text style={styles.text}>
        First, confirm your email address to activate your account:
      </Text>
      <Button href={confirmUrl} style={styles.button}>
        Confirm Email Address
      </Button>
      <Text style={styles.hint}>
        Button not working? Copy and paste this link into your browser:
        <br />
        <a href={confirmUrl} style={styles.link}>{confirmUrl}</a>
      </Text>
      <Text style={styles.text}>
        Once confirmed, you can:
      </Text>
      <ul style={styles.list}>
        <li>Connect your first project in 2 minutes</li>
        <li>Invite your team (free for up to 3 members)</li>
        <li>Set up Slack notifications</li>
      </ul>
    </EmailLayout>
  )
}

export default WelcomeEmail

const styles = {
  h1: { fontSize: "28px", fontWeight: "700", color: "#111827", margin: "0 0 16px" },
  text: { fontSize: "16px", lineHeight: "1.6", color: "#374151", margin: "0 0 16px" },
  button: { backgroundColor: "#4f46e5", color: "#ffffff", borderRadius: "6px", fontSize: "16px", fontWeight: "600", padding: "12px 24px", textDecoration: "none", display: "inline-block", margin: "8px 0 24px" },
  hint: { fontSize: "13px", color: "#6b7280" },
  link: { color: "#4f46e5" },
  list: { fontSize: "16px", lineHeight: "1.8", color: "#374151", paddingLeft: "20px" },
}
```

---

## Счет по электронной почте { #invoice-email }

```tsx
// emails/templates/invoice.tsx
import { Row, Column, Section, Heading, Text, Hr, Button } from "@react-email/components"
import { EmailLayout } from "../components/layout/email-layout"

interface InvoiceItem { description: string; amount: number }

interface InvoiceEmailProps {
  name: "string"
  invoiceNumber: string
  invoiceDate: string
  dueDate: string
  items: InvoiceItem[]
  total: number
  currency: string
  downloadUrl: string
}

export function InvoiceEmail({ name, invoiceNumber, invoiceDate, dueDate, items, total, currency = "USD", downloadUrl }: InvoiceEmailProps) {
  const formatter = new Intl.NumberFormat("en-US", { style: "currency", currency })

  return (
    <EmailLayout preview={`Invoice ${invoiceNumber} - ${formatter.format(total / 100)}`}>
      <Heading style={styles.h1}>Invoice #{invoiceNumber}</Heading>
      <Text style={styles.text}>Hi {name},</Text>
      <Text style={styles.text}>Here's your invoice from MyApp. Thank you for your continued support.</Text>

      {/* Invoice Meta */}
      <Section style={styles.metaBox}>
        <Row>
          <Column><Text style={styles.metaLabel}>Invoice Date</Text><Text style={styles.metaValue}>{invoiceDate}</Text></Column>
          <Column><Text style={styles.metaLabel}>Due Date</Text><Text style={styles.metaValue}>{dueDate}</Text></Column>
          <Column><Text style={styles.metaLabel}>Amount Due</Text><Text style={styles.metaValueLarge}>{formatter.format(total / 100)}</Text></Column>
        </Row>
      </Section>

      {/* Line Items */}
      <Section style={styles.table}>
        <Row style={styles.tableHeader}>
          <Column><Text style={styles.tableHeaderText}>Description</Text></Column>
          <Column><Text style={{ ...styles.tableHeaderText, textAlign: "right" }}>Amount</Text></Column>
        </Row>
        {items.map((item, i) => (
          <Row key={i} style={i % 2 === 0 ? styles.tableRowEven : styles.tableRowOdd}>
            <Column><Text style={styles.tableCell}>{item.description}</Text></Column>
            <Column><Text style={{ ...styles.tableCell, textAlign: "right" }}>{formatter.format(item.amount / 100)}</Text></Column>
          </Row>
        ))}
        <Hr style={styles.divider} />
        <Row>
          <Column><Text style={styles.totalLabel}>Total</Text></Column>
          <Column><Text style={styles.totalValue}>{formatter.format(total / 100)}</Text></Column>
        </Row>
      </Section>

      <Button href={downloadUrl} style={styles.button}>Download PDF Invoice</Button>
    </EmailLayout>
  )
}

export default InvoiceEmail

const styles = {
  h1: { fontSize: "24px", fontWeight: "700", color: "#111827", margin: "0 0 16px" },
  text: { fontSize: "15px", lineHeight: "1.6", color: "#374151", margin: "0 0 12px" },
  metaBox: { backgroundColor: "#f9fafb", borderRadius: "8px", padding: "16px", margin: "16px 0" },
  metaLabel: { fontSize: "12px", color: "#6b7280", fontWeight: "600", textTransform: "uppercase" as const, margin: "0 0 4px" },
  metaValue: { fontSize: "14px", color: "#111827", margin: 0 },
  metaValueLarge: { fontSize: "20px", fontWeight: "700", color: "#4f46e5", margin: 0 },
  table: { width: "100%", margin: "16px 0" },
  tableHeader: { backgroundColor: "#f3f4f6", borderRadius: "4px" },
  tableHeaderText: { fontSize: "12px", fontWeight: "600", color: "#374151", padding: "8px 12px", textTransform: "uppercase" as const },
  tableRowEven: { backgroundColor: "#ffffff" },
  tableRowOdd: { backgroundColor: "#f9fafb" },
  tableCell: { fontSize: "14px", color: "#374151", padding: "10px 12px" },
  divider: { borderColor: "#e5e5e5", margin: "8px 0" },
  totalLabel: { fontSize: "16px", fontWeight: "700", color: "#111827", padding: "8px 12px" },
  totalValue: { fontSize: "16px", fontWeight: "700", color: "#111827", textAlign: "right" as const, padding: "8px 12px" },
  button: { backgroundColor: "#4f46e5", color: "#fff", borderRadius: "6px", padding: "12px 24px", fontSize: "15px", fontWeight: "600", textDecoration: "none" },
}
```

---

## Единая функция отправки { #unified-send-function }

```typescript
// emails/lib/send.ts
import { Resend } from "resend"
import { render } from "@react-email/render"
import { WelcomeEmail } from "../templates/welcome"
import { InvoiceEmail } from "../templates/invoice"
import { addTrackingParams } from "./tracking"

const resend = new Resend(process.env.RESEND_API_KEY)

type EmailPayload =
  | { type: "welcome"; props: Parameters<typeof WelcomeEmail>[0] }
  | { type: "invoice"; props: Parameters<typeof InvoiceEmail>[0] }

export async function sendEmail(to: string, payload: EmailPayload) {
  const templates = {
    welcome: { component: WelcomeEmail, subject: "Welcome to MyApp — confirm your email" },
    invoice: { component: InvoiceEmail, subject: `Invoice from MyApp` },
  }

  const template = templates[payload.type]
  const html = render(template.component(payload.props as any))
  const trackedHtml = addTrackingParams(html, { campaign: payload.type })

  const result = await resend.emails.send({
    from: "MyApp <hello@yourapp.com>",
    to,
    subject: template.subject,
    html: trackedHtml,
    tags: [{ name: "email-type", value: payload.type }],
  })

  return result
}
```

---

## Настройка сервера предварительного просмотра { #preview-server-setup }

```typescript
// package.json scripts
{
  "scripts": {
    "email:dev": "email dev --dir emails/templates --port 3001",
    "email:build": "email export --dir emails/templates --outDir emails/out"
  }
}

// Run: npm run email:dev
// Opens: http://localhost:3001
// Shows all templates with live preview and hot reload
```

---

## поддержка i18n { #i18n-support }

```typescript
// emails/i18n/en.ts
export const en = {
  welcome: {
    preview: (name: string) => `Welcome to MyApp, ${name}!`,
    heading: (name: string) => `Welcome to MyApp, ${name}!`,
    body: (days: number) => `You've got ${days} days to explore everything.`,
    cta: "Confirm Email Address",
  },
}

// emails/i18n/de.ts
export const de = {
  welcome: {
    preview: (name: string) => `Willkommen bei MyApp, ${name}!`,
    heading: (name: string) => `Willkommen bei MyApp, ${name}!`,
    body: (days: number) => `Du hast ${days} Tage Zeit, alles zu erkunden.`,
    cta: "E-Mail-Adresse bestätigen",
  },
}

// Usage in template
import { en, de } from "../i18n"
const t = locale === "de" ? de : en
```

---

## Чек-лист по оптимизации количества спама для рассылки по электронной почте. { #spam-score-optimization-checklist }

- [ ] В домене отправителя настроены записи SPF, DKIM и DMARC
- [ ] From address использует ваш собственный домен (не gmail.com/hotmail.com)
- [ ] Строка темы не более 50 символов, без заглавных букв, без "БЕСПЛАТНО!!!"
- [ ] Соотношение текста к изображению: не менее 60% текста
- [ ] Обычная текстовая версия включена вместе с HTML
- [ ] Ссылка для отказа от подписки в каждом маркетинговом электронном письме (CAN-СПАМ, GDPR)
- [ ] Никаких сокращений URL—адресов - используйте полные фирменные ссылки
- [ ] Никаких предупреждающих слов: "гарантия", "без риска", "предложение ограничено по времени" в теме
- [ ] Один CTA для каждого электронного письма — нет 5 разных кнопок
- [ ] Изображение с измененным текстом на каждом изображении
- [ ] HTML проверяется — нет неработающих тегов
- [ ] Протестируйте с помощью Mail-Tester.com перед первой отправкой (цель: 9+/10)

---

## Отслеживание аналитики { #analytics-tracking }

```typescript
// emails/lib/tracking.ts
interface TrackingParams {
  campaign: string
  medium?: string
  source?: string
}

export function addTrackingParams(html: string, params: TrackingParams): string {
  const utmString = new URLSearchParams({
    utm_source: params.source ?? "email",
    utm_medium: params.medium ?? "transactional",
    utm_campaign: params.campaign,
  }).toString()

  // Add UTM params to all links in the email
  return html.replace(/href="(https?:\/\/[^"]+)"/g, (match, url) => {
    const separator = url.includes("?") ? "&" : "?"
    return `href="${url}${separator}${utmString}"`
  })
}
```

---

## Распространенные подводные камни { #common-pitfalls }

- **Требуются встроенные стили ** — большинство почтовых клиентов удаляют `<head>` стили; React Email обрабатывает это
- ** Максимальная ширина 600 пикселей ** — все, что шире, разрывается на мобильном Gmail
- **Нет гибкого ящика/grid** — использовать `<Row>` и `<Column>` из react-email, а не из CSS-сетки
- **Медиа—запросы в темном режиме** - необходимо использовать `!important` чтобы переопределить встроенные стили
- ** Отсутствует обычный текст ** — у всех основных поставщиков есть поле с простым текстом; всегда заполняйте его
- ** Транзакционный против маркетингового ** — используйте отдельные отправляющие домены / IP-адреса для защиты доступности доставки
