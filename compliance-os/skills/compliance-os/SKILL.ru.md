---
name: "compliance-os"
description: "Compliance OS — мета-оркестратор, который позволяет командам по обеспечению соответствия НАСТРАИВАТЬ, какие фреймворки применять, ВЫЧИСЛЯТЬ перекрытие контроля между фреймворками, ИМИТИРОВАТЬ внутренние аудиты и КОНСОЛИДИРОВАТЬ доказательства в нескольких фреймворках. Четыре решения: (1) Учитывая профиль компании, какой из 12 поддерживаемых фреймворков применим (ISO 27001/13485/42001/14971, Закон ЕС об ИИ, MDR 745, GDPR, SOC 2, FDA QSR, NIST CSF 2.0, NIS2, HIPAA)? (2) В рамках выбранных фреймворков, которые контролируют дублирование и сколько доказательств используется повторно? (3) Что дает реалистичный макет аудита для данного фреймворка + области применения, взятый из библиотеки 205 сценариев? (4) Каков единый чек-лист фактических данных для выбранных фреймворков с картой повторного использования? Используйте при разработке программы с несколькими фреймворками, планировании календаря ежегодных аудитов или подготовке к этапу 1 сертификации. НЕ заменяет скиллы для каждого фреймворка (он организует их)."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: compliance-os
  domain: multi-framework-compliance-orchestration
  updated: 2026-05-13
  python-tools: framework_selector.py, cross_framework_mapper.py, audit_simulator.py, evidence_pool_generator.py
  frameworks: iso-27001, iso-13485, iso-42001, iso-14971, eu-ai-act, eu-mdr-745, gdpr, soc-2, fda-qsr, nist-csf, nis2, hipaa
---

# Соответствие требованиям ОС — Мета-оркестратор { #compliance-os--meta-orchestrator }

Оркестрация программы соответствия требованиям с использованием нескольких фреймворков. **Четыре решения, без глубокого погружения в каждый фреймворк:**

1. **Какие фреймворки применимы к этой компании?** — `framework_selector.py` ранжирует 12 поддерживаемых фреймворков по профилю компании (отрасль, география, использование искусственного интеллекта, медицина, финансы, численность персонала, клиенты, здравоохранение-PHI, NIS2 essential/important организация, подрядчик правительства США) и возвращает применимые с графом зависимостей
2. **Насколько сильно перекрываются выбранные фреймворки?** — `cross_framework_mapper.py` вычисляет перекрытие уровней контроля с оценкой достоверности; выводит унифицированную матрицу контроля + возможности повторного использования фактических данных
3. **Что дает имитационный аудит?** — `audit_simulator.py` генерирует 8-15 сценариев поиска с распределением серьезности, соответствующим ожиданиям IIA + вопросы для интервью для каждого элемента управления
4. **Что такое единый чек-лист для получения доказательств?** — `evidence_pool_generator.py` объединяет данные во всех включенных фреймворках; выводит, какой артефакт удовлетворяет каким элементам управления во всех фреймворках

Этот скилл ** НЕ является ** глубоким погружением для каждого фреймворка. Скиллы для каждого фреймворка (`ra-qm-team/skills/iso42001-specialist/`, `compliance-team-eu-ai-act/`, `ra-qm-team/skills/gdpr-dsgvo-expert/`, и т.д.) выполняют оперативную работу. Операционная система Compliance управляет ими.

Этот скилл **НЕ** заменяет обязательную юридическую консультацию. Сопоставления между фреймворками отражают опубликованные рекомендации (стандарты ISO, нормативные акты, руководство EDPB/Комиссии, профессиональные стандарты IIA/ AICPA). Новые перекрестные прогулки следует ревью проводить с консультантом.

## Ключевые слова { #keywords }

оркестрация соответствия, соответствие с несколькими фреймворками, операционная система соответствия, сопоставление кросс-фреймворков, дублирование контроля, пул доказательств, повторное использование доказательств, имитация аудита, имитационный аудит, программа внутреннего аудита, GRC, соответствие рискам управления, выбор фреймворка, программа соответствия, интегрированное соответствие, ISO 19011, IIA IPPF, AICPA AT-C, Профиль NIST CSF, программа multi-cert, SOC 2 + ISO 27001, ISO 27001 + ISO 42001, ISO 13485 + MDR 745, AI Act + ISO 42001, GDPR + ISO 27001, специалист по соблюдению требований, воркфлоу команды по соблюдению требований, готовность к сертификации

