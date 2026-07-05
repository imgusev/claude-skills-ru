---
name: "contract-and-proposal-writer"
description: "Создавайте профессиональные деловые документы, ориентированные на юрисдикцию: внештатные контракты, проектные предложения, SOW, NDA и MSA. Структурированный вывод Markdown с инструкциями по преобразованию в docx. Распространяется на юрисдикции США (Делавэр), ЕС (GDPR), Великобритании и DACH (законодательство Германии). Не заменяет юрисконсульта — используйте в качестве надежной отправной точки. Используйте при составлении контракта с фрилансером, подготовке предложения для клиента, написании резюме для нового задания или подготовке соглашения о неразглашении перед публикацией конфиденциальных материалов."
---

# Составитель контрактов и предложений { #contract--proposal-writer }

**Уровень:** МОЩНЫЙ  
**Категория:** Рост бизнеса  
**Область применения:** Юридические документы, Развитие бизнеса, Отношения с клиентами

---

## Обзор { #overview }

Создавайте профессиональные деловые документы, ориентированные на юрисдикцию: внештатные контракты, проектные предложения, SOW, NDA и MSA. Выводит структурированный Markdown с инструкциями по преобразованию в docx. Распространяется на юрисдикции США (Делавэр), ЕС (GDPR), Великобритании и DACH (законодательство Германии).

** Не заменяет юрисконсульта.** Используйте эти шаблоны в качестве надежной отправной точки; ревью с адвокатом по важным или сложным делам.

---

## Основные возможности { #core-capabilities }

- Контракты на внештатную разработку (фиксированная цена и почасовая оплата)
- Проектные предложения с разбивкой по срокам/бюджету
- Отчеты о проделанной работе (SOW) с матрицей конечных результатов
- NDA (взаимные и односторонние)
- Соглашения о генеральном обслуживании (MSA)
- Положения, касающиеся конкретной юрисдикции (США/ЕС/Великобритания/DACH)
- Дополнения к GDPR по обработке данных (EU/DACH)

---

## Ссылка на ключевые положения { #key-clauses-reference }

| Оговорка | Варианты |
|--------|---------|
| Условия оплаты | Нетто-30, ежемесячный аванс с учетом этапов |
| Владение интеллектуальной собственностью | Работа по найму (США), переуступка (ЕС/Великобритания), возврат лицензии |
| Предел ответственности | 1-кратная стоимость контракта (стандартная), 3-кратная (высокорисковая) |
| Прекращение действия | По причине (14-дневное лечение), для удобства (уведомление за 30/60/90 дней) |
| Конфиденциальность | срок от 2 до 5 лет, бессрочный для коммерческой тайны |
| Гарантия | Отказ от ответственности "как есть", ограниченная гарантия на исправление в течение 30/90 дней |
| Разрешение споров | Арбитраж (AAA/ICC), суды (в зависимости от юрисдикции) |

---

## Когда использовать { #when-to-use }

- Начинаю работу с новым клиентом и нуждаюсь в быстром заключении контракта
- Клиент запрашивает предложение с указанием цены и сроков
- Партнерство или отношения с поставщиком, требующие MSA
- Защита IP-адреса или конфиденциальной информации с помощью NDA
- Проект ЕС/DACH, требующий соблюдения положений о данных, соответствующих GDPR

---

## Воркфлоу { #workflow }

### 1. Соберите требования { #1-gather-requirements }

Спросите пользователя:

    1. Тип документа? (контракт / предложение / SOW / NDA / MSA)
    2. Юрисдикция? (США-Делавэр / ЕС / Великобритания / DACH)
    3. Тип взаимодействия? (фиксированная цена / почасовая оплата / предварительный гонорар)
    4. Вечеринки? (имена, должности, деловые адреса)
    5. Краткое описание сферы применения? (1-3 предложения)
    6. Общая стоимость или почасовая ставка?
    7. Дата начала / окончания или продолжительность?
    8. Особые требования? (Присвоение IP-адреса, white-label, субподрядчики)

### 2. Выберите шаблон { #2-select-template }

