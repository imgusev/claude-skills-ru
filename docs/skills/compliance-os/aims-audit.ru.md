---
title: "/cs:aims-аудит — AIMS ISO 42001 Форсирует вопросы { #csaims-audit--aims-iso-42001-forcing-questions } — Плагин и агентский скилл для Claude Code"
description: "/cs:aims-аудит <область применения> — ISO/IEC 42001 AIMS внутренний аудит 6- принудительный опрос по вопросам. Используйте перед этапом сертификации. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:aims-аудит — AIMS ISO 42001 Форсирует вопросы { #csaims-audit--aims-iso-42001-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-shield-lock-outline: Compliance OS</span>
<span class="meta-badge">:material-identifier: `aims-audit`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/aims-audit/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install compliance-os</code>
</div>


**Команда:** `/cs:aims-audit <scope>`

Стандарт ISO 42001 нацелен на то, чтобы специалисты проверяли под давлением работу любой системы управления искусственным интеллектом. Шесть вопросов перед любым обязательством по сертификации, циклом внутреннего аудита или онбордингом новой системы.

## Когда запускать { #when-to-run }

- Перед этапом 1 сертификационного аудита ISO 42001
- Перед ежегодным циклом внутреннего аудита (пункт 9.2)
- При онбординге новой системы искусственного интеллекта в рамках существующих AIMS
- Если реестр рисков искусственного интеллекта не обновлялся более 6 месяцев
- После существенного изменения модели (повторная оценка рисков в соответствии с пунктом 6.1.2)
- Когда результаты аудита указывают на дублирование ЦЕЛЕЙ/СМИБ/СМК

## Вопросы о шести ЦЕЛЯХ { #the-six-aims-questions }

### 1. Дает ли определение области применения AIMS название каждой системе искусственного интеллекта? { #1-does-the-aims-scope-statement-name-every-ai-system }
**Упущение в области применения = вывод о сертификации.**
- В том числе: встроенные модели, сторонние сервисы искусственного интеллекта, "экспериментальные" производственные системы
- Бежать `aims_gap_analyzer.py` для проверки доказательств, предусмотренных пунктом 4.3
- "Функции искусственного интеллекта, добавленные поставщиками SaaS, которые мы используем" = в области применения, если они влияют на сервисы компании

### 2. Предусматривает ли политика в области искусственного интеллекта законное использование И полезные цели, А ТАКЖЕ человеческий надзор И постоянное совершенствование? { #2-does-the-ai-policy-commit-to-lawful-use-and-beneficial-purpose-and-human-oversight-and-continual-improvement }
**Отсутствие любого из четырех = критическое несоответствие на этапе 1.**
- Политика в области искусственного интеллекта не является политикой информационной безопасности - она имеет отдельное содержательное наполнение
- Ссылка на ISO 42001, приложение A.2.2 + пункт 5.2
- Маркетинговая копия "Этики искусственного интеллекта" не проходит

### 3. Каков охват регистра рисков и какие элементы управления в приложении А относятся к каждому риску? { #3-whats-the-risk-register-coverage-and-which-annex-a-controls-treat-each-risk }
**Идентификация риска без сопоставления элементов управления = пункт 6.1.3 не выполняется.**
- Бежать `ai_risk_register_builder.py` согласно методологии ISO 23894
- Каждый высокий/критический риск должен быть связан с ≥ 1 контролем, предусмотренным в приложении А
- "Остаточный вердикт: требуется дополнительное лечение" должен быть закрыт до этапа 1

### 4. Проводилась ли повторная оценка рисков ИИ с момента последнего изменения модели материала? { #4-has-the-ai-risk-assessment-been-re-run-since-the-last-material-model-change }
** Концептуальный дрифт - это не разовое событие.**
- Статья 9 Закона ЕС об ИИ + пункт 6.1.2 стандарта ISO 42001 требуют повторной оценки рисков
- Изменение материала = переподготовка на новых данных, тонкая настройка, изменение архитектуры, изменение контекста развертывания
- Если "мы сделали это 18 месяцев назад и до сих пор к этому не прикасались", то цель нарушена

