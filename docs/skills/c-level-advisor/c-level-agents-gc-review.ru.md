---
title: "/cs:gc-ревью — Главный юрисконсульт, форсирующий вопросы { #csgc-review--general-counsel-forcing-questions } — Агентский скилл для руководителей"
description: "/cs:gc-ревью <план> — опрос главного юрисконсульта по контрактам, интеллектуальной собственности, нормативным актам, срокам службы и трудовому праву. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:gc-ревью — Главный юрисконсульт, форсирующий вопросы { #csgc-review--general-counsel-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `gc-review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/gc-review/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:gc-review <plan>`

Объектив главного юрисконсульта. Шесть вопросов перед любым контрактом, сроками действия, перемещением интеллектуальной собственности или обязательствами регулирующих органов. Это полоса, в которой gstack имеет нулевое значение - и где одно пропущенное предложение стоит больше года разработки.

> ⚠️ ** Не юридическая консультация.** Эта команда подсказывает правильные вопросы, которые нужно задать, прежде чем обращаться к стороннему консультанту. Всегда привлекайте квалифицированного юриста для принятия решений, имеющих обязательную силу.

## Когда запускать { #when-to-run }

- Перед подписанием любого контракта на сумму > 100 тысяч долларов или > 1 года
- Перед выпуском акционерного капитала (гранты сотрудникам, гранты консультантам)
- Перед ответом на экзаменационный лист
- Перед выходом на регулируемый рынок (здравоохранение, финтех, оборона)
- До принятия любого решения о лицензии с открытым исходным кодом в core IP
- Перед сделкой по слиянию и поглощению LOI

## Шесть вопросов GC { #the-six-gc-questions }

### 1. Владение интеллектуальной собственностью { #1-ip-ownership }
**Кому принадлежит IP-адрес, создаваемый или совместно используемый в рамках этой транзакции?**
- Работа по найму против лицензии против совместного предприятия.
- Для сотрудников и подрядчиков: существует письменное присвоение IP-адреса?
- Для операционных систем: проверена совместимость лицензий?

### 2. Ответственность и возмещение убытков { #2-liability--indemnity }
** Каков предел ответственности и что из этого вытекает?**
- Стандартный лимит: сборы за 12 месяцев.
- Исключения: нарушение прав интеллектуальной собственности, утечка данных, умышленное неправомерное поведение.
- Желательна взаимная компенсация.

### 3. Обработка данных { #3-data-processing }
**О каких персональных данных идет речь и действует ли DPA?**
- Сфера применения GDPR / CCPA?
- Нисходящий поток подпроцессора?
- Требования к месту жительства данных?

### 4. Прекращение действия и продление срока действия { #4-termination--renewal }
** Каково право на расторжение договора, каков срок уведомления и что такое автоматическое продление?**
- Прекращение действия по соображениям удобства, а не по причине.
- Период уведомления (30 / 60 / 90 дней).
- Ловушка автоматического обновления?

### 5. Регулирующая поверхность { #5-regulatory-surface }
**Подвергает ли это компанию новому режиму регулирования?**
- Здравоохранение → HIPAA.
- Финтех → BSA/AML, государственный переводчик денег.
- Медицинское устройство → FDA, MDR, ISO 13485.
- Данные → GDPR, CCPA, государственные законы о нарушениях.

### 6. Занятость/равенство { #6-employment--equity }
**Если речь идет о найме или подрядчике: юрисдикция, классификация, предоставление акционерного капитала, присвоение интеллектуальной собственности?**
- Риск неправильной классификации?
- Стандарт долевого участия (4-летний, 1-летний клифф)?
- Триггеры ускорения?
- Ток 409А?

## Воркфлоу { #workflow }

1. Прочтите контракт / условия от начала до конца
2. Ответьте на шесть вопросов
3. Определите топ-3 вопросов, которые нуждаются в ревью со стороны консультанта
4. Вынести вердикт

## Выходной формат { #output-format }

```markdown
# GC Review: <plan>
**Date:** YYYY-MM-DD

## Document
- Type: <contract / term sheet / grant / DPA>
- Counterparty: <name>
- $ value or scope: <amount>

## Issues
| # | Issue | Risk | Recommendation |
|---|---|---|---|
| 1 | <e.g., uncapped IP indemnity> | HIGH | Cap at fees paid, mutual |
| 2 | <e.g., 5-year auto-renew> | MED | 1-year max, 60-day notice |
| 3 | <e.g., no DPA, EU data> | HIGH | Require DPA before sign |

## Regulatory Trigger
- New regime triggered? <yes/no>
- Specific frameworks: <HIPAA / GDPR / etc.>

## Outside Counsel Action Items
- [ ] <specific item 1>
- [ ] <specific item 2>
- [ ] <specific item 3>

## Verdict
🟢 SIGN AS-IS (rare)
🟡 NEGOTIATE — counter on top-3 issues
🔴 DO NOT SIGN — material risk
```

## Маршрутизация { #routing }

- `/cs:ciso-review` — для любого контракта, касающегося данных
- `/cs:cfo-review` — за любое обязательство > 1 года или > 1% от выручки
- `/cs:decide` — зарегистрируйте вердикт после ревью стороннего адвоката

## Интеграция воркфлоу с `general-counsel-advisor` скилл { #workflow-integration-with-general-counsel-advisor-skill }

Начиная с версии 2.5.1, эта команда поддерживается полным скилл в [`skills/general-counsel-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/general-counsel-advisor) с помощью двух инструментов Python:

```bash
# Automated contract scan (12 founder-killer patterns)
python ../../../skills/general-counsel-advisor/scripts/contract_risk_scanner.py path/to/contract.txt

# Term sheet scoring (0-100 founder-friendliness)
python ../../../skills/general-counsel-advisor/scripts/term_sheet_analyzer.py path/to/term_sheet.json
```

Тот `cs-general-counsel-advisor` агент управляет обоими инструментами плюс 3 справочниками (плейбук контрактов, IP + regulatory, term sheet decoder).

## Связанный { #related }

- Скилл: [`general-counsel-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/general-counsel-advisor/SKILL.md) — полный скилл работы с инструментами Python + ссылки
- Агент: [`cs-general-counsel-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/agents/cs-general-counsel-advisor.md)
- Выполнение требований законодательства: [`ra-qm-team`](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team)
- Смежный: [`skills/ma-playbook`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/ma-playbook)

---

**Версия:** 1.0.0
