---
title: "/cs:iso27001-audit-prep — Аудит ISMS по стандарту ISO 27001 форсирует вопросы { #csiso27001-audit-prep--iso-27001-isms-audit-forcing-questions } — Плагин и агентский скилл для Claude Code"
description: "/cs: iso27001-аудит-подготовка <область применения> — готовность к аудиту ISMS по стандарту ISO 27001 6- принудительный опрос. Используйте перед. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:iso27001-audit-prep — Аудит ISMS по стандарту ISO 27001 форсирует вопросы { #csiso27001-audit-prep--iso-27001-isms-audit-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-shield-lock-outline: Compliance OS</span>
<span class="meta-badge">:material-identifier: `iso27001-audit-prep`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/iso27001-audit-prep/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install compliance-os</code>
</div>


**Команда:** `/cs:iso27001-audit-prep <scope>`

Аудитор ISMS по стандарту ISO 27001 проверяет работу любой ISMS под давлением. Шесть вопросов, основанных на выборке, перед любым внутренним аудитом, подготовкой к этапу 1 или аудитом наблюдения.

## Когда запускать { #when-to-run }

- Перед ежегодным пунктом 9.2 внутреннего аудита
- Перед этапом 1 / этапом 2 сертификационного аудита ISO 27001
- До проведения надзорного аудита (год 2 / год 3)
- После существенных изменений в сфере применения ISMS (новое бизнес-подразделение, новая линейка продуктов, внедрение нового SaaS)
- Пост-инцидент (нарушение триггеров специального аудита ISMS)
- Ежеквартально на этапе интенсивного роста

## Вопросы о шести "ИЗМАХ" { #the-six-isms-questions }

### 1. Каков объем аудита и выполняется ли переход на трехлетний охват? { #1-whats-the-audit-scope-and-is-rolling-3-year-coverage-on-track }
**Нет дисциплины охвата на 3 года, нет оправданной программы.**
- Каждый пункт 4-10 + каждое применимое средство контроля приложения А должно подвергаться аудиту не реже одного раза в трехлетний цикл
- Бежать `isms_audit_scheduler.py` в `ra-qm-team/skills/isms-audit-expert/`
- Подтвердите независимость аудитора — ни в одной выборке не проводился самостоятельный аудит

### 2. Когда в последний раз обновлялся реестр рисков и связаны ли методы лечения с мерами контроля, предусмотренными в приложении А? { #2-when-was-the-risk-register-last-refreshed-and-are-treatments-linked-to-annex-a-controls }
**Устаревший реестр рисков = обнаружение сертификата.**
- Ожидается ежеквартальное обновление; годовой минимум
- Каждый высокий/critical риск должен быть связан с контролем, относящимся к ≥ 1 приложению А, рассматривающему его
- Принятие остаточного риска задокументировано + подписано
- Ревью в отношении `iso27001_audit_playbook.md` что касается ожиданий на этапе 1

### 3. Покажите мне записи ревью access — квартальная частота, последние 4 квартала. { #3-show-me-the-access-review-records--quarterly-cadence-the-last-4-quarters }
** Наиболее цитируемая область поиска.**
- Приложение A.5.15 + A.8.2 + A.8.3 средства контроля доступа
- Примеры реальных записей, извлеченных из Okta / IAM, а не из подготовительных пакетов для аудита
- Для каждого уволенного сотрудника за последние 90 дней: подтверждение отмены предоставления в течение 24-часового соглашения об уровне обслуживания
- Ревью привилегированного доступа с более высокой степенью детализации

### 4. Каковы данные инвентаризации поставщика + последней ревью? { #4-whats-the-supplier-inventory--last-review-evidence }
**Вторая по популярности область поиска.**
- Приложение A.5.19-A.5.21 управление поставщиками
- Ревью важнейших поставщиков SaaS проводится не реже одного раза в год
- DPA, подписанные для субобработчиков персональных данных (перекрестная проверка с cs-dpo-gdpr)
- Положения контракта, относящиеся к ИИ, в которых используются сторонние сервисы ИИ (сверьте с cs-aims-iso42001)