### 5. Каков план внутреннего аудита, предусмотренный пунктом 9.2, и соблюдается ли независимость аудитора? { #5-whats-the-clause-92-internal-audit-plan-and-is-auditor-independence-respected }
**Без плана 9.2 AIMS является неполным.**
- Бежать `aims_audit_scheduler.py` с охватом + аудиторы + предыдущие выводы
- Аудит каждого пункта + применимое приложение A контроль за переходящим 3-летним циклом
- Один и тот же аудитор не может провести аудит собственной работы
- Перекрестная проверка с помощью cs-quality-regulatory при интеграции с программой аудита 13485

### 6. Были ли ЦЕЛИ интегрированы с существующими ISMS/СМК или создавались параллельно? { #6-has-the-aims-been-integrated-with-existing-isms--qms-or-built-in-parallel }
**Параллельные системы = 5-кратные текущие затраты на техническое обслуживание.**
- В 60% случаев в пунктах 4-10 доказательств повторно используется стандарт ISO 27001 /13485 с добавлением области применения искусственного интеллекта
- Цикл CAPA должен быть ОДНИМ циклом с несоответствиями, помеченными AI, а не отдельными
- Ссылка `cross_framework_mapping_ai.md` для карты повторного использования
- Перепроверьте с cs-ciso-advisor соответствие стандарту ISO 27001

## Воркфлоу { #workflow }

```bash
# 1. AIMS gap analysis
python ra-qm-team/skills/iso42001-specialist/scripts/aims_gap_analyzer.py evidence.json

# 2. AI risk register
python ra-qm-team/skills/iso42001-specialist/scripts/ai_risk_register_builder.py risks.json

# 3. Internal audit plan
python ra-qm-team/skills/iso42001-specialist/scripts/aims_audit_scheduler.py audit_scope.json

# 4. Cross-framework reuse map (via compliance-os)
python ../../skills/compliance-os/scripts/cross_framework_mapper.py program.json
```

## Выходной формат { #output-format }

```markdown
# AIMS Audit: <scope>
**Date:** YYYY-MM-DD

## The Decision Being Made
[gap-closure | risk-treatment | audit-scope | new-system-onboarding]

## Gap Analysis (Clauses 4-10)
- Weighted coverage: X%
- Critical gaps: N
- Major gaps: M
- Certification readiness: ready | stage_2_candidate | not_ready

## AI Risk Register
- Total risks: N
- By severity: critical=X, high=Y, medium=Z, low=W
- Requires additional treatment: K
- Top risk requiring action: <description>

## Clause 9.2 Audit Plan
- 12-month coverage: clauses=X, controls=Y
- Auditor independence: clean | issues
- Prior-year follow-up: scheduled in Q1

## Cross-Framework Reuse
- ISO 27001 evidence reused: % of AIMS Clauses 4-10
- 13485 evidence reused: % (if applicable)
- Net-new for AIMS: % (mostly Annex A)

## Verdict
🟢 STAGE-1-READY | 🟡 CLOSE-CRITICALS-FIRST | 🔴 NOT-READY

## Top 3 Actions
[3 concrete next steps with owner + date]
```

## Маршрутизация { #routing }

- `/cs:compliance-readiness` — для просмотра с несколькими фреймворками
- `/cs:ai-act-readiness` — если Закон ЕС об искусственном интеллекте также применяется
- `/cs:caio-review` — для принятия управленческих стратегических решений по ИИ
- `/cs:ciso-review` — для согласования кросс-фреймворка ISO 27001
- `/cs:decide` — для регистрации вердикта
- `/cs:freeze 30` — об обязательствах по сертификации

## Связанный { #related }

- Агент: [`cs-aims-iso42001`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/agents/cs-aims-iso42001.md)
- Скилл: [`iso42001-specialist`](https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team/skills/iso42001-specialist/SKILL.md)
- Смежный: [`skills/compliance-os`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/compliance-os), [`skills/ai-act-readiness`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/ai-act-readiness), [`skills/compliance-readiness`](https://github.com/imgusev/claude-skills-ru/tree/main/compliance-os/skills/compliance-readiness)

---

**Версия:** 1.0.0