## Быстрый старт { #quick-start }

```bash
# Decision A: Which frameworks apply for the company?
python scripts/framework_selector.py                          # embedded mid-stage AI SaaS sample
python scripts/framework_selector.py path/to/profile.json

# Decision B: Compute cross-framework overlap
python scripts/cross_framework_mapper.py                      # embedded ISO 27001 + SOC 2 sample
python scripts/cross_framework_mapper.py path/to/control_libs.json

# Decision C: Simulate an audit
python scripts/audit_simulator.py                             # embedded ISO 27001 sample
python scripts/audit_simulator.py path/to/audit_scope.json

# Decision D: Consolidate evidence checklist across frameworks
python scripts/evidence_pool_generator.py                     # embedded 3-framework sample
python scripts/evidence_pool_generator.py path/to/program.json
```

## Ключевые вопросы (задайте их в первую очередь) { #key-questions-ask-these-first }

- **Назвали ли вы все применимые фреймворки?** Забыть об одном означает перестроить программу аудита позже. Бежать `framework_selector.py` с вашим профилем.
- **Какие наиболее распространенные сертификаты / нормативные акты уже действуют в вашей компании?** Это ваш якорь повторного использования. Сопоставьте с ним каждый новый фреймворк.
- ** Каков календарь аудита?** Программа с несколькими фреймворками подразумевает проведение надзорных аудитов в рамках годового плана "Независимость аудитора + потенциал".
- **Где хранятся доказательства?** Программы с несколькими фреймворками терпят крах, когда доказательства хранятся на диске одной команды без индекса. Бежать `evidence_pool_generator.py` чтобы выявить возможности повторного использования.
- **Какова частота проведения ревью со стороны руководства в разных фреймворках?** Каждому фреймворку требуется свой собственный управленческий ревью, но единый интегрированный ревью (согласно приложению ISO SL) обычно удовлетворяет их всех с помощью одного календарного интервала.
- **Кому принадлежит метапрограмма?** Если нет единой ответственной роли, программа фрагментируется.

## Основные обязанности { #core-responsibilities }

### 1. Выбор фреймворка { #1-framework-selection }

** Фреймворк:** JSON профиля компании в → применимо-список фреймворков с графиком зависимостей.

**Детерминированная логика:**
- Медицинское устройство → ISO 13485 + ISO 14971 + (EU MDR 745 для рынка ЕС) + (FDA QSR для рынка США)
- ИИ, ориентированный на клиента → ISO 42001 + Закон ЕС об ИИ (для пользователей из ЕС) + GDPR (для персональных данных)
- B2B SaaS для корпоративных клиентов → SOC 2 + ISO 27001 (часто требуется для закупок)
- Клиенты из ЕС + персональные данные → обязательный GDPR
- Строго регулируемая отрасль (финансовая, здравоохранение) → дополнительные отраслевые накладки

**Запуск** `framework_selector.py` чтобы применить правила принятия решений.

### 2. Сопоставление элементов управления между фреймворками { #2-cross-framework-control-mapping }

** Фреймворк:** для каждого выбранного фреймворка проанализируйте его библиотеку элементов управления; вычислите перекрытие с другими выбранными фреймворками.

**Для каждого объединенного управляющего выхода:**
- Достоверность отображения (ВЫСОКАЯ/ СРЕДНЯЯ/ НИЗКАЯ)
- Возможность повторного использования доказательств (один артефакт удовлетворяет N элементам управления)
- Цитирование по каждому фреймворку
- Руководство по внедрению, многократно используемое в разных фреймворках

** Самое плотное из известных совпадений: ** Приложение A ISO 27001 ↔ Критерии доверительных служб SOC 2 — исторически общий охват контроля составлял ~75%. Добавление стандарта ISO 42001 привносит элементы управления, специфичные для искусственного интеллекта; добавление GDPR привносит элементы, специфичные для конфиденциальности.

**Запуск** `cross_framework_mapper.py` с помощью библиотек управления фреймворком.

