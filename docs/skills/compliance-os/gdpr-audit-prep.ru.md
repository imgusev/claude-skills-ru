---
title: "/cs:gdpr-аудит-подготовка — GDPR DPO - Форсирующие вопросы { #csgdpr-audit-prep--gdpr-dpo-forcing-questions } — Плагин и агентский скилл для Claude Code"
description: "/cs:gdpr-аудит-подготовка <область применения> — аудит GDPR 6-статья с вопросом - цитируемый принудительный допрос. Используйте перед ежегодной. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:gdpr-аудит-подготовка — GDPR DPO - Форсирующие вопросы { #csgdpr-audit-prep--gdpr-dpo-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-shield-lock-outline: Compliance OS</span>
<span class="meta-badge">:material-identifier: `gdpr-audit-prep`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/gdpr-audit-prep/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install compliance-os</code>
</div>


**Команда:** `/cs:gdpr-audit-prep <scope>`

Аудитор DPO по GDPR проверяет под давлением любую работу по соблюдению конфиденциальности. Шесть цитируемых в статье вопросов перед любым внутренним аудитом, реагированием на нарушения, расследованием DPA или проведением due diligence при приобретении.

## Когда запускать { #when-to-run }

- Перед ежегодным внутренним аудитом GDPR
- Перед ежеквартальным обновлением статьи 30 RoPA
- Перед запуском новой обработки с высоким риском (требуется статья 35 DPIA)
- Последующее нарушение (статьи 33-34)
- До принятия мер по расследованию DPA или привлечению надзорного органа
- Во время проведения due diligence при приобретении (политика конфиденциальности целевой компании)
- Ежеквартально во время крупномасштабных поставок новых функций

## Шесть вопросов DPO { #the-six-dpo-questions }

### 1. Покажите мне статью 30 RoPA — с датой последнего обновления. { #1-show-me-the-article-30-ropa--with-last-updated-date }
** Наиболее цитируемая область поиска.**
- Должны включать все элементы статьи 30(1)(a)-(g) для контроллеров
- Должны включать все элементы статьи 30(2)(a)-(d) для переработчиков
- Обновлено в разумные сроки после внесения изменений (ожидается, что через 90 дней)
- Соглашения о совместном контролере, задокументированные в соответствии со статьей 26

### 2. Каковы законные основания для этой операции по обработке данных в соответствии со статьей 6? { #2-for-this-processing-activity-whats-the-lawful-basis-under-article-6 }
**Статья 6 является эксклюзивной — выберите ОДНО основание для каждой цели.**
- Шесть вариантов: согласие / контракт / юридическое обязательство / жизненно важные интересы / общественная задача / законные интересы
- Где "законные интересы": документально подтвержденный LIA
- Где "согласие": записи в соответствии со статьей 7; механизм отзыва
- Особые категории (статья 9) требуют исключения из статьи 9(2)

### 3. Для обработки с высоким риском, где находится DPIA в соответствии со статьей 35? { #3-for-high-risk-processing-wheres-the-dpia-per-article-35 }
**Требуется для мероприятий с высоким риском; выборка из 3-5 видов деятельности.**
- Статья 35(7)(a)-(d) обязательные элементы:
  - Систематическое описание процесса обработки
  - Оценка необходимости + соразмерности
  - Риски для прав и свобод
  - Меры по устранению рисков
- С DPO были проведены консультации в соответствии со статьей 35(2)
- Статья 36 предварительная консультация триггера по остаточному высокому риску
- Для систем искусственного интеллекта: интегрируется со статьей 27 Закона ЕС об искусственном интеллекте FRIA (перекрестная проверка с cs-ai-act-соответствие)

### 4. Покажите мне DSAR за последние 30 дней и время ответа. { #4-show-me-a-dsar-from-the-last-30-days--and-the-response-timing }
**Статьи 15-22 операционный воркфлоу.**
- Ответ в течение 1 месяца (статья 12(3)); продление до 2 месяцев для сложных запросов
- Процесс проверки личности задокументирован
- Ответ о праве доступа включает всю информацию, предусмотренную статьей 15
- Право на удаление (статья 17) воркфлоу распространяется на резервные копии + процессоры

### 5. Покажите мне оценки воздействия трансфертов для крупнейших трансфертов за пределы ЕС. { #5-show-me-transfer-impact-assessments-for-the-largest-non-eu-transfers }
**Дисциплина Schrems II.**
- Решение об адекватности ИЛИ SCCs (статья 46) ИЛИ отступление (статья 49)
- TIA в соответствии с рекомендациями EDPB 01/2020 + 02/2020
- Дополнительные меры в тех случаях, когда TIA выявила риск
- Переводы в США, подпадающие под действие Фреймворка адекватности защиты данных ЕС-США (июль 2023 г.) — проверка списка сертифицированных организаций

