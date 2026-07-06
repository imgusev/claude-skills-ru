---
title: "/cs-handoff-setup — слэш-команда для ИИ-агентов разработки"
description: "Сначала запустите настройку для скилла хэндоффа. Отвечает на 5 вопросов (местоположение сохранения, хранение, строгость редактирования, контекст git. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-handoff-setup

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/productivity/handoff/commands/cs-handoff-setup.md">Источник</a></span>
</div>


Настройте скилл хэндоффа. Отвечает на 5 вопросов (плюс 1-2 необязательных) и записывает конфигурацию. Повторите запуск в любое время.

## Призыв { #invocation }

```
/cs:handoff-setup                 # configure global defaults
/cs:handoff-setup --project       # set project-specific overrides
```

## Вопросы { #questions }

1. ** Сохранить местоположение ** — Временная папка операционной системы / домашняя папка / скрытая домашняя папка / для каждого проекта / пользовательская. *Нет предварительно выбранного значения по умолчанию - явный выбор не требуется при первом запуске.*
2. **Окно сохранения** — 7 / 30 дни / вечность / руководство пользователя.
3. **Строгость редактирования** — строго / предупреждать / выключать.
4. **Контекст Git** — автоматическое включение ветки + последняя фиксация + количество грязных файлов? да/нет.
5. **Область рекомендаций по скиллу** — все репозитории / только текущий домен / отключено.
6. **Стиль имени файла** *(только если сохранить местоположение ≠ temp)* — date_slug / timestamp / mktemp.

## Поведение { #behaviour }

- **Глобальная конфигурация** в `~/.config/handoff/config.json`.
- **Переопределение проекта** в `<repo>/.handoff/config.json` (с `--project`). Отсутствующие ключи возвращаются к глобальному значению.
- Для `save_location.mode = project`, настройка предлагает добавить `.handoff/` к `.gitignore`.
- Идемпотентен. Повторный запуск предварительно заполняет текущие значения.

## Сброс к значениям по умолчанию { #reset-to-defaults }

Удалите конфигурацию и запустите повторно:

```bash
rm ~/.config/handoff/config.json
rm ~/.config/handoff/.setup-declined 2>/dev/null
```

## Бежать { #run }

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/setup.py
```

Для переопределений в рамках проекта:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/setup.py --reconfigure --project
```
