---
title: "/cs:soc2-audit-prep — SOC 2 Тип II Форсирующие вопросы { #cssoc2-audit-prep--soc-2-type-ii-forcing-questions } — Плагин и агентский скилл для Claude Code"
description: "/cs: soc2-аудит-подготовка <область применения> — SOC 2 Готовность II типа 6 - принудительный допрос. Сосредоточенный период наблюдения. Используйте. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:soc2-audit-prep — SOC 2 Тип II Форсирующие вопросы { #cssoc2-audit-prep--soc-2-type-ii-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-shield-lock-outline: Compliance OS</span>
<span class="meta-badge">:material-identifier: `soc2-audit-prep`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/soc2-audit-prep/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install compliance-os</code>
</div>


**Команда:** `/cs:soc2-audit-prep <scope>`

Аудитор SOC 2 Type II проверяет под давлением любую работу SOC 2. Шесть вопросов, регламентирующих период наблюдения, перед любым циклом типа II.

## Когда запускать { #when-to-run }

- Период предварительного наблюдения (1-2 месяца цикла)
- Середина периода наблюдения (контрольный пункт 6-го месяца)
- Предварительные полевые испытания (месяц 10)
- Пост-отчет (планирование следующего цикла)
- После изменения области применения (добавление категории TSC)
- После крупного инцидента в период наблюдения

## Шесть вопросов SOC 2 типа II { #the-six-soc-2-type-ii-questions }

### 1. Какова область применения и к каким категориям относятся TSC? { #1-whats-the-scope-and-which-tsc-categories-are-in }
** Безопасность требуется всегда; другие варианты выбираются в зависимости от запроса клиента.**
- Общие критерии (CC1-CC9) в разделе Безопасность всегда
- Доступность (A1): для SaaS с обязательствами по SLA
- Целостность обработки (PI1): для систем, обрабатывающих транзакционные / финансовые данные
- Конфиденциальность (C1): для систем, обрабатывающих служебные / конфиденциальные данные
- Конфиденциальность (P1-P8): для систем, обрабатывающих персональные данные (совпадает с GDPR, если применимо)
- Описание системы AICPA AT-C 205: полное + точное + четкие границы

### 2. Пропускал ли какой-либо контрольный цикл в течение периода наблюдения? { #2-did-any-control-skip-a-cycle-during-observation-period }
**Тип II требует последовательной работы — один пропущенный цикл = вероятное исключение.**
- Ежеквартальный контроль (например, ревью доступа): охвачены все 4 квартала
- Ежемесячный контроль (например, сканирование уязвимостей): охватываются все месяцы
- Непрерывный контроль (например, ведение журнала): никаких пробелов в течение периода
- Ежегодный контроль (например, упражнения по BCP, тренинги): завершен в течение периода

### 3. Покажите мне доказательства управления изменениями для любого контроля, внедренного в середине периода. { #3-show-me-the-change-management-evidence-for-any-control-implemented-mid-period }
**Изменения в середине периода = высокий риск аудита.**
- Новые элементы управления, внедренные во время наблюдения: документированы с помощью управления изменениями
- Модифицированные средства контроля: обоснование + дата вступления в силу + влияние на предыдущие образцы
- Снятый контроль: обоснование + оценка воздействия на клиента
- Стратегия: избегайте изменений в середине периода; отложите до следующего цикла

### 4. Где находится журнал исключений и какова оценка существенности? { #4-wheres-the-exception-log-and-whats-the-materiality-assessment }
**Регистрация исключений в режиме реального времени — не имеет обратной силы.**
- Каждое исключение регистрируется при обнаружении, а не во время аудита
- За исключением: что / когда / воздействие / исправление / владелец
- Оценка существенности: влияет ли исключение на общую работу системы контроля?
- Порог аудита фирмы: обычно приемлемо 1-2 исключения для каждого элемента контроля; 3+ = обнаружение

### 5. Покажите мне образцы доказательств по каждому критерию TSC за ПЕРВЫЙ месяц наблюдения. { #5-show-me-sample-evidence-from-each-tsc-criterion-in-the-first-month-of-observation }
** Не последнюю неделю — первый месяц.**
- Аудит выборок фирм за период наблюдения
- Загруженные заранее данные демонстрируют оперативную дисциплину
- Повторно загруженные данные (за последние 30 дней) = сигнал "скремблирования".
- Идентификаторы образцов должны быть воспроизводимыми из операционных систем

