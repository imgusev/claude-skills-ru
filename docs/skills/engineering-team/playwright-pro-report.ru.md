---
title: "Интеллектуальный отчет о тестировании { #smart-test-reporting } — Агентский скилл и плагин Codex"
description: ">-. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Интеллектуальный отчет о тестировании { #smart-test-reporting }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `report`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/playwright-pro/skills/report/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Создавайте отчеты о тестировании, которые подключаются к существующему воркфлоу пользователя. Никаких новых инструментов.

## Шаги { #steps }

### 1. Запустите тесты (если они еще не запущены) { #1-run-tests-if-not-already-run }

Проверьте, существуют ли последние результаты тестирования:

```bash
ls -la test-results/ playwright-report/ 2>/dev/null
```

Если последних результатов нет, запустите тесты:

```bash
npx playwright test --reporter=json,html,list 2>&1 | tee test-output.log
```

### 2. Проанализируйте результаты { #2-parse-results }

Прочитайте отчет в формате JSON:

```bash
npx playwright test --reporter=json 2> /dev/null
```

Выдержка:
- Всего тестов, пройдено, не пройдено, пропущено, шелушащееся
- Продолжительность каждого теста и общее количество
- Имена неудачных тестов с сообщениями об ошибках
- Слоеные тесты (пройдены при повторной попытке)

### 3. Определите пункт назначения отчета { #3-detect-report-destination }

Проверьте, что настроено, и проложите маршрут автоматически:

| Проверьте | Если найден | Действие |
|---|---|---|
| `TESTRAIL_URL` env var | Настроенный тестовый рельс | Отправляйте результаты через `/pw:testrail push` |
| `SLACK_WEBHOOK_URL` env var | Настроенный провис | Опубликовать резюме в Slack |
| `.github/workflows/` | Действия на GitHub | Результаты переходят в PR-комментарий с помощью артефактов |
| `playwright-report/` | Репортер HTML | Откройте или отправьте отчет |
| Ничего из вышеперечисленного | Значение по умолчанию | Сгенерировать отчет о Markdown |

### 4. Сгенерируйте отчет { #4-generate-report }

#### Отчет Markdown (всегда генерируется) { #markdown-report-always-generated }

```markdown
# Test Results — {{date}}

## Summary
- ✅ Passed: {{passed}}
- ❌ Failed: {{failed}}
- ⏭️ Skipped: {{skipped}}
- 🔄 Flaky: {{flaky}}
- ⏱️ Duration: {{duration}}

## Failed Tests
| Test | Error | File |
|---|---|---|
| {{name}} | {{error}} | {{file}}:{{line}} |

## Flaky Tests
| Test | Retries | File |
|---|---|---|
| {{name}} | {{retries}} | {{file}} |

## By Project
| Browser | Passed | Failed | Duration |
|---|---|---|---|
| Chromium | X | Y | Zs |
| Firefox | X | Y | Zs |
| WebKit | X | Y | Zs |
```

Сохранить в `test-reports/{{date}}-report.md`.

#### Сводка Slack (если настроен Webhook) { #slack-summary-if-webhook-configured }

```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "🧪 Test Results: ✅ {{passed}} | ❌ {{failed}} | ⏱️ {{duration}}\n{{failed_details}}"
  }'
```

#### Нажатие тестового поручня (если настроено) { #testrail-push-if-configured }

Вызывать `/pw:testrail push` с результатами в формате JSON.

#### Отчет в формате HTML { #html-report }

```bash
npx playwright show-report
```

Или если в CI:
```bash
echo "HTML report available at: playwright-report/index.html"
```

### 5. Анализ тенденций (при наличии исторических данных) { #5-trend-analysis-if-historical-data-exists }

Если предыдущие отчеты существуют в `test-reports/`:
- Сравните скорость прохождения с течением времени
- Определите тесты, которые в последнее время стали ненадежными
- Выделите новые сбои в сравнении с повторяющимися сбоями

## Выход { #output }

- Резюме с пропуском/fail/skip/flaky подсчитывает
- Сведения о неудачном тестировании с сообщениями об ошибках
- Сообщить о подтверждении назначения
- Сравнение тенденций (при наличии исторических данных)
- Рекомендация к следующему действию (исправлять сбои или отмечать зеленый цвет)
