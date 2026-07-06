---
title: "/ar:status — Экспериментальная Дашборд { #arstatus--experiment-dashboard } — Агентский скилл для Codex и OpenClaw"
description: "Покажите дашборд эксперимента с результатами, активными циклами и ходом выполнения. Используйте, когда пользователь запускает /ar:status или. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /ar:status — Экспериментальная Дашборд { #arstatus--experiment-dashboard }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `status`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/autoresearch-agent/skills/status/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


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