### 5. Где доказательства реагирования на инцидент + ревью после инцидента? { #5-wheres-the-incident-response-evidence--post-incident-review }
**A.5.24-27 + A.6.8 — область аудита с высокими ставками.**
- Определения серьезности задокументированы + последовательно применяются
- Последние 5 инцидентов прошли ревью после инцидента (PIR) в течение 30-дневного SLA
- Сроки уведомления в соответствии со статьей 33/34 GDPR приведены в соответствие с A.5.24 (перекрестная проверка с cs-dpo-gdpr)
- Безупречная ретро-культура; не карательная

### 6. Какова частота проведения ревью руководством + вводимые данные? { #6-whats-the-management-review-cadence--inputs }
**Пункт 9.3 обязательные входные данные носят предписывающий характер — их легко пропустить.**
- Необходимые исходные данные: результаты аудита, риски, производительность, несоответствия, возможности
- График: минимум годовой; предпочтительнее ежеквартальный для зрелых программ
- Результаты документированы + отслеживаются до закрытия
- Интегрированный ревью по всем фреймворкам (в соответствии `multi_framework_audit_playbook.md`) предпочитал разделять ревью

## Воркфлоу { #workflow }

```bash
# 1. Audit programme planning
python ra-qm-team/skills/isms-audit-expert/scripts/isms_audit_scheduler.py audit_scope.json

# 2. Mock audit for readiness check
python ../../skills/compliance-os/scripts/audit_simulator.py iso27001_scope.json

# 3. Cross-framework reuse (SOC 2 = 75% overlap; ISO 42001 = 60% reuse)
python ../../skills/compliance-os/scripts/cross_framework_mapper.py program.json
```

## Выходной формат { #output-format }

```markdown
# ISO 27001 Audit Prep: <scope>
**Date:** YYYY-MM-DD

## The Decision Being Made
[programme-plan | finding-severity | cert-readiness | incident-followup]

## Audit Programme Status
- Clauses scheduled this year: <list>
- Annex A controls scheduled: <count>
- Rolling 3-year coverage: clean | gaps in <list>
- Auditor independence: clean | issues in <list>

## Risk Register Health
- Last refresh: YYYY-MM-DD
- High/critical risks without Annex A control link: N
- Residual risk acceptance documentation: complete | gaps

## High-Stakes Controls Status
- A.5.15 + A.8.2 + A.8.3 access control: pass/fail with sample
- A.5.19-A.5.21 supplier mgmt: pass/fail with sample
- A.5.24-27 + A.6.8 incident response: pass/fail with sample
- A.8.15-16 logging: pass/fail with sample

## Management Review Status
- Last review date: YYYY-MM-DD
- Required Article 9.3 inputs present: yes/no
- Open action items past due: N

## Cross-Framework Impact
- SOC 2 controls affected: <list>
- ISO 42001 controls affected (if applicable): <list>
- GDPR Article 32 controls affected: <list>

## Verdict
🟢 READY | 🟡 CLOSE-CRITICALS-FIRST | 🔴 NOT-READY

## Top 3 Actions
[3 concrete next steps with owner + corrective-action timeline]
```

## Маршрутизация { #routing }

- `/cs:compliance-readiness` — для просмотра с несколькими фреймворками
- `/cs:soc2-audit-prep` — для пары перекрестных переходов SOC 2 (перекрытие 75%)
- `/cs:aims-audit` — для целей стандарта ISO 42001 перекрестная ходьба
- `/cs:gdpr-audit-prep` — в отношении статьи 32 организационные меры перекрываются
- `/cs:ciso-review` — для исполнительной стратегии кибербезопасности
- `/cs:decide` — для регистрации вердикта

## Связанный { #related }

- Агент: [`cs-ciso-iso27001`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/agents/cs-ciso-iso27001.md)
- Скилл: [`isms-audit-expert`](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team/skills/isms-audit-expert/SKILL.md)
- Плейбук: [iso27001_audit_playbook.md](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team/skills/isms-audit-expert/references/iso27001_audit_playbook.md)
- Смежный: [`skills/soc2-audit-prep`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/soc2-audit-prep), [`skills/aims-audit`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/aims-audit), [`skills/gdpr-audit-prep`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/gdpr-audit-prep), [`skills/compliance-readiness`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/compliance-readiness)

---

**Версия:** 1.0.0
