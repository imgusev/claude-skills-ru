---
title: "Генератор списка изменений { #changelog-generator } — Агентский скилл для Codex и OpenClaw"
description: "Создавайте согласованные, проверяемые примечания к выпуску на основе обычных коммитов. Разделяет синтаксический анализ фиксации, логику. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Генератор списка изменений { #changelog-generator }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `changelog-generator`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/changelog-generator/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Уровень:** МОЩНЫЙ  
**Категория:** Инженерия  
**Домен:** Управление выпуском / документация

## Обзор { #overview }

Используйте этот скилл для создания согласованных, проверяемых примечаний к выпуску из обычных коммитов. Он разделяет синтаксический анализ фиксации, логику семантического изменения и рендеринг журнала изменений, чтобы команды могли автоматизировать выпуски без потери редакторского контроля.

## Основные возможности { #core-capabilities }

- Анализ сообщений о фиксации с использованием обычных правил фиксации
- Обнаружить семантический сбой (`major`, `minor`, `patch`) из потока фиксации
- Рендеринг Ведет разделы журнала изменений (`Added`, `Changed`, `Fixed` и т.д.)
- Генерируйте записи release из диапазонов git или предоставленных данных фиксации
- Примените формат фиксации с помощью специального скрипта компоновки
- Поддержка интеграции CI с помощью машиночитаемого вывода JSON

## Когда использовать { #when-to-use }

- Перед публикацией тега выпуска
- Во время CI автоматически генерировать примечания к выпуску
- Во время проверки PR для блокировки недопустимых форматов сообщений о фиксации
- В monorepos, где журналы изменений пакетов требуют ограниченной фильтрации
- При преобразовании необработанной истории git в пользовательские заметки

## Ключевые Воркфлоу { #key-workflows }

### 1. Сгенерируйте запись в Журнале изменений из Git { #1-generate-changelog-entry-from-git }

```bash
python3 scripts/generate_changelog.py \
  --from-tag v1.3.0 \
  --to-tag v1.4.0 \
  --next-version v1.4.0 \
  --format markdown
```

### 2. Сгенерируйте запись из стандартного ввода/Файла { #2-generate-entry-from-stdinfile-input }

```bash
git log v1.3.0..v1.4.0 --pretty=format:'%s' | \
  python3 scripts/generate_changelog.py --next-version v1.4.0 --format markdown

python3 scripts/generate_changelog.py --input commits.txt --next-version v1.4.0 --format json
```

### 3. Обновление `CHANGELOG.md` { #3-update-changelogmd }

```bash
python3 scripts/generate_changelog.py \
  --from-tag v1.3.0 \
  --to-tag HEAD \
  --next-version v1.4.0 \
  --write CHANGELOG.md
```

### 4. Вычислите следующую версию на основе коммитов { #4-compute-the-next-version-from-commits }

Если пользователь не определился со следующей версией, выведите ее вместо того, чтобы гадать:

```bash
git log v1.3.0..HEAD --oneline | \
  python3 scripts/version_bumper.py --current-version 1.3.0 --output-format json
```

Выходной JSON содержит `recommended_version`, `bump_type` (`major`/`minor`/`patch`/`none`), и с `--include-commands` точный `git tag` команды. Кормить `recommended_version` в `generate_changelog.py --next-version`. Предварительные релизы: добавить `--prerelease alpha|beta|rc`. Вводимые данные должны быть реальными `git log --oneline` выходные данные (шестнадцатеричные хэши); образец живет в `assets/sample_git_log.txt`.

### 5. Lint фиксирует перед слиянием { #5-lint-commits-before-merge }

```bash
python3 scripts/commit_linter.py --from-ref origin/main --to-ref HEAD --strict --format text
```

Или файл/stdin:

```bash
python3 scripts/commit_linter.py --input commits.txt --strict
cat commits.txt | python3 scripts/commit_linter.py --format json
```

## Обычные правила фиксации { #conventional-commit-rules }

Поддерживаемые типы:

- `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`
- `security`, `deprecated`, `remove`

Кардинальные изменения:

- `type(scope)!: summary`
- Нижний колонтитул/основная часть включает в себя `BREAKING CHANGE:`

Отображение SemVer:

- нарушение...> `major`
- неразрывный `feat` -> `minor`
- все остальные -> `patch`

## Интерфейсы сценариев { #script-interfaces }

- `python3 scripts/generate_changelog.py --help`
  - Считывает коммиты из git или stdin/`--input`
  - Отображает Markdown или JSON
  - Необязательный предварительный список изменений на месте
- `python3 scripts/commit_linter.py --help`
  - Проверяет формат фиксации
  - Возвращает ненулевое значение в `--strict` режим по нарушениям

## Распространенные подводные камни { #common-pitfalls }

1. Смешивание сообщений о фиксации слияния с анализом фиксации освобождения
2. Использование расплывчатых сводок о фиксации, которые не могут стать примечаниями к выпуску
3. Отсутствие руководства по миграции для внесения критических изменений
4. Рассмотрение изменений в документации / рутинной работе как функций, ориентированных на пользователя
5. Перезапись исторических разделов журнала изменений вместо добавления

