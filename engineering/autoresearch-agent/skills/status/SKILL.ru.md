---
name: "status"
description: "Покажите дашборд эксперимента с результатами, активными циклами и ходом выполнения. Используйте, когда пользователь запускает /ar:status или спрашивает, как проходит эксперимент с автоматическим поиском."
command: /ar:status
---

# /ar:status — Экспериментальная Дашборд { #arstatus--experiment-dashboard }

Отображать результаты экспериментов, активные циклы и прогресс во всех экспериментах.

## Использование { #usage }

```
/ar:status                                  # Full dashboard
/ar:status engineering/api-speed            # Single experiment detail
/ar:status --domain engineering             # All experiments in a domain
/ar:status --format markdown                # Export as markdown
/ar:status --format csv --output results.csv  # Export as CSV
```

## Что он делает { #what-it-does }

### Одиночный эксперимент { #single-experiment }

```bash
python {skill_path}/scripts/log_results.py --experiment {domain}/{name}
```

Также проверьте наличие активного цикла:
```bash
cat .autoresearch/{domain}/{name}/loop.json 2>/dev/null
```

Если цикл.json существует, покажите:
```
Active loop: every {interval} (cron ID: {id}, started: {date})
```

### Просмотр домена { #domain-view }

```bash
python {skill_path}/scripts/log_results.py --domain {domain}
```

### Полная дашборд { #full-dashboard }

```bash
python {skill_path}/scripts/log_results.py --dashboard
```

Для каждого эксперимента также проверяйте наличие файла цикла.json и показывайте статус цикла.

### Экспорт { #export }

```bash
# CSV
python {skill_path}/scripts/log_results.py --dashboard --format csv --output {file}

# Markdown
python {skill_path}/scripts/log_results.py --dashboard --format markdown --output {file}
```

## Пример вывода { #output-example }

```
DOMAIN          EXPERIMENT          RUNS  KEPT  BEST         CHANGE    STATUS   LOOP
engineering     api-speed            47    14   185ms        -76.9%    active   every 1h
engineering     bundle-size          23     8   412KB        -58.3%    paused   —
marketing       medium-ctr           31    11   8.4/10       +68.0%    active   daily
prompts         support-tone         15     6   82/100       +46.4%    done     —
```
