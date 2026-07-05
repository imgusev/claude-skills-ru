---
title: "/cs:соответствие требованиям-готовность — Сотрудник по соблюдению требований форсирует вопросы { #cscompliance-readiness--compliance-officer-forcing-questions } — Плагин и агентский скилл для Claude Code"
description: "/cs:compliance-readiness <программа> — сотрудник по комплаенсу с несколькими фреймворками 6 - принудительный опрос любой программы комплаенс. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:соответствие требованиям-готовность — Сотрудник по соблюдению требований форсирует вопросы { #cscompliance-readiness--compliance-officer-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-shield-lock-outline: Compliance OS</span>
<span class="meta-badge">:material-identifier: `compliance-readiness`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/compliance-readiness/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install compliance-os</code>
</div>


**Команда:** `/cs:compliance-readiness <program>`

Специалист по комплаенсу с несколькими фреймворками проводит проверку любой программы соответствия требованиям. Шесть вопросов перед любым принятием новых обязательств по фреймворку, планированием цикла аудита или подтверждением готовности к сертификации.

## Когда запускать { #when-to-run }

- Прежде чем внедрять новую фреймворк соответствия требованиям
- До завершения составления календаря ежегодного аудита
- Перед сертификацией этап 1 - подтверждение готовности
- До проведения ревью руководством (пункт 9.3 во всех фреймворках)
- Когда усилия по сбору доказательств выросли более чем на 50% в годовом исчислении (запах)
- Когда в результате аудита было получено более 15% критических выводов

## Шесть вопросов сотрудника по соблюдению требований { #the-six-compliance-officer-questions }

### 1. Назвали ли вы все применимые фреймворки? { #1-have-you-named-every-applicable-framework }
**Нет запуска селектора фреймворка, нет защищаемой области.**
- Бежать `framework_selector.py` с профилем компании
- Забвение фреймворка означает последующую перестройку программы аудита
- Обратите внимание на отраслевые накладки (финансовые: NYDFS, FINMA; здравоохранение: HIPAA, ISO 13485; AI: ISO 42001 + Закон ЕС об искусственном интеллекте).

### 2. Где пересекаются фреймворки и каковы преимущества повторного использования? { #2-where-do-the-frameworks-overlap-and-whats-the-reuse-leverage }
**Единое доказательство -> N средств контроля = краеугольный камень эффективности многоуровневых фреймворков.**
- Бежать `cross_framework_mapper.py` с включенными фреймворками
- Сопоставления с высокой степенью достоверности: те же доказательства; СРЕДНЯЯ: существующие + наложение; НИЗКАЯ: новый артефакт
- Без анализа совпадений вы будете собирать одни и те же записи о доступе-ревью 3 раза

### 3. Кому принадлежит каждый артефакт и каков коэффициент полезного использования при повторном использовании? { #3-who-owns-each-artefact-and-whats-the-reuse-leverage-score }
**Совместное владение без подотчетности является наиболее распространенной причиной устаревания доказательств.**
- Бежать `evidence_pool_generator.py` для инвентаризации артефактов
- Артефакты с высоким коэффициентом использования (≥ 5 отображений) создаются первыми
- Каждому артефакту нужен один ответственный владелец
- Устаревшие свидетельства — это эффективный пробел, даже если артефакт существовал исторически

### 4. Каков график проведения аудита и соблюдается ли независимость аудитора? { #4-whats-the-audit-calendar-and-is-auditor-independence-respected }
**Проведение надзорных аудитов в течение одной недели - это неприятный запах.**
- Используйте инструменты планирования аудита для каждого фреймворка (aims_audit_scheduler, isms_audit_scheduler, audit_schedule_optimizer)
- Аудитор не может проводить аудит своей собственной работы (пункт 9.2 во всех стандартах ISO)
- Для небольших команд: ротация аудиторов + случайный внешний аудитор

