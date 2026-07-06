---
title: "/cs:caio-review — КАЙО форсирует вопросы { #cscaio-review--caio-forcing-questions } — Агентский скилл для руководителей"
description: "/cs:caio-ревью <плана> — Оценка - требовательный опрос главного специалиста по ИИ любого плана, который включает ИИ: выбор модели, классификацию. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:caio-review — КАЙО форсирует вопросы { #cscaio-review--caio-forcing-questions }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `caio-review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/caio-review/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:caio-review <plan>`

Требовательный к оценке CAIO тестирует любой план, в котором задействован искусственный интеллект. Шесть вопросов перед выпуском любой функции искусственного интеллекта, любым многолетним обязательством поставщика или расширением команды искусственного интеллекта.

## Когда запускать { #when-to-run }

- Перед отправкой любой новой функции на базе искусственного интеллекта
- Перед подписанием многолетнего контракта с поставщиком искусственного интеллекта (API или автономная инфраструктура)
- До запуска в ЕС какой-либо функции искусственного интеллекта
- Перед наймом крупной команды по искусственному интеллекту (особенно инженера ML или ученого-исследователя)
- Перед выполнением обязательств по проекту тонкой настройки
- Прежде чем внедрять искусственный интеллект в регулируемой сфере (занятость, кредитование, здравоохранение, образование и т.д.)
- Когда основатель использует слово "искусственный интеллект" рядом с "конкурентным преимуществом" или "рвом"

## Шесть вопросов CAIO { #the-six-caio-questions }

### 1. В чем должен быть хорош этот искусственный интеллект, и как бы вы это оценили? { #1-what-does-this-ai-need-to-be-good-at-and-how-would-you-measure-it }
**Не установлено значение eval = не отправлено.** Прежде чем деплою какой-либо функции искусственного интеллекта, определите критерии оценки.
- минимум 50-100 репрезентативных входных данных
- Ожидаемые результаты ИЛИ рубрика для оценки
- Крайние случаи: неоднозначные, состязательные, граничащие с форматом
- Если вы не можете описать, как выглядит "хорошо", у вас нет функции; у вас есть атмосфера.

### 2. Каков уровень галлюцинаций/ошибок и каков запасной вариант? { #2-whats-the-slo-on-hallucination--error-rate-and-whats-the-fallback }
** Каждая функция искусственного интеллекта имеет режим сбоя. Планируйте это.**
- Количественный SLO: "<5% галлюцинаций по фактическим запросам"
- Механизм обнаружения: мониторинг, отбор проб, цикл обратной связи с клиентами
- Запасной вариант: ревью с участием человека в цикле, реакция по умолчанию с меньшим риском, отказ от ответа
- Радиус поражения при нарушении SLO: сколько пользователей пострадало, какова стоимость?

### 3. Каков уровень риска в соответствии с Законом ЕС об ИИ и требуется ли оценка соответствия? { #3-whats-the-risk-tier-under-eu-ai-act-and-is-conformity-assessment-required }
**Запуск `ai_risk_classifier.py` если затронуты какие-либо резиденты ЕС ИЛИ домен регулируется.**
- ЗАПРЕЩЕНО → не может быть запущено в ЕС; изменить сферу применения
- ВЫСОКИЙ уровень → оценка соответствия + регистрация в базе данных ЕС + 10 статей обязательств (3-12 месяцев, $50-200 тыс.)
- ОГРАНИЧЕННЫЕ → обязательства по прозрачности (раскрытие информации чат-ботом, маркировка контента, сгенерированного искусственным интеллектом)
- МИНИМАЛЬНЫЙ → никаких конкретных обязательств; NIST AI RMF добровольный

### 4. API, тонкая настройка или сборка? { #4-api-fine-tune-or-build }
**Запуск `model_buildvsbuy_calculator.py` для конкретного случая использования.**
- 80% случаев использования SaaS в B2B: API
- 15%: тонкая настройка (когда поведение зависит от домена + помеченные данные + команда ML + большой объем)
- <1%: сборка с нуля
- Решение должно учитывать экономическую безубыточность и практическую осуществимость (данные, команда, соответствие требованиям).

