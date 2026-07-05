---
title: "Аудитор зависимостей { #dependency-auditor } — Агентский скилл для Codex и OpenClaw"
description: "Аудит и управление зависимостями в многоязычных проектах. Определяет уязвимости, конфликты лицензий, риски переходных зависимостей и пути безопасного. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Аудитор зависимостей { #dependency-auditor }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `dependency-auditor`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/dependency-auditor/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> **Тип скилла:** МОЩНЫЙ · **Категория:** Инженерия · **Домен:** Управление зависимостями и безопасность

Автономный детерминированный аудит зависимостей в более чем 8 экосистемах пакетов. Эти три скрипта сопоставляют шаблоны с манифестами / файлами блокировки — они **не** вызывают API-интерфейсы live advisory; сопоставьте их результаты с `npm audit` / `pip-audit` / `cargo audit` для текущего покрытия CVE.

## Быстрый старт { #quick-start }

```bash
# 1. Scan for vulnerabilities (built-in offline CVE pattern set; exit non-zero on high severity)
python3 scripts/dep_scanner.py /path/to/project --format json --fail-on-high -o scan.json

# 2. Check license compliance and conflicts
python3 scripts/license_checker.py /path/to/project --policy strict --format json -o licenses.json

# 3. Plan upgrades from the scanner's inventory
python3 scripts/upgrade_planner.py scan.json --risk-threshold medium --timeline 90 --format json -o plan.json
```

Потребляйте выходные данные: `scan.json` результаты определяют, какие пакеты теперь нужно закрепить /исправлять; `licenses.json` конфликты передаются пользователю в виде списка юридических рисков; `plan.json` заказывает обновления по степени риска с пометками об откате. `--quick-scan` пропускает переходные значения deps; `--security-only` ограничивает план исправлениями безопасности.

**Цикл проверки:** после применения обновлений повторно запустите шаг 1 и подтвердите 0 результатов высокой степени серьезности перед закрытием аудита.

## Поддерживаемые экосистемы { #supported-ecosystems }

| Язык | Проанализированные манифесты |
|---|---|
| JavaScript/Узел | package.json, package-lock.json, yarn.замок |
| Питон | requirements.txt , pyproject.toml, Pipfile.замок, поэзия.замок |
| Иди | go.mod, go.sum |
| Ржавчина | Груз.томл, Груз.замок |
| Рубин | Драгоценный файл, драгоценный файл.замок |
| Java | pom.xml , gradle.файл блокировки |
| PHP | composer.json, композитор.замок |
| C#/.NET | пакеты.конфигурация, project.assets.json |

## Классификация лицензий { #license-classification }

- **Разрешающий**: MIT, Apache 2.0, BSD (предложение 2/3), ISC
- **Авторское лево (сильное)**: GPL v2/v3, AGPL v3 — указывает на риск заражения в разрешительных проектах
- **Авторское лево (слабое)**: LGPL v2.1/v3, MPL 2.0
- **Проприетарные / двойные / неизвестные** — неизвестные лицензии отображаются для ревью вручную

Средство проверки анализирует наследование лицензий по цепочкам зависимостей и выдает конфликтные пары с предложениями по исправлению.

## Матрица рисков обновления { #upgrade-risk-matrix }

| Риск | Тип обновления | Обработка |
|---|---|---|
| Низкий | Патч, исправления безопасности | Применяйте немедленно |
| Средний | Второстепенный с новыми функциями | Пакетное обновление по расписанию |
| Высокий | Основная версия, изменения в API | Специальная задача миграции + тесты |
| Критический | Известные критические изменения | Запланированная миграция с процедурой отката |

Расстановка приоритетов: исправления безопасности > исправления ошибок > обновления функций > основные изменения; устаревшим функциям уделяется немедленное внимание.

## Сценарии (точные требования к возможностям) { #scripts-accurate-capability-claims }

- **`scripts/dep_scanner.py`** — многоформатный синтаксический анализатор; встроенный автономный набор шаблонов уязвимостей (~16 шаблонов CVE — слой дыма, не замена оперативным рекомендациям); переходное разрешение из файлов блокировки; вывод текста в формате JSON +.
- **`scripts/license_checker.py`** — определение лицензии по метаданным пакета; матрица совместимости для более чем 20 типов лицензий; `--policy permissive|strict`; обнаружение конфликтов с устранением неполадок.
- **`scripts/upgrade_planner.py`** — прогнозирование критических изменений на основе semver; план миграции с учетом рисков с чек-листом тестирования и оценкой временных рамок.

Образцы приспособлений: `test-project/` и `test-inventory.json` в этой папке; ожидаемые формы в `expected_outputs/`.

## Интеграция CI { #ci-integration }

```bash
# Security gate in CI
python3 scripts/dep_scanner.py . --format json --fail-on-high
python3 scripts/license_checker.py . --policy strict --format json
```

## Лучшие практики { #best-practices }

1. ** Уделяйте приоритетное внимание безопасности**: немедленно обращайтесь к важным /критичным обнаружениям; соответствие лицензии важнее функциональности.
2. ** Постепенные обновления **: поэтапные обновления с тщательным тестированием; фич-флаги для опасных неровностей.
3. **Частота **: проверка безопасности при каждой фиксации; аудит лицензий ежемесячно; полный аудит ежеквартально.
4. **Ложные срабатывания**: внесение в белый список с документацией; обратитесь к сопровождающим по поводу неоднозначности лицензии.

Видишь [README.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/dependency-auditor/README.md) для подробного использования и `references/` для баз знаний об уязвимостях/лицензиях.
