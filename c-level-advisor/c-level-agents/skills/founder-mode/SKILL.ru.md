---
name: "founder-mode"
description: "/cs:режим основателя <вопрос> — автоматически перенаправляет любой вопрос основателя нужному консультанту C-роли или в /cs:зал заседаний для многоцелевых тем. Точка входа с единой командой. Используйте, когда основатель задает какой—либо стратегический вопрос, не зная, какой советник или команда подходит - например, "давление на взлетно-посадочную полосу" направляется финансовому директору, "общее снижение удержания" - генеральному директору."
---

# /cs: режим основателя — Автоматический маршрутизатор { #csfounder-mode--the-auto-router }

**Команда:** `/cs:founder-mode <question>`

Единственная команда, которую должен помнить основатель. Автоматически направляет вопрос к нужной C-роли или триггеру `/cs:boardroom` если многоцелевой.

Это команда—убийца** - ответ на вопрос "Я не знаю, какую слэш-команду использовать". Введите вопрос; система определит номер.

## Логика маршрутизации { #routing-logic }

Маршрутизатор (через `cs-chief-of-staff`) соответствует ли ключевое слово + намерение:

| Рассматриваемый сигнал | Маршрут |
|---|---|
| ожог, взлетно-посадочная полоса, сбор средств, разбавление, модель, LTV, CAC | `cs-cfo-advisor` |
| пайплайн, коэффициент выигрыша, прогноз, квота, рампа, динамика продаж | `cs-cro-advisor` |
| позиционирование, ICP, сообщение, бренд, канал, кампания | `cs-cmo-advisor` |
| дорожная карта, PMF, JTBD, Северная звезда, РАЙС, убийство | `cs-cpo-advisor` |
| частота вращения, OKR, система показателей, DRI, операционная система, ритм | `cs-coo-advisor` |
| наем, вознаграждение, лестница, уровень, выбытие, eNPS, справедливость | `cs-chro-advisor` |
| безопасность, угроза, нарушение, соответствие требованиям, аудит, SOC 2 | `cs-ciso-advisor` |
| архитектура, масштабирование, технический долг, SLO, задержка | `cs-cto-advisor` |
| контракт, IP, срок действия, регулирующий орган, лицензия | `cs-general-counsel-advisor` |
| удержание, GRR, NRR, отток, успех клиентов, CSM, время окупаемости, обновления | `cs-cco-advisor` |
| обучающие данные, права на данные, согласие, ресурс данных, хранилище, домик на озере, сетка данных | `cs-cdo-advisor` |
| выбор модели, оценка, галлюцинация, риск ИИ, закон ЕС об ИИ, тонкая настройка, сборка или покупка ИИ | `cs-caio-advisor` |
| DORA, время цикла, частота деплою, воронка найма персонала, топология команды, пропускная способность доставки | `cs-vpe-advisor` |
| стратегия, видение, правление, слияния и поглощения, повышение, выход | `cs-ceo-advisor` |
| **2+ сигнала от разных ролей** | `/cs:boardroom` |
| **неоднозначный** | `/cs:office-hours` сначала, затем проложите маршрут |

## Воркфлоу { #workflow }

1. Проанализируйте вопрос на предмет ролевых сигналов
2. Если только одна роль: вызовите этот cs-* агент напрямую
3. Если 2+ роли: создайте краткое описание с помощью `/cs:brief` и триггер `/cs:boardroom`
4. Если неоднозначно / нет совпадения сигналов: триггер `/cs:office-hours` чтобы заставить основателя затачивать
5. Регистрируйте решение о маршрутизации (необработанный уровень) с помощью `decision-logger`

## Выход { #output }

Маршрутизатор выдает один из трех ответов:

### Маршрут с одной ролью { #single-role-route }
```
**Routing:** cs-cfo-advisor
**Why:** Question hits burn rate and unit economics.
**Next:** Invoking cs-cfo-advisor with company-context loaded.

[Advisor's response follows]
```

### Многоцелевой маршрут { #multi-role-route }
```
**Routing:** /cs:boardroom
**Why:** Question touches CFO + CMO + CPO (pricing change has finance, positioning, and product implications).
**Next:** Building brief via /cs:brief, then running boardroom.

Brief saved: ~/.claude/briefs/2026-05-12-pricing-v3.md
Run: /cs:boardroom ~/.claude/briefs/2026-05-12-pricing-v3.md
```

### Неоднозначно → часы работы офиса { #ambiguous--office-hours }
```
**Routing:** /cs:office-hours
**Why:** Question is too broad ("should we grow faster?"). Need framing before any advisor can help.
**Next:** Six-question intake.

[Office hours questions follow]
```

## Почему это убийственная команда { #why-this-is-the-killer-command }

gstack требует, чтобы основатель знал все 23 слэш-команды и выбрал правильную. Это когнитивный налог. `/cs:founder-mode` сводит это к единице — система выбирает. Это также то место, где постоянная память окупается: с company-context.md + регистратор решений, маршрутизатор знает, что уже решено, и не будет повторно подавать в суд.

## Примеры { #examples }

```
/cs:founder-mode "should we raise a Series B now or wait 6 months?"
   → boardroom (CFO + CEO + CRO touched)

/cs:founder-mode "the win rate dropped 20% this month"
   → cs-cro-advisor

/cs:founder-mode "gross retention dropped 5 points this quarter"
   → cs-cco-advisor

/cs:founder-mode "let's hire a VP Marketing"
   → boardroom (CHRO + CMO + CFO touched)

/cs:founder-mode "should we be growing faster?"
   → /cs:office-hours (too ambiguous)
```

## Связанный { #related }

- Агент: [`cs-chief-of-staff`](../../agents/cs-chief-of-staff.md) — выполняет ли маршрутизация
- Скилл: [`chief-of-staff`](../../../skills/chief-of-staff/SKILL.md) — логика маршрутизации
- Скилл: [`context-engine`](../../../skills/context-engine/SKILL.md) — загружает контекст

---

**Версия:** 1.0.0
