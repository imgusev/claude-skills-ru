---
name: "iso13485-audit-prep"
description: "/cs: iso13485-аудит-подготовка <область применения> — аудит СМК ISO 13485 6 - принудительный опрос по вопросам. Управление дизайном + CAPA + ориентация на пострыночный рынок. Используйте перед пунктом 8.2.4 внутреннего аудита, ревью соответствия QSR MDR/FDA или аудитом закрытия DHF перед запуском продукта."
---

# /cs: iso13485-аудит-подготовка — ISO 13485 СМК форсирует вопросы { #csiso13485-audit-prep--iso-13485-qms-forcing-questions }

**Команда:** `/cs:iso13485-audit-prep <scope>`

Аудитор СМК по стандарту ISO 13485 проверяет под давлением работу любой системы менеджмента качества медицинского оборудования. Шесть вопросов, связанных с отслеживаемостью, перед любым внутренним аудитом, ревью MDR / FDA QSR или запуском продукта.

## Когда запускать { #when-to-run }

- Перед ежегодным пунктом 8.2.4 внутреннего аудита
- Перед ревью по согласованию MDR/FDA QSR (существенно гармонизировано после февраля 2026 г.)
- Перед коммерческим запуском нового устройства (аудит закрытия DHF)
- После значительного события закрытия CAPA (аудит по проверке эффективности)
- Событие после отзыва (первопричина + аудит корректирующих действий)
- Ежеквартально во время подготовки нормативных документов

## Шесть вопросов по СМК { #the-six-qms-questions }

### 1. Извлеките три случайных DHF. Завершены ли доказательства верификации проекта + валидации? { #1-pull-three-random-dhfs-are-design-verification--validation-evidence-complete }
** Наиболее цитируемая область поиска.**
- DHF должен включать: план проектирования + входные данные + выходные данные + верификация + валидация + передача + изменения
- Выборка, стратифицированная по классу продукта (I, IIa, IIb, III на МЛУ)
- Ссылка `iso13485_audit_playbook.md` для чек-листа для каждого DHFFF
- Проверьте матрицу прослеживаемости на основе потребностей пользователя с помощью клинических данных

### 2. Покажите мне последние 5 CAPAs с доказательствами проверки эффективности. { #2-show-me-the-last-5-capas-with-effectiveness-verification-evidence }
**Вторая по популярности область поиска.**
- Документально подтвержденное различие между сдерживанием/исправлением/корректирующим действием
- Глубина анализа первопричин: минимум 5 причин
- Проверка эффективности = измеримые доказательства, а не "мы обновили процедуру".
- Закрытие, одобренное соответствующим органом
- Повторные настройки для разных продуктов = триггер системной проблемы

### 3. Когда в последний раз проводилась повторная проверка процесса (IQ/OQ/PQ)? { #3-when-was-process-validation-iqoqpq-last-revalidated }
**Пункт 7.5.6 — часто устарел.**
- Первоначальная проверка при внедрении процесса
- Триггеры повторной проверки: изменение технологического процесса, замена оборудования, замена материала, периодический график
- Мониторинг тенденций (SPC), при котором применяются статистические методы в соответствии с пунктом 8.4
- Перепроверьте с cs-fda-qsr-аудитором соответствие 21 CFR 820.75

### 4. Покажите мне файл управления рисками для продукта с самым высоким уровнем риска. { #4-show-me-the-risk-management-file-for-the-highest-risk-product }
**Пункт 7.1 + ISO 14971:2019.**
- План управления рисками существует для каждого продукта
- Идентификация опасности охватывает разумное предсказуемое неправильное использование
- Применяемая иерархия контроля рисков: неотъемлемая безопасность > защитные меры > информация для обеспечения безопасности
- Остаточный риск оценен + принят с обоснованием
- Информация о постпроизводстве поступает обратно в RMF
- Для медицинских устройств с поддержкой искусственного интеллекта: уровень ISO 42001 A.5 оценка воздействия сверху

### 5. Покажите мне данные пострыночного надзора за последние 6 месяцев. { #5-show-me-post-market-surveillance-evidence--last-6-months }
**Пункт 8.2.1 — высокие ставки для МЛУ + FDA.**
- Журнал жалоб клиентов + завершение расследования
- Отчеты о бдительности (серьезный инцидент / FSCA), представленные в соответствии с применимыми правилами
- Данные анализа тенденций + ревью руководства
- Последующее клиническое наблюдение (PMCF) за устройствами высокого риска МЛУ
- Отчеты о MDR в соответствии с 21 CFR 803 для устройств, продаваемых в США (перекрестная проверка с cs-fda-qsr-аудитором)

