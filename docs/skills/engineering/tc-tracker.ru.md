---
title: "Трекер TC { #tc-tracker } — Агентский скилл для Codex и OpenClaw"
description: "Используйте, когда пользователь просит отслеживать технические изменения, создавать записи изменений, управлять жизненными циклами TC или передавать. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Трекер TC { #tc-tracker }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `tc-tracker`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/tc-tracker/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Отслеживайте каждое изменение кода со структурированными записями JSON, принудительным автоматом состояний и форматом хэндоффа сеанса, который позволяет новому сеансу искусственного интеллекта возобновлять работу без сбоев по истечении срока действия предыдущего.

## Обзор { #overview }

Техническое изменение (TC) - это структурированная запись, которая фиксирует ** что** изменилось, **почему** это изменилось, **кто** это изменил, ** когда** это изменилось, ** как это было протестировано** и **на каком этапе находится работа** для следующего сеанса. Записи хранятся в формате JSON в `docs/TC/` внутри целевого проекта, проверенного на соответствие строгой схеме и конечному автомату.

**Используйте этот скилл, когда пользователь:**
- Просит "отследить это изменение" или хочет получить журнал аудита изменений кода
- Хочет перенести текущую работу на будущую сессию искусственного интеллекта
- Нужны структурированные примечания к выпуску, которые выходят за рамки сообщений о фиксации
- онбординг существующего проекта и хочет получить документацию об изменениях, имеющую обратную силу
- Просит о `/tc init`, `/tc create`, `/tc update`, `/tc status`, `/tc resume`, или `/tc close`

**Не используйте этот скилл, когда:**
- Пользователю нужен только список изменений из истории git (используйте `engineering/changelog-generator`)
- Пользователь хочет отслеживать только элементы технического долга (используйте `engineering/tech-debt-tracker`)
- Изменение тривиально (опечатка, форматирование) и не повлияет на поведение

## Расположение хранилища { #storage-layout }

Каждый проект хранит TCS по адресу `{project_root}/docs/TC/`:

```
docs/TC/
├── tc_config.json          # Project settings
├── tc_registry.json        # Master index + statistics
├── records/
│   └── TC-001-04-05-26-user-auth/
│       └── tc_record.json  # Source of truth
└── evidence/
    └── TC-001/             # Log snippets, command output, screenshots
```

## Соглашение об идентификаторе TC { #tc-id-convention }

- **Родительский TC:** `TC-NNN-MM-DD-YY-functionality-slug` (например,, `TC-001-04-05-26-user-authentication`)
- **Суб-ТК:** `TC-NNN.A` или `TC-NNN.A.1` (буква = редакция, цифра = дополнительная редакция)
- `NNN` является последовательным, `MM-DD-YY` это дата создания, slug - футляр для кебаба.

## Государственная машина { #state-machine }

```
planned -> in_progress -> implemented -> tested -> deployed
   |            |              |           |          |
   +-> blocked -+              +- in_progress <-------+
        |                          (rework / hotfix)
        +-> planned
```

> Видишь [ссылки/lifecycle.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/tc-tracker/references/lifecycle.md) для получения полной таблицы переходов и потоков восстановления.

## Команды воркфлоу { #workflow-commands }

Скилл содержит пять скриптов на Python, которые выполняют детерминированные операции только с stdlib над записями TC. Каждый из них поддерживает `--help` и `--json`.

### 1. Инициализируйте отслеживание в проекте { #1-initialize-tracking-in-a-project }

```bash
python3 scripts/tc_init.py --project "My Project" --root .
```

Создает `docs/TC/`, `docs/TC/records/`, `docs/TC/evidence/`, `tc_config.json`, и `tc_registry.json`. Idempotent — повторный запуск отчетов, "уже инициализированных", с текущей статистикой.

### 2. Создайте новую запись TC { #2-create-a-new-tc-record }

```bash
python3 scripts/tc_create.py \
  --root . \
  --name "user-authentication" \
  --title "Add JWT-based user authentication" \
  --scope feature \
  --priority high \
  --summary "Adds JWT login + middleware" \
  --motivation "Required for protected endpoints"
```

Генерирует следующий последовательный идентификатор TC, создает каталог записей, записывает полностью заполненный `tc_record.json` (статус `planned`, Редакция создания R1) и обновляет реестр.

