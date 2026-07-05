---
title: "/cs:ciso-ревью — CISO форсирует вопросы { #csciso-review--ciso-forcing-questions } — Агентский скилл для руководителей"
description: "/cs:ciso-ревью <плана> — Параноидальный анализ рисков любого плана, который касается данных, соответствия требованиям или производственного доступа. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:ciso-ревью — CISO форсирует вопросы { #csciso-review--ciso-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `ciso-review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/ciso-review/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:ciso-review <plan>`

Специалист по моделированию рисков и параноидальных угроз. Шесть вопросов перед любым производственным изменением, касающимся данных клиента или сферы соответствия требованиям.

## Когда запускать { #when-to-run }

- Перед деплей любой системы, которая касается данных PII / PHI / держателя карты
- Перед подписанием контракта с новым поставщиком с доступом к данным
- Перед аудитом соответствия требованиям (SOC 2, ISO 27001, HIPAA, GDPR)
- Прежде чем какое-либо архитектурное решение пересечет границы доверия
- После любого инцидента, близкого к промаху

## Шесть вопросов CISO { #the-six-ciso-questions }

### 1. Модель угрозы { #1-threat-model }
**Какова модель угроз STRIDE для этой системы и какая угроза наиболее вероятна?**
- Подмена, Фальсификация, Отказ от ответственности, раскрытие информации, DoS, повышение привилегий.
- Выберите топ-3 по вероятности × воздействию.

### 2. Радиус поражения { #2-blast-radius }
**Если это будет полностью скомпрометировано, какие данные будут раскрыты и сколько пользователей пострадает?**
- Наихудший вариант на простом английском языке.
- Количественно выражайте в долларах с помощью ЧЕСТНОГО ЭЛЯ.

### 3. Обнаружение { #3-detection }
**Какие сигналы указывают на компромисс и через сколько времени они будут триггерами (MTTD)?**
- Сами по себе журналы не являются обнаружением.
- Определите правило обнаружения, оповещение и вызов по вызову.

### 4. Реакция { #4-response }
**Существует ли IR-рансбук для этого сценария и был ли он протестирован на настольных компьютерах?**
- Если нет рансбука: создайте его перед отправкой.
- Если не протестировано: столешница перед отправкой.

### 5. Окно регулирования { #5-regulatory-window }
**Каково окно уведомления регулирующего органа в случае возникновения такого сценария?**
- GDPR: 72 часа. HIPAA: 60d. Законы о нарушениях в штатах различаются.
- Предварительно напишите шаблон для связи с клиентом.

### 6. Поставщик и цепочка поставок { #6-vendor--supply-chain }
**Какие сторонние поставщики входят в сферу действия и какова их система безопасности?**
- Текущий список подпроцессоров?
- DPA на месте?
- Последний ревью по безопасности для каждого поставщика?

## Воркфлоу { #workflow }

```bash
python ../../../skills/ciso-advisor/scripts/risk_quantifier.py
python ../../../skills/ciso-advisor/scripts/compliance_tracker.py
```

## Выходной формат { #output-format }

```markdown
# CISO Review: <plan>
**Date:** YYYY-MM-DD

## Threat Model
- Top threat: <STRIDE category> — <description>
- Likelihood: H/M/L | Impact: H/M/L
- ALE: $X / year

## Blast Radius
- Data exposed (worst case): <description>
- Users affected: N
- Estimated cost: $X

## Detection
- MTTD target: X hours
- Current MTTD: X hours
- Detection rule: <name>

## Response
- IR runbook: ✅ / ❌
- Last tabletop: <date>

## Regulatory
- Frameworks in scope: SOC 2 / ISO 27001 / HIPAA / GDPR
- Notification window: X hours/days

## Vendors
- New vendors added: N
- DPAs signed: N / N
- Security reviews complete: N / N

## Verdict
🟢 SHIP | 🟡 MITIGATE THEN SHIP | 🔴 BLOCK
```

## Маршрутизация { #routing }

- `/cs:cto-review` — согласование архитектуры
- `/cs:gc-review` — DPA, нормативные последствия
- `/cs:decide` — регистрируйте принятие риска
- `/cs:boardroom` — для КРИТИЧЕСКИХ рисков

## Связанный { #related }

- Агент: [`cs-ciso-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/agents/cs-ciso-advisor.md)
- Скилл: [`ciso-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ciso-advisor/SKILL.md)
- Соответствие требованиям: [`ra-qm-team`](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team)

---

**Версия:** 1.0.0
