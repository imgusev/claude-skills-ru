---
name: "fda-qsr-audit-prep"
description: "/cs:fda-qsr-аудит-подготовка <область применения> — FDA 21 CFR 820 (QSR / QMSR) аудит 6 - принудительный опрос по вопросу. После февраля 2026 года существенно гармонизирован с ISO 13485. Используйте перед ежегодным внутренним аудитом QSR, подготовкой к инспекции FDA или ответом по форме 483."
---

# /cs:fda-qsr-audit-prep — FDA QSR форсирует вопросы { #csfda-qsr-audit-prep--fda-qsr-forcing-questions }

**Команда:** `/cs:fda-qsr-audit-prep <scope>`

Аудитор FDA по QSR проверяет под давлением работу любого медицинского устройства в США по QSR. Шесть вопросов перед любым внутренним аудитом, инспекцией FDA, ответом по форме 483 или решением об отзыве.

## Когда запускать { #when-to-run }

- Перед ежегодным внутренним аудитом QSR
- Перед ревью готовности к предварительной проверке FDA (любое устройство, коммерчески распространяемое в США)
- После получения формы 483 замечания
- После получения письма с предупреждением
- После МЛУ-отчетного события
- До принятия решения об отзыве (добровольного или инициированного FDA)
- Перед отправкой 510(k) / PMA (где положение QSR влияет на сроки утверждения)

## Шесть вопросов QSR { #the-six-qsr-questions }

### 1. Покажите мне файлы жалоб за последний квартал и соответствующие отчеты о MDR. { #1-show-me-the-complaint-files-from-the-last-quarter--and-the-corresponding-mdr-reports }
**21 CFR 820.198 + 21 CFR 803 — наиболее цитируемая зона инспекции FDA.**
- Заполнен журнал жалоб: кто / что / когда / устройство / пакет
- Завершение расследования в разумные сроки
- Применено дерево принятия решений по сообщению о МЛУ: смерть, серьезная травма ИЛИ неисправность, которые могли бы стать причиной = МЛУ
- 30-дневный график для большинства отчетов о МЛУ; 5 дней для некоторых серьезных событий
- Информация о тенденциях рассмотрения жалоб для ревью руководства

### 2. Когда в последний раз проводилась повторная проверка процесса (IQ/OQ/PQ) в соответствии с 21 CFR 820.75? { #2-when-was-process-validation-iqoqpq-last-revalidated-per-21-cfr-82075 }
**Соответствует пункту 7.5.6 стандарта ISO 13485 (существенно гармонизирован после февраля 2026 года).**
- Первоначальная проверка при внедрении процесса
- Триггеры повторной проверки: изменение процесса/оборудования/ материала ИЛИ периодический график
- Статистические методы за 21 820,250 канадских долларов, где это применимо
- Перекрестная проверка с помощью cs-cqm-iso13485 на соответствие стандарту ISO 13485

### 3. Покажите мне DHR для продуктов, коммерчески распространявшихся за последние 2 года. { #3-show-me-the-dhrs-for-products-commercially-distributed-in-last-2-years }
**21 CFR 820.180 — хранение в течение 2 лет после коммерческого распространения; проверьте полноту выборки.**
- Запись истории устройства (DHR) для каждого устройства/lot/batch
- Должны быть указаны: даты изготовления, произведенное количество, выпущенное количество, акты приемки, первичная идентификационная этикетка, идентификация устройства, контрольный номер.
- Выборка, стратифицированная по классу продукта
- Проверьте близость DHR к DHF (файлу истории проектирования)

### 4. Покажите мне CAPAS за последние 6 месяцев с подтверждением эффективности. { #4-show-me-capas-from-the-last-6-months-with-effectiveness-verification }
**21 CFR 820.100 = ISO 13485 8.5.2, существенно гармонизированный.**
- Глубина анализа первопричин (минимум 5 причин)
- Проверка эффективности = измеримые доказательства, а не "мы обновили процедуру".
- Документально подтвержденное различие между сдерживанием/исправлением/корректирующим действием
- Одобрение закрытия соответствующим органом
- Отмечены сроки выдержки > 90 дней

