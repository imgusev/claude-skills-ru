---
title: "Пакет рекомендаций уровня C — Индекс { #c-level-advisory-bundle--index } — Агентский скилл для руководителей"
description: "Индекс и маршрутизатор для консультативного пакета C-level: 33 скилла, охватывающих 14 ролей C-suite, оркестрацию, сквозные возможности и культуру. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Пакет рекомендаций уровня C — Индекс { #c-level-advisory-bundle--index }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `c-level-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/c-level-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


Это индекс пакета, а не советник. В нем рассказывается, что существует и с чего начать; приведенные ниже скиллы выполняют всю работу.

## Начните здесь { #start-here }

1. **Онбординг** — на `cs-onboard` скилл проводит собеседование с основателем (`/cs:setup`, 7 измерений, ~45 мин) и записывает `~/.claude/company-context.md`. Обновляйте ежеквартально с помощью `/cs:update`. Это каноническая контекстная схема, которую читает каждый советник.
2. **Спроси** — у `chief-of-staff` скилл направляет любой вопрос нужному консультанту (-ам). Смотрите его матрицу маршрутизации для всех 14 ролей.
3. **Важные решения** — the `board-meeting` скилл проводит ** 6-фазное** обсуждение: (1) сбор контекста → (2) независимые вклады (изолированные) → (3) критический анализ → (4) обобщение → (5) ревью основателя (полная остановка) → (6) принятие решения. Вызывается через `/cs:boardroom` в плагине c-level-агенты.
4. **Память** — решения принимаются в канонической двухслойной компоновке `~/.claude/decisions/{raw,approved}/` (см. [`agent-protocol/SKILL.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/agent-protocol/SKILL.md) → "Память принятия решений (каноническая компоновка)").

## Что входит в комплект (33 скилла) { #whats-in-the-bundle-33-skills }

** 14 ролей C-suite + критик (15): ** генеральный директор-советник, финансовый директор-советник, технический директор-советник, исполнительный директор-советник, cpo-советник, cmo-советник, cro-советник, ciso-советник, chro-советник, главный юрисконсульт-советник, руководитель отдела обработки данныхсотрудник-консультант, главный специалист по искусственному интеллекту-консультант, главный специалист по работе с клиентами-консультант, вице-президент-консультант — плюс критик-наставник руководителя (родственный плагин).

**Оркестрация (6): ** cs- онбординг, начальник штаба, заседание правления, регистратор решений, протокол агента, механизм контекста.

** Сквозные (6): ** доска-конструктор колод, сценарий-боевая комната, конкурентная разведка, организация-диагностика здоровья, ma-плейбук, международное расширение.

**Культура и сотрудничество (6):** архитектор культуры, операционная система компании, основатель-тренер, стратегическое согласование, управление изменениями, внутреннее повествование.

Плюс этот индекс (1). 37 инструментов Python только для stdlib и 68 справочных материалов по всему пакету.

## Краткий справочник по маршрутизации { #routing-quick-reference }

Полная матрица в [`chief-of-staff/SKILL.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/chief-of-staff/SKILL.md) и [`references/routing-matrix.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/chief-of-staff/references/routing-matrix.md). Основные роли: финансовый директор (капитал/burn), CRO (пайплайн/sales), CMO (позиционирование), CPO (дорожная карта/PMF), технический директор (архитектура), исполнительный директор (ops/OKRs), CHRO (люди), CISO (безопасность), GC (контракты/term таблицы), CDO (стратегия обработки данных/training-data права), CAIO (стратегия искусственного интеллекта/evals), технический директор (удержание/GRR), вице-президент (доставка/DORA), генеральный директор (направление). Многодоменный или необратимый → заседание правления.

## Связанные слои { #related-layers }

- [`c-level-advisor/c-level-agents`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents) — 13 cs-* агентов-персон + 21 `/cs:*` слэш-команды дополняют эти скиллы
- [`c-level-advisor/executive-mentor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/executive-mentor) — состязательный `/em:*` команды критика
- [`c-level-advisor/CLAUDE.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/CLAUDE.md) — полная схема архитектуры и руководство по интеграции
