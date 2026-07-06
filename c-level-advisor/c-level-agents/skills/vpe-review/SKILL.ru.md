---
name: "vpe-review"
description: "/cs:vpe-ревью <плана> — Пропускная способность - первый вице-президент по инженерным вопросам проводит опрос любого плана, который касается поставок, найма персонала, структуры команды или производственной дисциплины. Используйте, когда время цикла увеличивается, показатели DORA снижаются, или перед началом волны приема на работу в eng или реорганизации."
---

# /cs:vpe-review — VPE форсирует вопросы { #csvpe-review--vpe-forcing-questions }

**Команда:** `/cs:vpe-review <plan>`

Давление VPE, ориентированное в первую очередь на производительность, проверяет любой план, касающийся операций eng. Шесть вопросов перед выполнением любых обязательств по поставкам, расширением штата, реструктуризацией команды или изменением производственной дисциплины.

## Когда запускать { #when-to-run }

- Перед выполнением ежеквартальных обязательств по поставкам (планирование спринта, ревью OKR)
- Перед утверждением плана найма на работу в Англии
- До реструктуризации англоязычных команд (разделение/merging отряды, добавляющие племена)
- Прежде чем принимать решение о том, нанимать ли вице-президента отдельно от технического директора (или объединить их)
- Когда количество производственных инцидентов увеличивается
- Когда скорость спринта падает, но все говорят: "Мы усердно работаем".

## Шесть вопросов VPE { #the-six-vpe-questions }

### 1. Каково время цикла и где ожидает работа? { #1-whats-the-cycle-time-and-where-does-work-wait }
** Нет ДОРЫ - нет диагноза.**
- Время, необходимое для внесения изменений, является единственным лучшим показателем состояния здоровья
- Если вы не можете разложить время цикла на этапы, вы не сможете устранить узкое место
- Бежать `delivery_throughput_analyzer.py`

### 2. Каков уровень производительности DORA по всем 4 показателям? { #2-whats-the-dora-performance-level-on-all-4-metrics }
** Один элитный показатель и три низких = плохо. Четыре максимума = здоров.**
- Частота развертывания, время выполнения заказа, MTTR, частота отказов при изменении
- Наихудший показатель определяет общий уровень
- Сначала определите время выполнения заказа; все остальное последует за этим

### 3. Где происходит утечка в воронке найма? { #3-where-is-the-hiring-funnel-leaking }
** "Не могу найти хороших инженеров" - это неправильно.**
- На определенном этапе происходит чрезмерная фильтрация, или объем в верхней части воронки слишком мал, ИЛИ нарушено предложение к принятию
- Бежать `eng_hiring_funnel_calculator.py`
- Если предложение к принятию < 70%, то цена ниже рыночной или дисциплина закрытия слабая

### 4. Соответствует ли структура команды численности персонала? { #4-is-the-team-structure-healthy-for-the-headcount }
**5-9 ICs на команду; 5-8 ICs на EM; 4-6 EMs на директора.**
- Бежать `eng_team_structure_designer.py`
- Менеджер-триггер срабатывает, когда у 5+ микросхем нет выделенного EM
- Директор-триггер срабатывает, когда 3+ EMS отчитываются непосредственно перед VPE/техническим директором

### 5. Какова степень зрелости производственной дисциплины? { #5-whats-the-production-discipline-maturity }
** Уровень 1-5; стремитесь к уровню 3 на стадии роста.**
- Ротация по вызову ≥ 6 человек
- Реагирование на инцидент с учетом степени тяжести с безупречным вскрытием
- SLO по обслуживанию, ориентированному на клиента (в сочетании с `engineering/slo-architect/`)
- Непрерывное развертывание ИЛИ запланированное — не "обычно одно, иногда другое".

### 6. Добавляем ли мы VPE отдельно, или технический директор делает и то, и другое? { #6-are-we-adding-a-vpe-separately-or-is-cto-doing-both }
**Если технический директор тратит более 50% на управление по сравнению со стратегией, необходим VPE.**
- Или: дополнение VPE, когда технический директор является соучредителем, более комфортно относящимся к стратегии
- VPE владеет операционной моделью; технический директор владеет архитектурой
- В небольших масштабах (< 20 англ.) один человек может выполнять и то, и другое

## Воркфлоу { #workflow }

```bash
# 1. Delivery throughput
python ../../../skills/vpe-advisor/scripts/delivery_throughput_analyzer.py sprint_metrics.json

# 2. Hiring funnel
python ../../../skills/vpe-advisor/scripts/eng_hiring_funnel_calculator.py funnel.json

# 3. Team structure
python ../../../skills/vpe-advisor/scripts/eng_team_structure_designer.py team.json
```

## Выходной формат { #output-format }

```markdown
# VPE Review: <plan>
**Date:** YYYY-MM-DD

## The Decision Being Made
[throughput | hiring | structure | production | VPE-vs-CTO]

## Delivery Throughput (if applicable)
- DORA overall: Elite / High / Medium / Low
- Worst metric: <DF | LT | MTTR | FR>
- Bottleneck: <stage> (X% of cycle time)
- Top fix: <action + owner>

## Hiring Funnel (if applicable)
- End-to-end conversion: X%
- Weakest stage: <stage>
- Pipeline gap: +N candidates needed
- Top fix: <specific action>

## Team Structure (if applicable)
- Recommended: <informal pods / squads / tribes>
- Manager trigger fired: yes/no
- Director trigger fired: yes/no
- Action: <hire EM | hire director | split squad>

## Production Discipline (if applicable)
- Current maturity level: 1-5
- Next practice to add: <specific>
- SLO coverage: X / Y services

## Verdict
🟢 SHIP | 🟡 SHARPEN | 🔴 BLOCK

## Next Steps
[3 concrete actions]
```

## Маршрутизация { #routing }

- `/cs:cto-review` — по архитектурным причинам проблем с пропускной способностью
- `cs-chro-advisor` агент — для составления воронки найма/leveling проблемы
- `/cs:cfo-review` — для расчета стоимости аренды и бюджета на английском языке
- `/cs:ciso-review` — для соблюдения производственной дисциплины + перекрытие требований
- `/cs:decide` — зарегистрируйте вердикт
- `/cs:freeze 30` — о многолетних обязательствах по найму

## Связанный { #related }

- Агент: [`cs-vpe-advisor`](../../agents/cs-vpe-advisor.md)
- Скилл: [`vpe-advisor`](../../../skills/vpe-advisor/SKILL.md)
- Смежный: `../../../../engineering/slo-architect/`, `../../../../engineering/feature-flags-architect/`, `../../../../engineering/chaos-engineering/`

---

**Версия:** 1.0.0
