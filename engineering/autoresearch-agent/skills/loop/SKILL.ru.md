---
name: "loop"
description: "Запустите автономный цикл эксперимента с выбранным пользователем интервалом (10 минут, 1 час, ежедневно, еженедельно, ежемесячно). Использует CronCreate для планирования. Используется, когда пользователь запускает /ar:цикл или запрашивает непрерывный эксперимент с автоматическим поиском по расписанию."
command: /ar:loop
---

# /ar:loop — Цикл автономного эксперимента { #arloop--autonomous-experiment-loop }

Запустите повторяющийся цикл эксперимента, который выполняется с выбранным пользователем интервалом.

## Использование { #usage }

```
/ar:loop engineering/api-speed             # Start loop (prompts for interval)
/ar:loop engineering/api-speed 10m         # Every 10 minutes
/ar:loop engineering/api-speed 1h          # Every hour
/ar:loop engineering/api-speed daily       # Daily at ~9am
/ar:loop engineering/api-speed weekly      # Weekly on Monday ~9am
/ar:loop engineering/api-speed monthly     # Monthly on 1st ~9am
/ar:loop stop engineering/api-speed        # Stop an active loop
```

## Что он делает { #what-it-does }

### Шаг 1: Разрешите эксперимент { #step-1-resolve-experiment }

Если эксперимент не указан, перечислите эксперименты и позвольте пользователю выбрать.

### Шаг 2: Выберите интервал { #step-2-select-interval }

Если интервал не указан в качестве аргумента, укажите параметры:

```
Select loop interval:
  1. Every 10 minutes  (rapid — stay and watch)
  2. Every hour         (background — check back later)
  3. Daily at ~9am      (overnight experiments)
  4. Weekly on Monday   (long-running experiments)
  5. Monthly on 1st     (slow experiments)
```

Сопоставление с выражениями cron:

| Интервал | Выражение Cron | Стенография |
|----------|----------------|-----------|
| 10 минут | `*/10 * * * *` | `10m` |
| 1 час | `7 * * * *` | `1h` |
| Ежедневно | `57 8 * * *` | `daily` |
| Еженедельно | `57 8 * * 1` | `weekly` |
| Ежемесячно | `57 8 1 * *` | `monthly` |

### Шаг 3: Создайте повторяющееся задание { #step-3-create-the-recurring-job }

Использование `CronCreate` с помощью этой промпты (заполните детали эксперимента):

```
You are running autoresearch experiment "{domain}/{name}".

1. Read .autoresearch/{domain}/{name}/config.cfg for: target, evaluate_cmd, metric, metric_direction
2. Read .autoresearch/{domain}/{name}/program.md for strategy and constraints
3. Read .autoresearch/{domain}/{name}/results.tsv for experiment history
4. Run: git checkout autoresearch/{domain}/{name}

Then do exactly ONE iteration:
- Review results.tsv: what worked, what failed, what hasn't been tried
- Edit the target file with ONE change (strategy escalation based on run count)
- Commit: git add {target} && git commit -m "experiment: {description}"
- Evaluate: python {skill_path}/scripts/run_experiment.py --experiment {domain}/{name} --single
- Read the output (KEEP/DISCARD/CRASH)

Rules:
- ONE change per experiment
- NEVER modify the evaluator
- If 5 consecutive crashes in results.tsv, delete this cron job (CronDelete) and alert
- After every 10 experiments, update Strategy section of program.md

Current best metric: {read from results.tsv or "no baseline yet"}
Total experiments so far: {count from results.tsv}
```

### Шаг 4: Сохраните метаданные цикла { #step-4-store-loop-metadata }

Напишите в `.autoresearch/{domain}/{name}/loop.json`:

```json
{
  "cron_id": "{id from CronCreate}",
  "interval": "{user selection}",
  "started": "{ISO timestamp}",
  "experiment": "{domain}/{name}"
}
```

### Шаг 5: Подтвердите это пользователю { #step-5-confirm-to-user }

```
Loop started for {domain}/{name}
  Interval: {interval description}
  Cron ID: {id}
  Auto-expires: 3 days (CronCreate limit)

  To check progress: /ar:status
  To stop the loop:  /ar:loop stop {domain}/{name}

  Note: Recurring jobs auto-expire after 3 days.
  Run /ar:loop again to restart after expiry.
```

## Остановка цикла { #stopping-a-loop }

Когда пользователь запускает `/ar:loop stop {experiment}`:

1. Читать `.autoresearch/{domain}/{name}/loop.json` чтобы получить идентификатор cron
2. Вызов `CronDelete` с этим идентификатором
3. Удалить `loop.json`
4. Подтверждаю: "цикл остановлен на {experiment}. {n} эксперименты завершены."

## Важные ограничения { #important-limitations }

- **автоматическое истечение срока действия на 3 дня **: срок действия заданий CronCreate истекает через 3 дня. Для более длительных экспериментов пользователь должен повторно запустить `/ar:loop` для перезапуска. Результаты сохраняются — новый цикл начинается с того места, где прервался старый.
- **Один цикл на эксперимент**: Не запускайте несколько циклов для одного и того же эксперимента.
- ** Параллельные эксперименты **: Несколько экспериментов могут выполняться в цикле одновременно, только если они находятся в разных ветвях git (каковыми они являются по умолчанию — каждый эксперимент получает `autoresearch/{domain}/{name}`).
