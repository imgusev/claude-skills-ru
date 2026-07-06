---
title: "/cs-webinar — слэш-команда для ИИ-агентов разработки"
description: "/cs:webinar — Вебинар и воркфлоу по маркетингу виртуальных мероприятий. Спланируйте вебинар с нуля (в обратном порядке от бизнес-цели), спасите того. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-webinar

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/cs-webinar.md">Источник</a></span>
</div>


**Команда:** `/cs:webinar [mode] [args]`

Тот `cs-webinar` команда - это ** точка входа для воркфлоу вебинара**: планирование → продвижение → запуск → контроль или диагностика → исправление → повторный запуск.

## Когда запускать { #when-to-run }

- Планируете вебинар, виртуальное мероприятие, живую демонстрацию, семинар, мастер-класс, беседу у камина или виртуальный саммит с нуля
- Спасение вебинара, количество участников которого разочаровало — низкая регистрация, низкая посещаемость или участники, которые не конвертируются
- Превращение одноразового вебинара в постоянно работающий механизм evergreen / on-demand
- Оцениваем существующую воронку, чтобы найти стадию, которая на самом деле нарушена

## Когда НЕ следует бегать { #when-not-to-run }

- Полный запуск продукта (не только вебинар) → использовать `/cs:launch` / стратегия запуска
- Общий жизненный цикл создания электронной почты, не связанной с событием → используйте `emails` скилл
- Личное участие - логистика мероприятий (место проведения, кейтеринг, стенд) → за рамками

## Режимы { #modes }

### `plan` — Спроектируйте все движение с нуля { #plan--design-the-whole-motion-from-scratch }

```bash
/cs:webinar plan
```

Отслеживает поступление, фиксирует формат promise +, определяет размер воронки в обратном направлении от бизнес-цели,
строит рекламную полосу и разрабатывает показ + от начала до конца + последующие действия. Предоставляет полный план
с использованием `marketing-skill/skills/webinar-marketing/templates/webinar-plan-template.md`.

### `rescue` — Диагностировать и исправить неэффективный вебинар { #rescue--diagnose-and-fix-an-underperforming-webinar }

```bash
/cs:webinar rescue --input funnel.json
```

Оценивает воронку, называет самый слабый этап и возвращает ранжированные исправления, нацеленные на фактическое узкое
место, а не на рефлексивное переписывание целевой страницы.

### `evergreen` — Преобразовать прошедший вебинар в "по запросу" { #evergreen--convert-a-past-webinar-to-on-demand }

```bash
/cs:webinar evergreen
```

Сопоставляет автоматизацию регистрации по запросу → просмотра → последующей деятельности с честным кадрированием в реальном времени и имитацией.

### `score` — Запустите воронкообразный счетчик напрямую { #score--run-the-funnel-scorer-directly }

```bash
/cs:webinar score --input funnel.json
/cs:webinar score                 # embedded sample data
```

## Минимальный прием (3 вопроса) { #minimal-intake-3-questions }

| Вопрос | Спрашивает | Когда |
|---|---|---|
| Вопрос 1 | Какой режим — планирование / спасение / вечнозеленый? | Всегда |
| Q2 | Бизнес-цель + действие по конверсии (лиды, пайплайн, внедрение, удержание, бренд)? | Всегда (управляет математикой обратной воронки) |
| Вопрос 3 | Температура аудитории (customers / warm / owned_cold / paid_cold)? | Всегда (выбирает контрольные показатели) |

Читать `marketing-context.md` во—первых, если он существует - он охватывает голос бренда, персонажей и язык клиентов,
поэтому вы спрашиваете только о том, что конкретно относится к данному мероприятию.

## Воркфлоу { #workflow }

```bash
# Mode: rescue / score — find the broken stage first
python3 marketing-skill/skills/webinar-marketing/scripts/webinar_funnel_scorer.py funnel.json
# → overall 0-100 score + per-stage rate vs. benchmark + named bottleneck

# Pipe JSON via stdin
cat funnel.json | python3 marketing-skill/skills/webinar-marketing/scripts/webinar_funnel_scorer.py -

# Demo on embedded sample data (no --help flag — run with no args)
python3 marketing-skill/skills/webinar-marketing/scripts/webinar_funnel_scorer.py
```

Ввод JSON (`registrations` + `attended_live` обязательно; остальное необязательно):

```json
{
  "invited": 5000, "page_visits": 1800, "registrations": 620,
  "attended_live": 180, "cta_clicks": 40, "conversions": 14,
  "audience": "owned_cold", "runtime_min": 45, "avg_watch_min": 26
}
```

## Математика воронки (планируйте в обратном порядке) { #the-funnel-math-plan-backward }

Всегда исходите из бизнес—цели в обратном направлении - это не позволяет никому отмечать 800 регистраций, в то время как 6 человек покупают:

```
Business goal:        20 sales-qualified opportunities
÷ attendee→SQO rate   (~10%)      → need 200 engaged attendees
÷ register→attend     (~35% live) → need ~570 registrations
÷ landing-page CVR     (~40%)     → need ~1,425 landing-page visits
→ promotion must drive ~1,425 qualified visits
```

Если требуемое количество посещений превышает доступную аудиторию, определите цель, формат или бюджет продвижения * сейчас*.

## Критерии оценки аудитории { #audience-benchmarks }

Система подсчета очков настраивается в зависимости от температуры аудитории (более теплая аудитория лучше преобразуется на каждом этапе).:

| Аудитория | Страница→Рег | Регистрация→Присутствовать | Присутствовать→CTA | Посещать→Конвертировать |
|---|---|---|---|---|
| `customers` | 40% | 50% | 25% | 12% |
| `warm` | 35% | 42% | 22% | 10% |
| `owned_cold` | 25% | 35% | 18% | 7% |
| `paid_cold` | 18% | 28% | 15% | 5% |

## Отклоненные анти-паттерны { #anti-patterns-rejected }

- Отмечаем регистрацию, в то время как показ или конверсия незаметно завершаются неудачей
- Переписывание целевой страницы, когда неработающая сцена открыта или готовится к закрытию
- Продвижение до определения размера воронки в обратном направлении от бизнес-цели
- Очевидный фейк-живое обрамление, подрывающее доверие аудитории
- Относитесь к вебинару как к событию, а не как к воронке

## Фразы-триггеры { #trigger-phrases }

- "спланируйте вебинар" / "стратегия проведения вебинара"
- "мой вебинар не конвертируется" / "низкая посещаемость"
- "продвижение вебинара" / "продолжение вебинара"
- "виртуальное мероприятие" / "живая демонстрация" / "мастер-класс" / "чат у камина" / "виртуальный саммит"
- "вебинар evergreen" / "вебинар по запросу"
- "воронка регистрации" / "уровень посещаемости"

## Связанный { #related }

- Агент: [`cs-webinar-marketer`](https://github.com/imgusev/claude-skills-ru/tree/main/agents/marketing/cs-webinar-marketer.md)
- Скилл: [`webinar-marketing`](https://github.com/imgusev/claude-skills-ru/tree/main/marketing-skill/skills/webinar-marketing/SKILL.md)
- Компаньон: `/cs:aeo` (получите вспомогательный контент, цитируемый поиском по искусственному интеллекту), стратегия запуска (полные запуски)

---

**Версия:** 2.9.0
**Лицензия:** Массачусетский технологический институт