| Тип | Юрисдикция | Шаблон |
|------|-------------|----------|
| Исправлен контракт разработчика | Любой | Шаблон A |
| Гонорар консультанта | Любой | Шаблон B |
| Партнерство SaaS | Любой | Шаблон C |
| NDA взаимный | США/ЕС/Великобритания/ДАЧ | NDA-M |
| NDA односторонний | США/ЕС/Великобритания/ДАЧ | NDA-ПОТОК |
| СЕЯТЬ | Любой | База для свиноматок |

### 3. Сгенерируйте и заполните { #3-generate--fill }

Заполнить все [ЗАКЛЮЧЕННЫЕ В КВАДРАТНЫЕ скобки] заполнители. Отметьте отсутствующие данные как "ОБЯЗАТЕЛЬНЫЕ".

### 4. Преобразовать в DOCX { #4-convert-to-docx }

```bash
# Install pandoc
brew install pandoc        # macOS
apt install pandoc         # Ubuntu

# Basic conversion
pandoc contract.md -o contract.docx \
  --reference-doc=reference.docx \
  -V geometry:margin=1in

# With numbered sections (legal style)
pandoc contract.md -o contract.docx \
  --number-sections \
  -V documentclass=article \
  -V fontsize=11pt

# With custom company template
pandoc contract.md -o contract.docx \
  --reference-doc=company-template.docx
```

---

## Примечания к юрисдикции { #jurisdiction-notes }

### США (Делавэр) { #us-delaware }
- Применимое право: Штат Делавэр
- Применяется доктрина работы по найму (Закон об авторском праве 101)
- Арбитраж: Коммерческие правила AAA
- Неконкурентоспособность: подлежит исполнению в разумных пределах/сроки

### ЕС (GDPR) { #eu-gdpr }
- При обработке персональных данных должно быть включено дополнение к обработке данных
- В некоторых государствах-членах для присвоения IP-адреса требуется отдельный письменный акт
- Арбитраж: ICC или местная палата

### Великобритания (после Brexit) { #uk-post-brexit }
- Регулируется английским законодательством
- ИС: Закон о патентах 1977 года / CDPA 1988
- Арбитраж: Регламент LCIA
- Данные: GDPR Великобритании (эквивалент после Brexit)

### ДАХ (Германия / Австрия / Швейцария) { #dach-germany--austria--switzerland }
- BGB (Buergerliches Gesetzbuch) регулирует контракты
- Требование к письменной форме для определенных положений (пункт 126 BGB)
- IP: Автор всегда сохраняет личные неимущественные права; должен явно передать Nutzungsrechte
- Не участвует в соревнованиях: максимум 2 года, требуется компенсация (пункт 74 HGB)
- Юрисдикция: Суды Германии (Landgericht) или арбитраж DIS
- DSGVO (внедрение GDPR) обязательно для обработки персональных данных
- Kuendigungsfristen: действуют установленные законом сроки уведомления

---

## Шаблон A: Контракт веб-разработчика с фиксированной ценой { #template-a-web-dev-fixed-price-contract }

```markdown
# SOFTWARE DEVELOPMENT AGREEMENT

**Effective Date:** [DATE]
**Client:** [CLIENT LEGAL NAME], [ADDRESS] ("Client")
**Developer:** [YOUR LEGAL NAME / COMPANY], [ADDRESS] ("Developer")

---

## 1. SERVICES

Developer agrees to design, develop, and deliver:

**Project:** [PROJECT NAME]
**Description:** [1-3 sentence scope]

**Deliverables:**
- [Deliverable 1] due [DATE]
- [Deliverable 2] due [DATE]
- [Deliverable 3] due [DATE]

## 2. PAYMENT

**Total Fee:** [CURRENCY] [AMOUNT]

| Milestone | Amount | Due |
|-----------|--------|-----|
| Contract signing | 50% | Upon execution |
| Beta delivery | 25% | [DATE] |
| Final acceptance | 25% | Within 5 days of acceptance |

Late payments accrue interest at 1.5% per month.
Client has [10] business days to accept or reject deliverables in writing.

## 3. INTELLECTUAL PROPERTY

Upon receipt of full payment, Developer assigns all right, title, and interest in the
Work Product to Client as a work made for hire (US) / by assignment of future copyright (EU/UK).

Developer retains the right to display Work Product in portfolio unless Client
requests confidentiality in writing within [30] days of delivery.

Pre-existing IP (tools, libraries, frameworks) remains Developer's property.
Developer grants Client a perpetual, royalty-free license to use pre-existing IP
as embedded in the Work Product.

## 4. CONFIDENTIALITY

Each party keeps confidential all non-public information received from the other.
This obligation survives termination for [3] years.

## 5. WARRANTIES

Developer warrants Work Product will substantially conform to specifications for
[90] days post-delivery. Developer will fix material defects at no charge during
this period. EXCEPT AS STATED, WORK PRODUCT IS PROVIDED "AS IS."

## 6. LIABILITY

Developer's total liability shall not exceed total fees paid under this Agreement.
Neither party liable for indirect, incidental, or consequential damages.

## 7. TERMINATION

For Cause: Either party may terminate if the other materially breaches and fails
to cure within [14] days of written notice.

For Convenience: Client may terminate with [30] days written notice and pay for
all work completed plus [10%] of remaining contract value.

## 8. DISPUTE RESOLUTION

US: Binding arbitration under AAA Commercial Rules, [CITY], Delaware law.
EU/DACH: ICC / DIS arbitration, [CITY]. German / English law.
UK: LCIA Rules, London. English law.

## 9. GENERAL

- Entire Agreement: Supersedes all prior discussions.
- Amendments: Must be in writing, signed by both parties.
- Independent Contractor: Developer is not an employee of Client.

---

CLIENT: _________________________ Date: _________
[CLIENT NAME], [TITLE]

DEVELOPER: _________________________ Date: _________
[YOUR NAME], [TITLE]
```