### 3. Имитация аудита { #3-audit-simulation }

** Фреймворк:** создайте реалистичный макет внутреннего аудита в соответствии со стандартами ISO 19011 + IIA IPPF.

**По каждому результату аудита:**
- 8-15 сценариев поиска в соответствии с типичной глубиной ISO 19011
- Распределение серьезности: ≥ 40% наблюдений/OFI, ≤ 15% критических/major (Ожидания IIA в отношении программ здорового образа жизни)
- Вопросы для собеседования на каждый контрольный предмет (3-5 вопросов на контрольный предмет)
- Список запросов на ревью документов
- Пошаговые запросы, где это применимо

**Запуск** `audit_simulator.py` с фреймворком + областью видимости.

### 4. Совокупность доказательств { #4-evidence-pool }

** Фреймворк:** консолидация требований к доказательствам в рамках включенных фреймворков; определение возможностей повторного использования.

**Выход:**
- Список артефактов-доказательств (например, журнал доступа-ревью, реестр рисков поставщика, журнал инцидентов)
- Для каждого артефакта: список кортежей (фреймворк, элемент управления), которым он удовлетворяет
- Оценка эффективности повторного использования (артефакт A удовлетворяет N элементам управления в M фреймворках)
- Оценка затрат на приобретение (затраты на производство + техническое обслуживание)

**Запуск** `evidence_pool_generator.py` с конфигурацией программы.

## Воркфлоу { #workflows }

### Воркфлоу 1: Загрузка программы (мульти-фреймворк, 4-8 недель) { #workflow-1-program-bootstrap-multi-framework-48-weeks }
**Цель:** разработать программу соответствия требованиям, охватывающую 2-4 фреймворка одновременно.

```bash
# 1. Run framework selector with company profile
python scripts/framework_selector.py profile.json
# 2. For each applicable framework, identify the per-framework skill and run its gap analysis
# 3. Run cross-framework mapper to identify reuse opportunities
python scripts/cross_framework_mapper.py control_libs.json
# 4. Run evidence pool generator to consolidate
python scripts/evidence_pool_generator.py program.json
# 5. Cross-check with cs-compliance-officer agent
# 6. Output: prioritized program backlog with owners + dates
```

### Воркфлоу 2: Календарь ежегодных аудитов (ежегодно) { #workflow-2-annual-audit-calendar-yearly }
**Цель:** спланировать циклы внутреннего аудита, охватывающие все применимые фреймворки.

```bash
# 1. Refresh framework selector if profile changed
python scripts/framework_selector.py profile.json
# 2. For each framework, run its internal-audit-plan tool
#    (e.g., aims_audit_scheduler.py for ISO 42001; isms_audit_scheduler.py for ISO 27001)
# 3. Coordinate the audit calendar across frameworks (auditor independence + capacity)
# 4. Run audit simulator for each framework to prep auditors
python scripts/audit_simulator.py scope.json
# 5. Output: integrated audit calendar with owners + auditor assignments
```

### Воркфлоу 3: Готовность к предварительной сертификации (в соответствии с новым фреймворком, 6-12 недель) { #workflow-3-pre-certification-readiness-per-new-framework-612-weeks }
**Цель:** подготовка к внешнему сертификационному аудиту.

```bash
# 1. Run gap analysis for the new framework
#    (ISO 42001: aims_gap_analyzer.py; ISO 27001: compliance_checker.py; SOC 2: gap_analyzer.py)
# 2. Run cross-framework mapper against already-certified frameworks
python scripts/cross_framework_mapper.py control_libs.json
# 3. Reuse evidence for HIGH-confidence mappings; build new for MEDIUM/LOW
# 4. Run audit simulator to dry-run the certification audit
python scripts/audit_simulator.py scope.json
# 5. Close remaining gaps before external auditor stage 1
```

### Воркфлоу 4: Консолидация пула фактических данных (ежеквартально) { #workflow-4-evidence-pool-consolidation-quarterly }
** Цель:** сохранять единый пул доказательств свежим и пригодным для повторного использования.

