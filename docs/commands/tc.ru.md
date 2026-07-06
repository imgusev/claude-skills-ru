---
title: "/tc — слэш-команда для ИИ-агентов разработки"
description: "Отслеживайте технические изменения с помощью структурированных записей, конечного автомата и хэндоффа сеанса. Использование: /tc. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /tc

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/tc.md">Источник</a></span>
</div>


Отправьте команду TC (Техническое изменение). Аргументы: `$ARGUMENTS`.

Если `$ARGUMENTS` пусто, распечатайте это меню и остановите:

```
/tc init                       Initialize TC tracking in this project
/tc create <name>              Create a new TC record
/tc update <tc-id> [...]       Update fields, status, files, handoff
/tc status [tc-id]             Show one TC or the registry summary
/tc resume <tc-id>             Resume a TC from a previous session
/tc close <tc-id>              Transition a TC to deployed
/tc export                     Re-render derived artifacts
/tc dashboard                  Re-render the registry summary
```

В противном случае проанализируйте `$ARGUMENTS` как `<subcommand> <rest>` и отправьте по соответствующему протоколу, приведенному ниже. Все скрипты живут по адресу `engineering/tc-tracker/scripts/`.

## Подкоманды { #subcommands }

### `init` { #init }

1. Бежать:
   ```bash
   python3 engineering/skills/tc-tracker/scripts/tc_init.py --root . --json
   ```
2. Если статус равен `already_initialized`, сообщите текущую статистику и остановитесь.
3. В противном случае сообщите о том, что было создано, и предложите `/tc create <name>` в качестве следующего шага.

### `create <name>` { #create- }

1. Разобрать `<name>` как слизняк для шашлыка. Если он отсутствует, попросите его у пользователя.
2. Промпту пользователя (по одному вопросу за раз) для:
   - Название (5-120 символов)
   - Область применения: `feature | bugfix | refactor | infrastructure | documentation | hotfix | enhancement`
   - Приоритет: `critical | high | medium | low` (по умолчанию `medium`)
   - Краткое описание (более 10 символов)
   - Мотивация
3. Бежать:
   ```bash
   python3 engineering/skills/tc-tracker/scripts/tc_create.py --root . \
     --name "<slug>" --title "<title>" --scope <scope> --priority <priority> \
     --summary "<summary>" --motivation "<motivation>" --json
   ```
4. Сообщите новый идентификатор TC и путь к записи.

### `update <tc-id> [intent]` { #update--intent }

1. Если `<tc-id>` отсутствует, перечислите активные TCS (статус `in_progress` или `blocked`) из `tc_status.py --all` и спроси, какой именно.
2. Определите намерения пользователя на основе естественного языка:
   - **Изменение статуса** → `--set-status <state>` с `--reason "<why>"`
   - **Добавить файлы** → один или несколько `--add-file path[:action]`
   - **Добавить тест** → `--add-test "<title>" --test-procedure "<step>" --test-expected "<result>"`
   - **Обновить хэндофф** → любая комбинация `--handoff-progress`, `--handoff-next`, `--handoff-blocker`, `--handoff-context`
   - **Добавить примечание** → `--note "<text>"`
   - **Добавить тег** → `--tag <tag>`
3. Бежать:
   ```bash
   python3 engineering/skills/tc-tracker/scripts/tc_update.py --root . --tc-id <tc-id> [flags] --json
   ```
4. Если код выхода ненулевой, выведите сообщение об ошибке дословно. Конечный автомат и валидатор отклонят недопустимые ходы — не повторяйте слепо.

### `status [tc-id]` { #status-tc-id }

- Если `<tc-id>` предоставляется:
  ```bash
  python3 engineering/skills/tc-tracker/scripts/tc_status.py --root . --tc-id <tc-id>
  ```
- В противном случае:
  ```bash
  python3 engineering/skills/tc-tracker/scripts/tc_status.py --root . --all
  ```

### `resume <tc-id>` { #resume- }