### 3. Обновите запись TC { #3-update-a-tc-record }

```bash
# Status transition (validated against the state machine)
python3 scripts/tc_update.py --root . --tc-id TC-001-04-05-26-user-auth \
  --set-status in_progress --reason "Starting implementation"

# Add a file
python3 scripts/tc_update.py --root . --tc-id TC-001-04-05-26-user-auth \
  --add-file src/auth.py:created

# Append handoff data
python3 scripts/tc_update.py --root . --tc-id TC-001-04-05-26-user-auth \
  --handoff-progress "JWT middleware wired up" \
  --handoff-next "Write integration tests" \
  --handoff-next "Update README"
```

Каждое изменение добавляет последовательный `R<n>` запись о пересмотре, обновляет `updated`, и повторно проверяет соответствие схеме перед записью атомарно (`.tmp` затем переименуйте).

### 4. Просмотр статуса { #4-view-status }

```bash
# Single TC
python3 scripts/tc_status.py --root . --tc-id TC-001-04-05-26-user-auth

# All TCs (registry summary)
python3 scripts/tc_status.py --root . --all --json
```

### 5. Подтвердите запись или реестр { #5-validate-a-record-or-registry }

```bash
python3 scripts/tc_validator.py --record docs/TC/records/TC-001-.../tc_record.json
python3 scripts/tc_validator.py --registry docs/TC/tc_registry.json
```

Валидатор применяет схему, проверяет законность конечного автомата, проверяет последовательный `R<n>` и `T<n>` Идентификаторы и подтверждает согласованность утверждения (`approved=true` требует `approved_by` и `approved_date`).

> Видишь [ссылки/tc-schema.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/tc-tracker/references/tc-schema.md) для получения полной схемы.

## Косая черта - Диспетчер команд { #slash-command-dispatcher }

Репозиторий отправляет `/tc` слэш-команда в `commands/tc.md` который отправляется этим скриптам на основе подкоманды:

| Команда | Действие |
|---------|--------|
| `/tc init` | Бежать `tc_init.py` для текущего проекта |
| `/tc create <name>` | Промпт для полей, запустите `tc_create.py` |
| `/tc update <tc-id>` | Примените изменения, описанные пользователем, с помощью `tc_update.py` |
| `/tc status [tc-id]` | Бежать `tc_status.py` |
| `/tc resume <tc-id>` | Отобразить хэндофф, заархивировать предыдущую сессию, начать новую |
| `/tc close <tc-id>` | Переход к `deployed`, установленное утверждение |
| `/tc export` | Повторный рендеринг всех производных артефактов |
| `/tc dashboard` | Повторно отобразите сводку реестра |

Слэш-команда - это пользовательский интерфейс; скрипты Python - это движок.

## Формат Хэндоффа сессии { #session-handoff-format }

Блок хэндофф находится по адресу `session_context.handoff` внутри каждого TC и является единственной наиболее важной областью для непрерывности ИИ. Он содержит:

- `progress_summary` — что было сделано
- `next_steps` — упорядоченный список оставшихся действий
- `blockers` — что-либо, препятствующее прогрессу
- `key_context` — критические решения, ошибки, шаблоны, которые должен знать следующий бот
- `files_in_progress` — редактируемые файлы и их состояние (`editing`, `needs_review`, `partially_done`, `ready`)
- `decisions_made` — архитектурные решения с обоснованием и временной меткой

> Видишь [ссылки/handoff-format.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/tc-tracker/references/handoff-format.md) ознакомьтесь с полной структурой и правилами заполнения.

## Правила проверки (всегда применяются) { #validation-rules-always-enforced }

1. **Конечный автомат** — разрешены только допустимые переходы.
2. **Последовательные идентификаторы** — `revision_history` использует `R1, R2, R3...`; `test_cases` использует `T1, T2, T3...`.
3. ** История только для добавления ** - записи о ревизиях никогда не изменяются и не удаляются.
4. **Согласованность утверждений** — `approved=true` требует `approved_by` и `approved_date`.
5. **Формат идентификатора TC** — должен совпадать `TC-NNN-MM-DD-YY-slug`.
6. **Формат идентификатора суб-TC** — должен соответствовать `TC-NNN.A` или `TC-NNN.A.N`.
7. **Атомарные записи** — JSON записывается в `.tmp` затем переименован.
8. ** Статистика реестра** — пересчитывается при каждой записи в реестр.