### 5. Покажите мне ревью по маркировке (21 CFR 801) для самого последнего выпуска продукта. { #5-show-me-labeling-21-cfr-801-review-for-the-most-recent-product-launch }
**Накладка, специфичная для FDA, отсутствует в стандарте ISO 13485.**
- Маркировка в соответствии с требованиями 21 CFR 801
- Для конкретных типов устройств: также 21 секторальная накладка серии CFR 800
- UDI (Уникальная идентификация устройства) за 21 CFR 830
- Рекламные материалы ревью проверяются на точность + не вводят в заблуждение

### 6. Если форма 483 была выдана за последние 3 года, покажите мне статус закрытия. { #6-if-a-form-483-was-issued-in-the-last-3-years-show-me-the-closure-status }
**Форма 483 = замечание FDA; не эквивалентно несоответствию ISO.**
- Ответ в течение 15 рабочих дней
- Каждое наблюдение задокументировано корректирующими + превентивными действиями с указанием сроков
- Доказательства проверки эффективности
- Для писем с предупреждениями: отдельный трек ответов + потенциальное совещание FDA

## Воркфлоу { #workflow }

```bash
# 1. QSR compliance posture
python ra-qm-team/skills/fda-consultant-specialist/scripts/qsr_compliance_checker.py compliance_state.json

# 2. FDA submission tracking (510(k) / PMA / IDE)
python ra-qm-team/skills/fda-consultant-specialist/scripts/fda_submission_tracker.py submissions.json

# 3. HIPAA overlap (if connected device handles PHI)
python ra-qm-team/skills/fda-consultant-specialist/scripts/hipaa_risk_assessment.py phi_inventory.json

# 4. Mock FDA inspection
python ../../skills/compliance-os/scripts/audit_simulator.py fda_qsr_scope.json
```

## Выходной формат { #output-format }

```markdown
# FDA QSR Audit Prep: <scope>
**Date:** YYYY-MM-DD

## The Decision Being Made
[programme-plan | inspection-readiness | 483-response | MDR-decision | recall]

## Complaint + MDR Posture
- Complaints last quarter: N
- MDR-reportable events: M
- MDR reports filed within timeline: % (target 100%)
- Complaint trending review at management level: yes/no

## Process Validation Status (21 CFR 820.75)
- Validations on schedule: %
- Stale validations: <list>
- Statistical techniques applied: yes/no per process

## DHR Completeness (21 CFR 820.180)
- DHRs sampled: N
- Completeness rate: %
- 2-year retention compliant: yes/no
- Stratified by product class: yes/no

## CAPA Health (21 CFR 820.100)
- CAPAs sampled: N
- Root cause analysis depth: adequate/inadequate
- Effectiveness verification: complete/incomplete
- Aging CAPAs > 90 days: N

## Labeling (21 CFR 801)
- Recent products reviewed: <list>
- Labeling accurate + non-misleading: yes/no
- UDI compliance per 21 CFR 830: yes/no

## Form 483 / Warning Letter History
- Form 483s last 3 years: N (each: closed/in-progress)
- Warning Letters last 5 years: N (each: closed/in-progress)
- Pattern across observations: <thematic>

## ISO 13485 Cross-Walk (post-Feb 2026 harmonization)
- ISO 13485 audit findings: <link to cs-cqm-iso13485 output>
- FDA-specific overlays remaining: labeling + complaint handling + MDR reporting + recall procedures
- Cross-framework reuse: % of evidence shared

## Verdict
🟢 INSPECTION-READY | 🟡 GAPS-IDENTIFIED | 🔴 NOT-READY

## Top 3 Actions
[3 concrete next steps with owner + FDA-cited timeline (15 days / 30 days / etc.)]

## Outside Counsel Required
[For Warning Letter response, recall decisions, or 510(k) / PMA strategy disputes]
```

## Маршрутизация { #routing }

- `/cs:compliance-readiness` — для просмотра с несколькими фреймворками
- `/cs:iso13485-audit-prep` — для пары перекрестных переходов по стандарту ISO 13485 (в значительной степени согласовано)
- `/cs:gdpr-audit-prep` — если подключенное устройство обрабатывает персональные данные
- `/cs:gc-review` — для координации ответа на письмо с предупреждением

## Связанный { #related }

- Агент: [`cs-fda-qsr-auditor`](../../agents/cs-fda-qsr-auditor.md)
- Скилл: [`fda-consultant-specialist`](../../../ra-qm-team/skills/fda-consultant-specialist/SKILL.md)
- Смежный: `../iso13485-audit-prep/`, `../compliance-readiness/`

---

**Версия:** 1.0.0