### 6. Каков переход к стандарту ISO 27001 и какие доказательства используются повторно? { #6-whats-the-cross-walk-to-iso-27001-and-which-evidence-reuses }
**контрольное перекрытие на 75% — каноническая пара.**
- Бежать `cross_framework_mapper.py` для совпадающих тем с высокой степенью достоверности
- Каждый общий артефакт, упомянутый в обоих аудитах (одна коллекция, два отчета)
- Согласуйте календарь аудита с cs-ciso-iso27001
- Избегайте создания дублирующих файлов доказательств для одного и того же контроля

## Воркфлоу { #workflow }

```bash
# 1. Scoping + gap analysis (pre-observation)
python ra-qm-team/skills/soc2-compliance/scripts/gap_analyzer.py current_state.json

# 2. Control matrix with ISO 27001 cross-walk
python ra-qm-team/skills/soc2-compliance/scripts/control_matrix_builder.py program.json

# 3. Continuous evidence tracking (during observation)
python ra-qm-team/skills/soc2-compliance/scripts/evidence_tracker.py evidence_log.json

# 4. Mock audit (pre-field-test month 10)
python ../../skills/compliance-os/scripts/audit_simulator.py soc2_scope.json
```

## Выходной формат { #output-format }

```markdown
# SOC 2 Type II Audit Prep: <scope>
**Date:** YYYY-MM-DD
**Observation Period:** YYYY-MM-DD to YYYY-MM-DD

## The Decision Being Made
[scoping | pre-observation | observation-status | pre-field | report-response]

## TSC Scope
- Security: included
- Availability: <yes/no>
- Processing Integrity: <yes/no>
- Confidentiality: <yes/no>
- Privacy: <yes/no>

## Observation Period Status
- Months elapsed: N / 12
- Controls operated consistently: % of total
- Cycle skips identified: <list>
- Mid-period control changes: N (each documented with change-mgmt: yes/no)

## Exception Log
- Total exceptions logged: N
- Per-control max exceptions: M (audit firm tolerance: typically 1-2)
- Material exceptions (overall control affected): <list>
- Remediation status per exception: complete/in-progress

## Sample Evidence Coverage
- Month 1-3 evidence: complete/gaps
- Month 4-6 evidence: complete/gaps
- Month 7-9 evidence: complete/gaps
- Month 10-12 evidence: complete/gaps (only for pre-report status)

## ISO 27001 Cross-Walk Reuse
- HIGH-confidence overlap themes: N
- Shared artefacts in evidence pool: <count>
- Duplicate evidence collection avoided: % savings

## Audit Firm Readiness
- Scoping discussion: complete/pending
- Description of system per AT-C 205: complete/pending
- Walkthrough rehearsal: complete/pending
- Sample preparation: complete/pending

## Verdict
🟢 ON-TRACK | 🟡 NEEDS-ATTENTION | 🔴 MATERIAL-RISK

## Top 3 Actions
[3 concrete next steps with owner + observation-period timing]
```

## Маршрутизация { #routing }

- `/cs:compliance-readiness` — для просмотра с несколькими фреймворками
- `/cs:iso27001-audit-prep` — для пары перекрестных переходов ISO 27001 (перекрытие 75%)
- `/cs:gdpr-audit-prep` — для обеспечения конфиденциальности TSC перекрывается
- `/cs:ciso-review` — для исполнительной стратегии кибербезопасности

## Связанный { #related }

- Агент: [`cs-soc2-auditor`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/agents/cs-soc2-auditor.md)
- Скилл: [`soc2-compliance`](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team/skills/soc2-compliance/SKILL.md)
- Плейбук: [soc2_audit_playbook.md](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team/skills/soc2-compliance/references/soc2_audit_playbook.md)
- Смежный: [`skills/iso27001-audit-prep`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/iso27001-audit-prep), [`skills/gdpr-audit-prep`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/gdpr-audit-prep), [`skills/compliance-readiness`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/compliance-readiness)

---

**Версия:** 1.0.0