### 5. Что дает имитационный аудит и является ли распределение серьезности правильным? { #5-what-does-a-mock-audit-produce-and-is-the-severity-distribution-healthy }
**Нет имитационного аудита, нет сигнала готовности.**
- Бежать `audit_simulator.py` с фреймворком + областью применения
- Здоровое распределение: ≥ 40% наблюдений, ≤ 15% критических
- Все критические выводы = деструктивный аудит ИЛИ действительно провальная программа.
- Результаты всех наблюдений = слишком поверхностный аудит

### 6. Какова частота проведения ревью руководством в разных фреймворках? { #6-whats-the-management-review-cadence-across-frameworks }
**Каждому фреймворку требуется свой собственный управленческий ревью; интегрированный ревью (согласно приложению SL) экономит время выполнения в 5 раз.**
- Запланируйте один ежеквартальный кросс-фреймворк-ревью, охватывающий все включенные фреймворки, раздел 9.3 входных данных
- Исходные данные: изменения в реестре рисков, открытые несоответствия, результаты аудита, инциденты, дрейф, ключевые показатели эффективности.
- Результаты: пункты действий, решения о ресурсах, корректировки сферы охвата

## Воркфлоу { #workflow }

```bash
# 1. Framework selection
python ../../skills/compliance-os/scripts/framework_selector.py profile.json

# 2. Cross-framework overlap
python ../../skills/compliance-os/scripts/cross_framework_mapper.py program.json

# 3. Evidence pool consolidation
python ../../skills/compliance-os/scripts/evidence_pool_generator.py program.json

# 4. Mock audit (per framework)
python ../../skills/compliance-os/scripts/audit_simulator.py scope.json
```

## Выходной формат { #output-format }

```markdown
# Compliance Readiness: <program>
**Date:** YYYY-MM-DD

## The Decision Being Made
[framework-set | audit-calendar | certification-readiness | evidence-consolidation]

## Framework Set
- Applicable: <list>
- Binding (regulations): <count>
- Certifiable: <count>
- Missing dependencies: <list>

## Cross-Framework Overlap
- Total merged controls in scope: N
- High-leverage artefacts (≥ 5 mappings): M
- Top reuse opportunities: <top 5 artefacts>

## Evidence Pool
- Artefacts in catalog: N
- High-leverage count: M
- Stale evidence rate: X%
- Unowned artefacts: K

## Audit Calendar
- Frameworks scheduled this year: <list>
- Auditor independence respected: Y/N
- Conflicts: <list>

## Mock Audit Results (per framework)
- <framework>: total findings N, critical X%, observation Y%, healthy distribution: Y/N

## Verdict
🟢 READY | 🟡 STAGE-2-CANDIDATE | 🔴 NOT-READY

## Top 3 Actions
[3 concrete next steps with owners + dates]
```

## Маршрутизация { #routing }

- `/cs:aims-audit` — для форсирующих вопросов, специфичных для стандарта ISO 42001
- `/cs:ai-act-readiness` — для форсирующих вопросов, специфичных для Закона ЕС об ИИ
- `/cs:ciso-review` — для стратегии кибербезопасности
- `/cs:caio-review` — для исполнительной стратегии искусственного интеллекта
- `/cs:gc-review` — для юридического ревью по новому делу
- `/cs:decide` — для регистрации вердикта
- `/cs:freeze 30` — об обязательствах по сертификации (многолетние финансовые последствия)

## Связанный { #related }

- Агент: [`cs-compliance-officer`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/agents/cs-compliance-officer.md)
- Скилл: [`compliance-os`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/compliance-os/SKILL.md)
- Смежный: `ra-qm-team/skills/iso42001-specialist/`, `ra-qm-team/skills/eu-ai-act-specialist/`, `ra-qm-team/skills/information-security-manager-iso27001/`, `ra-qm-team/skills/soc2-compliance/`, `ra-qm-team/skills/gdpr-dsgvo-expert/`

---

**Версия:** 1.0.0