### 6. Покажите мне журнал нарушений в соответствии со статьей 33(5) — все нарушения, а не только те, о которых можно уведомить. { #6-show-me-the-breach-log-per-article-335--all-breaches-not-just-notifiable-ones }
**Статья 33(5) требует регистрировать ВСЕ нарушения.**
- Документированный внутренний механизм обнаружения нарушений
- Уведомление по статье 33 DPA в течение 72 часов (при необходимости)
- Статья 34 уведомление субъекта данных (при высоком риске)
- Первопричина + корректирующие действия через систему CAPA
- Перекрестная проверка с помощью cs-ciso-iso27001 для согласования A.5.24-27 управления инцидентами

## Воркфлоу { #workflow }

```bash
# 1. Compliance posture
python ra-qm-team/skills/gdpr-dsgvo-expert/scripts/gdpr_compliance_checker.py compliance_state.json

# 2. DPIA for high-risk activities
python ra-qm-team/skills/gdpr-dsgvo-expert/scripts/dpia_generator.py processing_activity.json

# 3. DSAR workflow validation
python ra-qm-team/skills/gdpr-dsgvo-expert/scripts/data_subject_rights_tracker.py dsar_log.json

# 4. Cross-framework reuse with ISO 27001 + SOC 2 + ISO 42001
python ../../skills/compliance-os/scripts/cross_framework_mapper.py program.json
```

## Выходной формат { #output-format }

```markdown
# GDPR Audit Prep: <scope>
**Date:** YYYY-MM-DD
**Article Citations:** Every finding cites Article + paragraph; no paraphrase.

## The Decision Being Made
[RoPA-refresh | DPIA-required | DSAR-workflow | transfer-risk | breach-followup | DPA-readiness]

## Article 30 RoPA Status
- Last refresh: YYYY-MM-DD
- Required elements present: yes/no per processing activity
- Joint controller arrangements: documented/missing

## Article 6 Lawful Basis Discipline
- Activities reviewed: N
- Legitimate-interests claims without LIA: <list>
- Article 9 special categories with documented exception: yes/no

## Article 35 DPIA Quality
- High-risk activities requiring DPIA: <list>
- DPIAs complete per Article 35(7): pass/fail per activity
- Article 36 prior consultation triggered: <list>

## Data Subject Rights (Articles 12-22)
- DSARs in last 90 days: N
- Average response time: X days (target: ≤ 30)
- Right to erasure backup-processor flow: complete/incomplete

## Article 28 Processor Management
- Processors reviewed: N
- Contracts with all Article 28(3)(a)-(j) clauses: % complete
- Sub-processor flow-down notification mechanism: yes/no

## Schrems II Transfer Status
- Non-EU transfers: <list>
- Mechanism per transfer: adequacy / SCCs / derogation
- TIA on file: yes/no per transfer
- Supplementary measures where needed: <list>

## Article 33-34 Breach Discipline
- Breach log last 12 months: N
- Article 33 notification timing: ≤ 72h ratio
- Article 34 data subject notification (where high risk): on-time ratio

## Cross-Framework Impact
- ISO 27001 Article 32 alignment: clean / gaps
- EU AI Act Article 27 FRIA integration: applicable / not
- SOC 2 Privacy TSC alignment (if scope): clean / gaps

## Verdict
🟢 DPA-READY | 🟡 GAPS-IDENTIFIED | 🔴 NOT-READY

## Top 3 Actions
[3 concrete next steps with owner + Article-cited timeline]

## Outside Counsel Required
[Article-level ambiguities flagged: Schrems II supplementary measure adequacy, EU AI Act ↔ GDPR interaction, sectoral derogation interpretation, novel DPA enforcement]
```

## Маршрутизация { #routing }

- `/cs:compliance-readiness` — для просмотра с несколькими фреймворками
- `/cs:iso27001-audit-prep` — по статье 32 организационные меры
- `/cs:ai-act-readiness` — для статьи 27 Закона ЕС об ИИ Интеграция FRIA
- `/cs:soc2-audit-prep` — для SOC 2 конфиденциальность TSC перекрывается
- `/cs:gc-review` — для юридического ревью по новому делу

## Связанный { #related }

- Агент: [`cs-dpo-gdpr`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/agents/cs-dpo-gdpr.md)
- Скилл: [`gdpr-dsgvo-expert`](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team/skills/gdpr-dsgvo-expert/SKILL.md)
- Плейбук: [gdpr_audit_playbook.md](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team/skills/gdpr-dsgvo-expert/references/gdpr_audit_playbook.md)
- Смежный: [`skills/iso27001-audit-prep`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/iso27001-audit-prep), [`skills/ai-act-readiness`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/ai-act-readiness), [`skills/soc2-audit-prep`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/soc2-audit-prep), [`skills/compliance-readiness`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/compliance-readiness)

---

**Версия:** 1.0.0