## Лучшие практики { #best-practices }

1. Делайте коммиты небольшими и ориентированными на намерение.
2. Сообщения о фиксации области действия (`feat(api): ...`) в репозиториях с несколькими пакетами.
3. Применяйте проверки линтера в пайплайнах PR.
4. Ревью сгенерированный Markdown перед публикацией.
5. Тег освобождается только после успешного создания журнала изменений.
6. Сохраняйте `[Unreleased]` раздел для ручного управления, когда это необходимо.

## Серьезность исправлений и соглашения об уровне обслуживания { #hotfix-severity--slas }

Когда выпуск идет не так, как надо, классифицируйте, прежде чем действовать (полные процедуры в [ссылки/исправление-procedures.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/changelog-generator/references/hotfix-procedures.md)):

| Суровость | Определение | Соглашение об уровне обслуживания | Одобрение |
|---|---|---|---|
| P0 — Критический | Сбой в работе, потеря данных, эксплуатируемая уязвимость | Исправлено деплою ≤ 2 часа; аварийное деплою обходит обычные гейты | Ведущий инженер + менеджер по вызову |
| P1 — Высокий | Основная функция нарушена, значительное влияние на пользователя | Исправление, деплою в течение ≤ 24 часов; ускоренный ревью | Ведущий инженер + менеджер по продукции |
| P2 — Средний | Незначительные проблемы, ограниченное воздействие | Следующий цикл выпуска | Стандартный PR-ревью |

Ветка исправлений берется из последнего стабильного тега, содержит только минимальное исправление и получает свою собственную запись в журнале изменений с исправлением исправлений с помощью приведенного выше воркфлоу.

## Триггеры отката { #rollback-triggers }

Предварительно зафиксируйте эти пороговые значения перед пометкой; откатитесь назад, когда что-либо сработает:

| Триггер | Порог |
|---|---|
| Всплеск частоты ошибок | > 2-кратный базовый уровень в течение 30 минут |
| Снижение производительности |  увеличение задержки > на 50% |
| Сбой функции | Нарушена основная функциональность |
| Инцидент в сфере безопасности | Эксплуатируемая уязвимость |
| Повреждение данных | Нарушена целостность базы данных |

Предпочтительная функция - отключение флага при откате кода; откат базы данных выполняется только для неразрушающих миграций (предпочтительны миграции только вперед). Видишь [ссылки/исправление-procedures.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/changelog-generator/references/hotfix-procedures.md).

## Ссылки { #references }

- [список литературы/ci-integration.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/changelog-generator/references/ci-integration.md)
- [ссылки/список изменений-форматирование-guide.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/changelog-generator/references/changelog-formatting-guide.md)
- [список литературы/monorepo-strategy.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/changelog-generator/references/monorepo-strategy.md)
- [ссылки/исправление-procedures.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/changelog-generator/references/hotfix-procedures.md)
- [README.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/changelog-generator/README.md)

## Управление выпуском { #release-governance }

Используйте этот поток выпуска для обеспечения предсказуемости:

1. История фиксации Lint для целевого диапазона выпуска.
2. Сгенерируйте черновик журнала изменений из коммитов.
3. Вручную отрегулируйте формулировку для ясности клиенту.
4. Подтвердите рекомендацию semver bump.
5. Выпуск тега возможен только после утверждения списка изменений.

## Проверка качества выходных данных { #output-quality-checks }

- Каждый маркер имеет значение для пользователя, а не для шума реализации.
- Кардинальные изменения включают в себя действие по миграции.
- Исправления безопасности изолированы в `Security` раздел.
- Разделы, в которых нет записей, опускаются.
- Повторяющиеся маркеры в разных разделах удаляются.

## Политика CI { #ci-policy }

- Бежать `commit_linter.py --strict` на всех персонах.
- Блокируйте слияние при недопустимых обычных коммитах.
- Автоматическое создание черновиков примечаний к выпуску при нажатии на тег.
- Требуйте одобрения человека, прежде чем записывать в `CHANGELOG.md` на главной ветке.

## Руководство по Монорепо { #monorepo-guidance }

- Предпочитайте, чтобы области фиксации были выровнены по именам пакетов.
- Фильтруйте поток фиксации по области действия для выпусков, зависящих от конкретного пакета.
- Сохраняйте изменения в масштабе всей системы в корневом журнале изменений.
- Храните журналы изменений пакетов рядом с корнями пакетов для ясности владения.

## Обработка сбоев { #failure-handling }

- Если не найдено допустимых обычных коммитов: сбой на ранней стадии, не создавайте вводящие в заблуждение пустые заметки.
- Если git range недопустим: явный диапазон поверхности в выводе ошибки.
- Если цель записи отсутствует: создайте безопасную структуру заголовка журнала изменений.