### 5. Какова траектория затрат на 12 месяцев при ожидаемом масштабе? { #5-whats-the-12-month-cost-trajectory-at-expected-scale }
**Запуск `ai_cost_economics.py` из-за рабочей нагрузки.**
- API: переменный, масштабируется линейно
- Автономный хостинг: в основном фиксированный, безубыточность обычно составляет 1-10B токенов/month для класса 70B
- Скрытые затраты на самостоятельный хостинг: операции, мониторинг, обновления моделей, пропускная способность, отработка отказа, безопасность
- Скрытые издержки API: привязка к поставщику, смещение возможностей, ограничения скорости, хранение данных
- Кэширование промптов - самый недооцененный рычаг; обратитесь в службу поддержки провайдера

### 6. Какая роль разблокирует это — и наняли ли мы предварительные условия в первую очередь? { #6-what-role-unblocks-this--and-have-we-hired-prerequisites-first }
** Привязать возможности искусственного интеллекта к конкретной роли. Основатели путают инженера по искусственному интеллекту / инженера по ML / ученого-исследователя.**
- Инженер по ИИ: прикладной + полный стек + промпты + оценки + развертывание (это нужно большинству стартапов)
- Инженер ML: тонкая настройка + переподготовка infra (только после инженера платформы + помеченные данные)
- Ученый-исследователь: модельное изобретение (только если модель является продуктом)
- Не нанимайте ученого—исследователя в качестве первого сотрудника по найму искусственного интеллекта - им нужна инфраструктура, чтобы быть продуктивными

## Воркфлоу { #workflow }

```bash
# 1. Model selection check
python ../../../skills/chief-ai-officer-advisor/scripts/model_buildvsbuy_calculator.py use_case.json

# 2. Regulatory classification
python ../../../skills/chief-ai-officer-advisor/scripts/ai_risk_classifier.py use_case.json

# 3. Cost projection
python ../../../skills/chief-ai-officer-advisor/scripts/ai_cost_economics.py workload.json
```

## Выходной формат { #output-format }

```markdown
# CAIO Review: <plan>
**Date:** YYYY-MM-DD

## The Decision Being Made
[one sentence — which CAIO decision: model selection | risk classification | economics | next hire]

## Eval Discipline
- Eval set committed: yes/no
- SLO defined: <metric> < <threshold>
- Fallback behavior: <one line>

## Model Selection (if applicable)
- Recommended: API / FINE_TUNE / BUILD
- 3-year TCO: $X (chosen path) vs $Y (alternatives)
- Breakeven: <volume>

## Risk Classification (if applicable)
- EU AI Act tier: PROHIBITED / HIGH / LIMITED / MINIMAL
- Conformity assessment required: yes/no
- US state triggers: [list]
- Required controls open: N

## Cost Economics (if applicable)
- Monthly cost at current volume: $X
- Breakeven for self-hosted migration: <volume>
- Migration cost if applicable: $X (3-6 months)

## Org (if applicable)
- Next hire: <role>
- Why this, not the alternative: <one line>
- Prerequisite hires in place: yes/no

## Verdict
🟢 SHIP | 🟡 SHARPEN | 🔴 BLOCK

## Next Steps
[3 concrete actions]
```

## Маршрутизация { #routing }

- `/cs:cdo-review` — для любого обучения-значение данных
- `/cs:gc-review` — для контрактов с поставщиками искусственного интеллекта, ответственности за результат, обучения -лицензирование данных
- `/cs:ciso-review` — для промпта внедрения / джейлбрейка / обучения -модель угрозы заражения данными
- `/cs:cfo-review` — для многолетних обязательств перед поставщиком или графическим процессором TCO
- `cs-chro-advisor` агент — для найма команды искусственного интеллекта (комп, лестница, прокачка)
- `/cs:decide` — зарегистрируйте вердикт
- `/cs:freeze 60` — о многолетних обязательствах в области искусственного интеллекта

## Связанный { #related }

- Агент: [`cs-caio-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/agents/cs-caio-advisor.md)
- Скилл: [`chief-ai-officer-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/chief-ai-officer-advisor/SKILL.md)
- Смежный: [`skills/chief-data-officer-advisor`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/chief-data-officer-advisor) (обучение правам на данные, стратегия обработки данных)

---

**Версия:** 1.0.0