1. Бежать:
   ```bash
   python3 engineering/skills/tc-tracker/scripts/tc_status.py --root . --tc-id <tc-id> --json
   ```
2. Отобразите блок хэндофф на видном месте: `progress_summary`, `next_steps` (пронумеровано), `blockers`, `key_context`.
3. Спросите: "Возобновить <tc-id> и перейти к следующему шагу 1? (y/n)"
4. Если да, запустите обновление, чтобы записать возобновление:
   ```bash
   python3 engineering/skills/tc-tracker/scripts/tc_update.py --root . --tc-id <tc-id> \
     --note "Session resumed" --reason "session handoff"
   ```
5. Начните выполнять первый пункт в `next_steps`. НЕ извлекайте контекст повторно — доверяйте хэндоффу.

### `close <tc-id>` { #close- }

1. Прочитайте запись с помощью `tc_status.py --tc-id <tc-id> --json`.
2. Убедитесь, что текущее состояние является `tested`. Если нет, откажитесь и сообщите пользователю, какие переходы все еще требуются.
3. Проверьте `test_cases`: предупреждать, если таковые имеются `pending`, `fail`, или `blocked`.
4. Спросите пользователя:
   - "Кто одобряет? (ваше имя или "я")"
   - "Примечания к официальному утверждению (необязательно):"
   - "Статус тестового покрытия: отсутствует / частичное / полное"
5. Бежать:
   ```bash
   python3 engineering/skills/tc-tracker/scripts/tc_update.py --root . --tc-id <tc-id> \
     --set-status deployed --reason "Approved by <approver>" --note "Approval: <approver> — <notes>"
   ```
   Затем непосредственно отредактируйте `approval` заблокируйте с помощью последующего обновления, если ваша версия скрипта поддерживает это; в противном случае попросите пользователя записать подтверждение в `notes`.
6. Отчет: "TC-NNN закрыт и депло -тирован".

### `export` { #export }

В этом скилле нет автоматического экспорта в HTML. Вместо этого перепроверьте все:

1. Ознакомьтесь с реестром.
2. Для каждой записи выполните:
   ```bash
   python3 engineering/skills/tc-tracker/scripts/tc_validator.py --record <path> --json
   ```
3. Бежать:
   ```bash
   python3 engineering/skills/tc-tracker/scripts/tc_validator.py --registry docs/TC/tc_registry.json --json
   ```
4. Отчет: общее количество проверенных записей, любые ошибки, пути к чему-либо недопустимому.

### `dashboard` { #dashboard }

Запустите сводку по всем записям:
```bash
python3 engineering/skills/tc-tracker/scripts/tc_status.py --root . --all
```

## Железные правила { #iron-rules }

1. **Никогда не редактируйте `tc_record.json` вручную.** Всегда используйте `tc_update.py` таким образом, добавляется история изменений и выполняется проверка.
2. **Никогда не пропускайте конечный автомат.** Продвигайтесь вперед по состояниям, даже если это кажется излишним.
3. ** Никогда не удаляйте TC.** История доступна только для добавления - добавьте окончательную редакцию и пометьте ее тегом `[CANCELLED]`.
4. **Справочная бухгалтерия.** В середине выполнения задачи запустите фоновый субагент для обновления TC. Не приостанавливайте кодирование, чтобы заняться бумажной работой.
5. ** Проверьте, прежде чем сообщать об успехе.** Если сценарий завершает работу с ненулевым значением, выявите ошибку и остановитесь.

## Связанные скиллы { #related-skills }

- `engineering/tc-tracker` — Полный SKILL.md со ссылкой на схему, диаграммами жизненного цикла и форматом хэндоффа.
- `engineering/changelog-generator` — Сопряжение с TC tracker: TCS для отслеживания аудита каждого изменения, журнал изменений для пользовательских заметок о выпуске.
- `engineering/tech-debt-tracker` — Для отслеживания долгосрочных долгов, а не дискретных изменений кода.