```bash
# 1. Refresh evidence pool generator
python scripts/evidence_pool_generator.py program.json
# 2. Identify HIGH-reuse-leverage artefacts (1 evidence -> 5+ controls)
# 3. Confirm evidence freshness (within retention requirement per framework)
# 4. Audit the evidence pool itself (no orphan controls, no stale evidence)
```

## Выходные стандарты { #output-standards }

```
**Bottom Line:** [one sentence — what's the multi-framework picture + biggest reuse opportunity]
**The Decision:** [one of: framework-set | overlap-map | audit-plan | evidence-consolidation]
**The Evidence:** [framework names + control IDs from the tool, not adjectives]
**How to Act:** [3 concrete next steps with owners + dates]
**Your Decision:** [the call only the compliance officer can make — which frameworks to pursue, audit cycle priority, evidence-reuse policy]
```

## Смежные скиллы { #adjacent-skills }

- `ra-qm-team/skills/iso42001-specialist/` — Глубокое погружение по стандарту ISO 42001 (в паре с плагином compliance-team-iso42001)
- `ra-qm-team/skills/eu-ai-act-specialist/` — Глубокое погружение EU AI Act (в паре с плагином compliance-team-eu-ai-act)
- `ra-qm-team/skills/information-security-manager-iso27001/` — ISO 27001 ISMS для глубокого погружения
- `ra-qm-team/skills/quality-manager-qms-iso13485/` — ISO 13485 СМК для глубокого погружения
- `ra-qm-team/skills/gdpr-dsgvo-expert/` — Глубокое погружение в GDPR
- `ra-qm-team/skills/soc2-compliance/` — SOC 2 глубокое погружение
- `ra-qm-team/skills/fda-consultant-specialist/` — Глубокое погружение FDA QSR
- `ra-qm-team/skills/mdr-745-specialist/` — EU MDR 745 для глубокого погружения
- `ra-qm-team/skills/risk-management-specialist/` — ISO 14971 для глубокого погружения
- `c-level-advisor/chief-ai-officer-advisor/` — Принятие управленческих решений о рисках с использованием искусственного интеллекта (сборка или покупка, выбор модели)
- `c-level-advisor/skills/general-counsel-advisor/` — Юридический ревью по новым делам

## Ссылки { #references }

- [compliance_os_pattern.md](references/compliance_os_pattern.md) — Архитектура мета-фреймворка (настройка → отображение → имитация → консолидация → ревью); когда использовать, а когда нет
- [cross_framework_overlap.md](references/cross_framework_overlap.md) — Таблица перекрытия фреймворков из 9 элементов × контрольных семейств с достоверностью отображения (фаза 3 расширяется до 12 фреймворков с помощью `cross_framework_mapper.py`)
- [audit_simulation_methodology.md](references/audit_simulation_methodology.md) — ISO 19011 + IIA IPPF + AICPA AT-C аудит-принципы моделирования + эвристика распределения серьезности
- [evidence_management.md](references/evidence_management.md) — Разработка пула доказательств + сохранение + свежесть + повторное использование -оценка эффективности использования
- [multi_framework_audit_playbook.md](references/multi_framework_audit_playbook.md) — Интегрированная программа аудита для 2+ фреймворков (фаза 2)
- [evidence_artifact_reuse_index.md](references/evidence_artifact_reuse_index.md) — Повторное использование, полученное эмпирическим путем -ранжирование рычагов воздействия во всех 12 фреймворках (фаза 3)

## Ресурс фазы 3: Библиотека сценариев макетного аудита { #phase-3-asset-mock-audit-scenario-library }

`assets/mock_audit_library.json` — 205 готовых сценариев поиска, охватывающих 12 фреймворков + 26 тем + 4 уровня серьезности (34 критических, 88 основных, 54 второстепенных, 29 наблюдательных). Каждый сценарий помечает применимые фреймворки; перекрестные ссылки `scripts/cross_framework_mapper.py` каталог объединенных элементов управления для определения идентификаторов элементов управления, специфичных для фреймворка. Используйте в качестве входных данных для обогащения `audit_simulator.py` имитационные аудиты в качестве учебного пособия для новых внутренних аудиторов или в качестве основы для выявления закономерностей в рамках программ с несколькими фреймворками.

---

**Версия:** 1.2.0
**Статус:** Производство готово
