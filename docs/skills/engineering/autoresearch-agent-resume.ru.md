---
title: "/ar:resume — Возобновить эксперимент { #arresume--resume-experiment } — Агентский скилл для Codex и OpenClaw"
description: "Возобновите приостановленный эксперимент. Проверьте ветку эксперимента, прочитайте историю результатов, продолжайте итерацию. Используйте, когда. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /ar:resume — Возобновить эксперимент { #arresume--resume-experiment }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `resume`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/autoresearch-agent/skills/resume/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Возобновите приостановленный или ограниченный контекстом эксперимент. Считывает всю историю и продолжает с того места, на котором вы остановились.

## Использование { #usage }

```
/ar:resume                                  # List experiments, let user pick
/ar:resume engineering/api-speed            # Resume specific experiment
```

## Что он делает { #what-it-does }

### Шаг 1: Перечислите эксперименты, если это необходимо { #step-1-list-experiments-if-needed }

Если эксперимент не указан:

```bash
python {skill_path}/scripts/setup_experiment.py --list
```

Показывать статус для каждого (активного/paused/done на основании результатов.tsv возраст). Позвольте пользователю выбрать.

### Шаг 2: Загрузите полный контекст { #step-2-load-full-context }

```bash
# Checkout the experiment branch
git checkout autoresearch/{domain}/{name}

# Read config
cat .autoresearch/{domain}/{name}/config.cfg

# Read strategy
cat .autoresearch/{domain}/{name}/program.md

# Read full results history
cat .autoresearch/{domain}/{name}/results.tsv

# Read recent git log for the branch
git log --oneline -20
```

### Шаг 3: Сообщите о текущем состоянии { #step-3-report-current-state }

Подведите итог для пользователя:

```
Resuming: engineering/api-speed
  Target: src/api/search.py
  Metric: p50_ms (lower is better)
  Experiments: 23 total — 8 kept, 12 discarded, 3 crashed
  Best: 185ms (-42% from baseline of 320ms)
  Last experiment: "added response caching" → KEEP (185ms)

  Recent patterns:
  - Caching changes: 3 kept, 1 discarded (consistently helpful)
  - Algorithm changes: 2 discarded, 1 crashed (high risk, low reward so far)
  - I/O optimization: 2 kept (promising direction)
```

### Шаг 4: Задайте вопрос о следующем действии { #step-4-ask-next-action }

```
How would you like to continue?
  1. Single iteration (/ar:run)  — I'll make one change and evaluate
  2. Start a loop (/ar:loop)     — Autonomous with scheduled interval
  3. Just show me the results    — I'll review and decide
```

Если пользователь выбирает цикл, передайте `/ar:loop` с заранее выбранным экспериментом.
Если вы одиноки, передайте это кому-нибудь `/ar:run`.