### 6. Где доказательства ревью руководства, охватывающие все исходные данные по пункту 5.6? { #6-wheres-the-management-review-evidence-covering-all-clause-56-inputs }
**Годовой минимум; полугодовой для зрелых программ.**
- Требуемые исходные данные в соответствии с пунктом 5.6.2: результаты аудита, отзывы клиентов, производительность процесса, соответствие продукции, статус превентивных + корректирующих действий, последующие действия по результатам предыдущих ревью, изменения, которые могут повлиять на СМК, рекомендации по улучшению, нормативные требования
- Результаты согласно пункту 5.6.3: решения по улучшению, изменения требований к продукту, потребности в ресурсах
- Интегрированный ревью по всем фреймворкам (в соответствии `multi_framework_audit_playbook.md`) предпочтительный

## Воркфлоу { #workflow }

```bash
# 1. Audit programme optimization
python ra-qm-team/skills/qms-audit-expert/scripts/audit_schedule_optimizer.py audit_scope.json

# 2. Mock audit for readiness check
python ../../skills/compliance-os/scripts/audit_simulator.py iso13485_scope.json

# 3. CAPA system review
# Route to ra-qm-team/skills/capa-officer/ tools

# 4. Risk management file review
# Route to ra-qm-team/skills/risk-management-specialist/ tools
```

## Выходной формат { #output-format }

```markdown
# ISO 13485 Audit Prep: <scope>
**Date:** YYYY-MM-DD

## The Decision Being Made
[programme-plan | DHF-closure | CAPA-health | post-market-trend | pre-cert | MDR-FDA-alignment]

## Design Control Status (sampled DHFs)
- DHFs sampled: <list product IDs>
- Verification evidence: pass/fail per DHF
- Validation evidence: pass/fail per DHF
- Clinical evidence (per MDR Annex XIV / FDA 510(k)): pass/fail
- Traceability matrix complete: yes/no per DHF

## CAPA Health
- CAPAs sampled: N
- Root cause analysis depth: adequate/inadequate per CAPA
- Effectiveness verification: complete/incomplete per CAPA
- Aging CAPAs > 90 days: N
- Repeat issues across products: <list>

## Process Validation Status
- Validations on schedule: %
- Stale validations (> 12 months since revalidation): <list>
- Statistical techniques applied per Clause 8.4: yes/no

## Risk Management File Status
- Sampled product RMFs: <list>
- Post-production updates in last 12 months: <count per product>
- Residual risk acceptance signed: yes/no

## Post-Market Surveillance
- Complaint trending: stable/rising
- MDR / vigilance reports filed timely: %
- PMCF on schedule (where required): yes/no

## Management Review Status
- Last review date: YYYY-MM-DD
- Required Clause 5.6.2 inputs present: yes/no
- Open action items past due: N

## Cross-Framework Impact
- EU MDR alignment: clean / gaps in <list>
- FDA QSR alignment (post-Feb 2026): substantially harmonized; FDA-specific overlays per cs-fda-qsr-auditor
- ISO 42001 AIMS overlay (if AI-enabled device): pass/fail per Annex A

## Verdict
🟢 READY | 🟡 CLOSE-DHF-GAPS-FIRST | 🔴 NOT-READY

## Top 3 Actions
[3 concrete next steps with owner + corrective-action timeline]
```

## Маршрутизация { #routing }

- `/cs:compliance-readiness` — для просмотра с несколькими фреймворками
- `/cs:fda-qsr-audit-prep` — для наложения, специфичного для FDA
- `/cs:aims-audit` — для медицинского устройства с поддержкой искусственного интеллекта уровень ISO 42001
- `/cs:gdpr-audit-prep` — для дублирования персональных данных (клинические данные, данные клиентов)
- `/cs:cpo-review` — для принятия управленческих решений по стратегии продукта
- `/cs:decide` — для регистрации вердикта

## Связанный { #related }

- Агент: [`cs-cqm-iso13485`](../../agents/cs-cqm-iso13485.md)
- Скилл: [`qms-audit-expert`](../../../ra-qm-team/skills/qms-audit-expert/SKILL.md)
- Плейбук: [iso13485_audit_playbook.md](../../../ra-qm-team/skills/qms-audit-expert/references/iso13485_audit_playbook.md)
- Смежный: `../fda-qsr-audit-prep/`, `../aims-audit/`, `../compliance-readiness/`

---

**Версия:** 1.0.0