## Неблокирующая схема ведения бухгалтерского учета { #non-blocking-bookkeeping-pattern }

Отслеживание TC не должно прерывать основной воркфлоу.

- ** Никогда не останавливайтесь для обновления встроенных записей TC. ** Продолжайте кодировать.
- На естественных этапах создайте фоновый субагент для обновления записи.
- Задавайте вопросы только тогда, когда это действительно необходимо ("Эта работа не соответствует ни одному активному TC — создайте его?"), и задавайте один раз за сеанс, а не за файл.
- В конце сеанса напишите заключительный блок хэндоффа перед закрытием.

## Ретроактивное массовое создание { #retroactive-bulk-creation }

Для онбординга существующего проекта с недокументированной историей создайте `retro_changelog.json` (одна запись на каждое логическое изменение) и передайте ее в `tc_create.py` в цикле или расширьте сценарий для пакетного режима. Группируйте фиксации по функциям, а не по файлам.

## Анти-паттерны { #anti-patterns }

| Анти-паттерн | Почему это плохо | Сделайте это вместо этого |
|--------------|--------------|-----------------|
| Редактирование `revision_history` чтобы "исправить" опечатку | История доступна только для добавления — вмешательство уничтожает след аудита | Добавьте новую редакцию, которая исправляет поле |
| Пропуск конечного автомата ("просто установите статус на деплою") | Обходит проверку и скрывает пропущенные этапы | Пройдите через `in_progress -> implemented -> tested -> deployed` |
| Создание одного TC для каждого измененного файла | Фрагментирует связанную работу и взрывает реестр | Один TC на логическую единицу (функция, исправление, рефакторинг) |
| Обновление встроенного TC между каждым редактированием кода | Замедляет работу основного агента, растрачивает контекст впустую | Создайте фонового субагента в milestones |
| Маркировка `approved=true` без `approved_by` | Валидатор отклонит; вводящий в заблуждение след аудита | Всегда устанавливайте `approved_by` и `approved_date` вместе |
| Перезапись `tc_record.json` непосредственно с помощью текстового редактора | Риск повреждения в середине записи и пропуск проверки | Использование `tc_update.py` (атомарная запись + проверка схемы) |
| Вкладывать секреты в `notes` или доказательства | Записи передаются в репозиторий | Ссылайтесь на env var или внешнее секретное хранилище |
| Повторное использование идентификаторов TC после удаления | Нарушает последовательную гарантию и запутывает историю | Увеличивайте только вперед — никогда не перерабатывайте |
| Позволяя `next_steps` становятся несвежими | Противоречит цели хэндоффа | Обновляйте информацию о каждом этапе, даже если это "ничего не изменилось". |

## Перекрестные ссылки { #cross-references }

- `engineering/changelog-generator` — Генерирует заметки о выпуске журнала изменений Keep-a-Changelog из обычных коммитов. Соедините его с TC tracker: TC для детального отслеживания аудита каждого изменения, changelog для пользовательских заметок о выпуске.
- `engineering/tech-debt-tracker` — Для отслеживания долгоживущих статей долга, а не отдельных изменений кода.
- `engineering/focused-fix` — Когда исправление ошибки требует систематического исправления по всему функционалу, запустите `/focused-fix` сначала затем зафиксируйте результат в виде TC.
- `project-management/decision-log` — Архитектурные решения, принятые внутри торгового центра `decisions_made` блок также может быть добавлен в журнал принятия решений по всему проекту.
- `engineering-team/code-reviewer` — Ревью перед объединением естественным образом вписывается в `tested -> deployed` переход; запечатлеть рецензента в `approval.approved_by`.

## Ссылки на этот скилл { #references-in-this-skill }

- [ссылки/tc-schema.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/tc-tracker/references/tc-schema.md) — Полная схема JSON для записей TC и реестра.
- [ссылки/lifecycle.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/tc-tracker/references/lifecycle.md) — Конечный автомат, допустимые переходы и потоки восстановления.
- [ссылки/handoff-format.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/tc-tracker/references/handoff-format.md) — Структура хэндоффа сессии и лучшие практики.
