---
title: "/cs:Онбординг — Интервью с основателем { #csonboard--founder-interview } — Агентский скилл для руководителей"
description: "/cs:онбординг — интервью с основателем, которое заполняет ~/.claude/company-context.md, используя каноническую 7-мерную схему cs-онбординг. Первая. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:Онбординг — Интервью с основателем { #csonboard--founder-interview }

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-level консультирование</span>
<span class="meta-badge">:material-identifier: `onboard`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/skills/onboard/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Команда:** `/cs:onboard`

Первая команда, выполняемая при внедрении агентов уровня c. Структурированное интервью с основателем, которое дает `~/.claude/company-context.md` — файл, который каждый советник cs-* читает перед ответом. Без этого советники строят догадки.

## К чему это приводит { #what-this-produces }

`~/.claude/company-context.md` — единый файл с достоверными фактами о компании. Прочитанный:
- `cs-chief-of-staff` (решения о маршруте)
- Каждый советник cs-* (контекст для любого вопроса)
- `/cs:brief` (допущения при принятии любого нового решения)

## Интервью (12 вопросов) { #the-interview-12-questions }

### Основы компании { #company-basics }
1. ** Название компании и текст из одного предложения.**
2. **Стадия:** предварительный посев / seed / Серия A / Серия B / Серия C+ / публичный
3. **Численность персонала:** всего, в разбивке по функциям (eng / product / GTM / ops / G&A)
4. **Географическое распределение:** Штаб-квартира + удаленное разделение, ключевые страны

### Бизнес-модель { #business-model }
5. **Модель получения дохода:** Подписка на SaaS / использование / транзакция / маркетплейс / оборудование / услуги
6. **ICP:** назовите одного реального клиента и опишите, что у него общего с другими
7. **ACV:** медиана и диапазон; количество сделок за последние 12 месяцев
8. ** Темпы роста:** В годовом исчислении; если до получения дохода, то ведущий показатель (пользователи, MAU и т.д.)

### Финансовое положение { #financial-posture }
9. **Взлетно-посадочная полоса:** месяцы наличных денег при текущем расходе; месяцы на случай банкротства
10. ** Последнее повышение:** сумма, оценка, ведущий инвестор, дата

### Стратегический контекст { #strategic-context }
11. **3 главных приоритета на текущий квартал** (простым языком)
12. ** Топ-3 рисков, из-за которых основатель теряет сон ** (будьте конкретны)

## Выходной формат { #output-format }

**Каноническая схема:** `~/.claude/company-context.md` находится в собственности [`cs-onboard`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/cs-onboard/SKILL.md) скилл и следует его 7-мерной схеме ([`templates/company-context-template.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/cs-onboard/templates/company-context-template.md)): Идентичность компании, Стадия и масштаб, Профиль основателя, Команда и культура, Рынок и конкуренция, Текущие вызовы, Цели и амбиции. Приведенные выше 12 вопросов представляют собой более быстрый структурированный ввод, который заполняет тот же файл — Личность / Бизнес / Финансы → Стадия и масштаб, Команда → Команда и культура, Квартальные приоритеты / риски → Текущие задачи + Цели и амбиции. Писать `[not captured]` для измерений, которых не достигает быстрый ввод (профиль основателя, рынок и конкуренция); запустите полный `cs-onboard` собеседование, чтобы заполнить их. Никогда не создавайте второй контекстный файл или другой макет.

Краткое содержание приема, отраженное в 12 вопросах:

```markdown
# Company Context
**Generated:** YYYY-MM-DD
**Last updated:** YYYY-MM-DD

## Identity
- **Company:** <name>
- **Pitch:** <one sentence>
- **Stage:** <stage>
- **HQ + remote:** <distribution>

## Business
- **Model:** <type>
- **ICP:** <description + named customer>
- **ACV:** $<median> (range $<low> - $<high>)
- **Deal count (LTM):** N
- **ARR growth (YoY):** X%

## Financial
- **Cash on hand:** $<amount>
- **Net burn (monthly):** $<amount>
- **Runway base:** N months
- **Runway bear:** N months
- **Last raise:** $<amount> at $<post> in <month YYYY>, led by <investor>

## Team
- **Total headcount:** N
- **Eng:** N | Product: N | GTM: N | Ops: N | G&A: N

## Quarter
- **Top priorities (Q<X> YYYY):**
  1. <priority>
  2. <priority>
  3. <priority>

- **Top risks:**
  1. <risk>
  2. <risk>
  3. <risk>

## Routing Hints
[Optional: any role the founder wants to use sparingly or rely on heavily]
```

## Воркфлоу { #workflow }

1. Ответьте основателю на все 12 вопросов
2. Цитируйте собственные слова основателя везде, где это возможно (не перефразируйте ICP).
3. Сохранить в `~/.claude/company-context.md`
4. (Необязательно) Если настроен мост llm-wiki: символическая ссылка на хранилище
   ```bash
   ln -sf ~/company-vault/00-meta/company-context.md ~/.claude/company-context.md
   ```
5. Подтвердите с основателем: прочитайте файл еще раз, спросите: "Чего-нибудь не хватает?"

## Когда следует выполнить повторный запуск { #when-to-re-run }

- После сбора средств (цифры меняются)
- После крупного поворота или запуска продукта
- Спустя более 6 месяцев (большинство фактов утеряно)
- После крупного найма (изменения в распределении команд)
- Всегда перед `/cs:boardroom` для принятия решения с высокими ставками

## Настойчивость { #persistence }

По умолчанию, `~/.claude/company-context.md` является локальным для компьютера основателя. Чтобы сделать его постоянным на разных машинах / доступным для совместного использования:

- **Хранилище Markdown (рекомендуется):** смотрите [[`references/llm-wiki-bridge.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md)](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md)
- ** Зашифрованная синхронизация точечных файлов:** возраст + git
- ** Общая команда:** хранить в частном репозитории символическую ссылку из `~/.claude/`

## Связанный { #related }

- Скилл: [`cs-onboard`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/cs-onboard/SKILL.md) — основной протокол собеседования
- Скилл: [`context-engine`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/skills/context-engine/SKILL.md) — считывает этот файл
- Ссылка: [[`references/llm-wiki-bridge.md`](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md)](https://github.com/imgusev/claude-skills-ru/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md)

---

**Версия:** 1.0.0