---

## Шаблон B: Ежемесячный гонорар за консультацию { #template-b-monthly-consulting-retainer }

```markdown
# CONSULTING RETAINER AGREEMENT

**Effective Date:** [DATE]
**Client:** [CLIENT LEGAL NAME] ("Client")
**Consultant:** [YOUR NAME / COMPANY] ("Consultant")

---

## 1. SERVICES

Consultant provides [DOMAIN, e.g., "CTO advisory and technical architecture"] services.

**Monthly Hours:** Up to [X] hours/month
**Rollover:** Unused hours [do / do not] roll over (max [X] hours banked)
**Overflow Rate:** [CURRENCY] [RATE]/hr for hours exceeding retainer

## 2. FEES

**Monthly Retainer:** [CURRENCY] [AMOUNT], due on the 1st of each month.
**Payment Method:** Bank transfer / Stripe / SEPA direct debit
**Late Payment:** 2% monthly interest after [10]-day grace period.

## 3. TERM AND TERMINATION

**Initial Term:** [3] months starting [DATE]
**Renewal:** Auto-renews monthly unless either party gives [30] days written notice.
**Immediate termination:** For material breach uncured after [7] days notice.

On termination, Consultant delivers all work in progress within [5] business days.

## 4. INTELLECTUAL PROPERTY

Work product created under this Agreement belongs to [Client / Consultant / jointly].
Advisory output (recommendations, analyses) are Client property upon full payment.

## 5. EXCLUSIVITY

[OPTION A - Non-exclusive:]
This Agreement is non-exclusive. Consultant may work with other clients.

[OPTION B - Partial exclusivity:]
Consultant will not work with direct competitors of Client during the term
and [90] days thereafter.

## 6. CONFIDENTIALITY AND DATA PROTECTION

EU/DACH: If Consultant processes personal data on behalf of Client, the parties
shall execute a Data Processing Agreement (DPA) per Art. 28 GDPR.

## 7. LIABILITY

Consultant's aggregate liability is capped at [3x] the fees paid in the [3] months
preceding the claim.

---

Signatures as above.
```

---

## Шаблон C: Соглашение о партнерстве SaaS { #template-c-saas-partnership-agreement }

