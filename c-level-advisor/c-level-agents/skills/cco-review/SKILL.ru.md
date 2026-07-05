---
name: "cco-review"
description: "/cs:cco-ревью <плана> — опрос директора по работе с клиентами, одержимого удержанием, о любом плане, который касается удержания клиентов, сегментации, определения размера команды CS или найма команды CS. Используйте, когда общий объем удержания сокращается, перед утверждением численности персонала CSM или при принятии решения о том, какие сегменты клиентов сохранить или уволить."
---

# /cs:cco-ревью — CCO форсирует вопросы { #cscco-review--cco-forcing-questions }

**Команда:** `/cs:cco-review <plan>`

Главный исполнительный директор, одержимый идеей удержания персонала, подвергает испытанию любой план, касающийся качества обслуживания клиентов. Шесть вопросов перед любым заявлением об удержании, изменении сегментации, расширении команды CS или крупном найме CS.

## Когда запускать { #when-to-run }

- Перед любым описанием правления, содержащим регистрационный номер
- Прежде чем одобрить увеличение численности команды CS
- Перед повторным сегментированием клиентской базы или изменением определений уровней
- Перед запуском маркетинговой или пропагандистской программы для клиентов
- Перед крупным привлечением CS (CSM, AM, внедрение, маркетинг для клиентов)
- Когда NRR "отличный", но жалобы на отток от CSMS растут
- Прежде чем принимать решение о добавлении роли AM отдельно от CSM

## Шесть вопросов CCO { #the-six-cco-questions }

### 1. Каков общий коэффициент удержания персонала? { #1-whats-the-gross-retention-rate }
**Не NRR. Отвратительно.** NRR может скрыть протекающее ведро за расширением.
- GRR здоровый ≥ 90% на стадии роста, ≥ 95% в масштабе
- Если GRR < 85%, но NRR > 100%, продукт выходит из строя более чем у 15% клиентов; расширение маскирует сбой
- Бежать `retention_decomposition_analyzer.py`

### 2. Какова причина №1, по которой клиенты уходят? { #2-whats-the-1-reason-customers-leave }
** Если вы не можете назвать это, значит, вы не понимаете, что такое отток.**
- таксономия по 7 категориям: product_fit / competitor_loss / no_value_realized / pricing / champion_left / company_event / тактический сбой
- Предотвратимый отток = product_fit + no_value_realized + тактический сбой
- Если предотвратимый > 50%, у CS есть явный рычаг воздействия; если < 30%, отток носит структурный характер (ICP, рынок, конкуренция).

### 3. Каково среднее время достижения значения (TTV) по сегментам? { #3-whats-the-median-time-to-value-ttv-by-segment }
**Длинный TTV сигнализирует о различных проблемах в зависимости от сегмента.**
- Длинный TTV на низком уровне = несоответствие ICP; понижение рейтинга или уничтожение
- Длинный TTV на высоком уровне = онбординг нарушен; исправьте хэндофф менеджера внедрения
- TTV является ведущим показателем GRR

### 4. Какого клиента вы бы уволили сегодня? { #4-which-customer-would-you-fire-today }
**Если "нет" — ваша сегментация нарушена.**
- Некоторые аккаунты стоят больше, чем они зарабатывают (стоимость поддержки > 50% от ARR + низкий ICP fit)
- Бежать `customer_segmentation_designer.py` чтобы вывести на поверхность список убийств
- 3 пути для кандидатов на уничтожение: отказ от продления / понижение рейтинга до технического уровня / повышение цены до возмещения затрат

### 5. Каково соотношение ARR на CSM и является ли модель объединенной или именованной? { #5-whats-the-arr-per-csm-ratio-and-is-the-model-pooled-or-named }
**Неправильная модель расходует мощность впустую.**
- Стратегический: именной + исполнительный спонсор, $300 тыс.-$1 млн в год/CSM
- Предприятие: названо, $500 тыс.-$2 млн
- Средний рынок: объединенный, $2 млн-$5 млн
- Малый и средний бизнес: tech-touch, $5 млн+
- Бежать `cs_coverage_calculator.py` чтобы определить размер команды

### 6. Входит ли CS в ваш тарифный план и чем он отличается от плана продаж? { #6-is-cs-in-your-comp-plan-and-how-is-it-different-from-sales-comp }
**Несоосность является основным показателем неисправности CS.**
- CS comp: 70/30 базовый/переменный типичный
- Переменная: 50% общего удержания + 30% чистого удержания + 20% активности
- Анти-паттерн: компилируйте CSM на NPS — они играют в это
- Анти-паттерн: компилирующие CSM—системы такие же, как и продажи - они продают, а не обслуживают

## Воркфлоу { #workflow }

```bash
# 1. Retention decomposition (always start here)
python ../../../skills/chief-customer-officer-advisor/scripts/retention_decomposition_analyzer.py cohorts.json

# 2. Segmentation audit
python ../../../skills/chief-customer-officer-advisor/scripts/customer_segmentation_designer.py customers.json

# 3. Coverage sizing (if making CS team changes)
python ../../../skills/chief-customer-officer-advisor/scripts/cs_coverage_calculator.py book.json
```

## Выходной формат { #output-format }

```markdown
# CCO Review: <plan>
**Date:** YYYY-MM-DD

## The Decision Being Made
[one sentence — retention | segmentation | coverage | next hire]

## Retention (if applicable)
- GRR: X% (vs vanity NRR of Y%)
- Top churn driver: <category> at X% of churn
- Preventable churn: X% (CS-controllable)
- Leaky-bucket pattern? yes/no

## Segmentation (if applicable)
- Tier distribution: Strategic X / Enterprise X / Mid-market X / SMB X
- Kill list size: N customers (X% of customers, Y% of ARR)
- Upgrade candidates: N

## Coverage (if applicable)
- Current CSMs: N | Required now: M | Required 12mo: P
- Annual cost (12mo): $X
- Manager trigger fired: yes/no

## Org (if applicable)
- Next hire: <CSM | Support | AM | IM | CS Ops | Customer Marketing>
- Why this, not the alternative: <one line>
- Customer outcome unblocked: <specific>

## Verdict
🟢 SHIP | 🟡 SHARPEN | 🔴 BLOCK

## Next Steps
[3 concrete actions]
```

## Маршрутизация { #routing }

- `/cs:cpo-review` — если основной причиной оттока является product_fit или no_value_realized
- `/cs:cro-review` — если речь идет о математике расширения или выравнивании компа
- `/cs:cfo-review` — для обязательств по затратам на CS и удержания-влияние-на-выручку
- `cs-chro-advisor` агент — для найма сотрудников CS, комп, лестница
- `/cs:decide` — зарегистрируйте вердикт
- `/cs:freeze 30` — об изменениях в многолетнем плане CS comp

## Связанный { #related }

- Агент: [`cs-cco-advisor`](../../agents/cs-cco-advisor.md)
- Скилл: [`chief-customer-officer-advisor`](../../../skills/chief-customer-officer-advisor/SKILL.md)
- Смежный: `../../../../business-growth/` (тактическое выполнение CS)

---

**Версия:** 1.0.0