```markdown
# SAAS PARTNERSHIP AGREEMENT

**Effective Date:** [DATE]
**Provider:** [NAME], [ADDRESS]
**Partner:** [NAME], [ADDRESS]

---

## 1. PURPOSE

Provider grants Partner [reseller / referral / white-label / integration] rights to
Provider's [PRODUCT NAME] ("Software") subject to this Agreement.

## 2. PARTNERSHIP TYPE

[ ] Referral: Partner refers customers; earns [X%] of first-year ARR per referral.
[ ] Reseller: Partner resells licenses; earns [X%] discount off list price.
[ ] White-label: Partner rebrands Software; pays [AMOUNT]/month platform fee.
[ ] Integration: Partner integrates Software via API; terms in Exhibit A.

## 3. REVENUE SHARE

| Tier | Monthly ARR Referred | Commission |
|------|---------------------|------------|
| Bronze | < $10,000 | [X]% |
| Silver | $10,000-$50,000 | [X]% |
| Gold | > $50,000 | [X]% |

Payout: Net-30 after month close, minimum $[500] threshold.

## 4. INTELLECTUAL PROPERTY

Each party retains all IP in its own products. No implied licenses.
Partner may use Provider's marks per Provider's Brand Guidelines (Exhibit B).

## 5. DATA AND PRIVACY

Each party is an independent data controller for its own customers.
Joint processing requires a separate DPA (Exhibit C - EU/DACH projects).

## 6. TERM

Initial: [12] months. Renews annually unless [90]-day written notice given.
Termination for Cause: [30]-day cure period for material breach.

## 7. LIMITATION OF LIABILITY

Each party's liability capped at [1x] fees paid/received in prior [12] months.
Mutual indemnification for IP infringement claims from own products.

---

Signatures, exhibits, and governing law per applicable jurisdiction.
```

---

## Дополнение к GDPR об обработке данных (блок положений ЕС/DACH) { #gdpr-data-processing-addendum-eudach-clause-block }

```markdown
## DATA PROCESSING ADDENDUM (Art. 28 GDPR)

Controller: [CLIENT NAME]
Processor: [CONTRACTOR NAME]

### Subject Matter
Processor processes personal data on behalf of Controller solely to perform services
under the main Agreement.

### Categories of Data Subjects
[e.g., end users, employees, customers]

### Categories of Personal Data
[e.g., names, email addresses, usage data]

### Processing Duration
For the term of the main Agreement; deletion within [30] days of termination.

### Processor Obligations
- Process data only on Controller's documented instructions
- Ensure persons authorized to process have committed to confidentiality
- Implement technical and organizational measures per Art. 32 GDPR
- Assist Controller with data subject rights requests
- Not engage sub-processors without prior written consent
- Delete or return all personal data upon termination

### Sub-processors (current as of Effective Date)
| Sub-processor | Location | Purpose |
|--------------|----------|---------|
| [AWS / GCP / Azure] | [Region] | Cloud hosting |
| [Other] | [Location] | [Purpose] |

### Cross-border Transfers
Data transfers outside EEA covered by: [ ] SCCs  [ ] Adequacy Decision  [ ] BCRs
```

---

## Распространенные подводные камни { #common-pitfalls }

1. **Отсутствует язык присвоения IP-адресов** - одного "работа по найму" недостаточно в ЕС; требуется явное присвоение Nutzungsrechte в DACH
2. ** Расплывчатые критерии принятия ** - Всегда определяйте, что означает "принято" (письменное согласие, X дней для отклонения)
3. ** Нет процесса заказа на изменение** - Масштабирование убивает проекты с фиксированной ценой; добавьте предложение для работ, выходящих за рамки проекта.
4. **Несоответствие юрисдикции** - Выбор законодательства штата Делавэр для проекта, ориентированного только на Германию, создает проблемы с правоприменением
5. ** Отсутствует ограничение ответственности ** - Без ограничения одна ошибка может привести к неограниченному ущербу
6. **Устные поправки** - Контракты, измененные устно, трудно привести в исполнение; всегда требуются письменные поправки

---

## Лучшие практики { #best-practices }

- Используйте ** поэтапные платежи ** свыше 30 нетто для проектов стоимостью более 10 тысяч долларов - снижает риск движения денежных средств
- Для ЕС/DACH: всегда проверяйте, требуется ли DPA (любые личные данные = да)
- Для DACH: явно включите **Schriftformklausel** (предложение письменной формы)
- Добавьте оговорку о ** форс-мажорных обстоятельствах** для всего, что длится более 3 месяцев
- Для постоянных клиентов: определите SLA по времени отклика (например, 4 часа срочно / 24 часа нормально).
- Храните шаблоны в системе управления версиями; отслеживайте изменения с помощью `git diff`
- Ежегодно проводите ревью - законы меняются, особенно толкования применения GDPR
- Для NDA: всегда указывайте возврат/уничтожение конфиденциальных материалов при прекращении действия
