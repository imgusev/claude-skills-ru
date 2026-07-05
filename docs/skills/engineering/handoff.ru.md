---
title: "Хэндофф { #handoff } — Агентский скилл для Codex и OpenClaw"
description: "Сведите текущий разговор в документ хэндофф, который может быть передан другому агенту. Ссылается на существующие артефакты (PRD, планы, ADR. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Хэндофф { #handoff }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `handoff`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/handoff/skills/handoff/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> Полученный из [Хэндофф Мэтта Покока](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) (Массачусетский технологический институт). Дисциплина Мэтта, запрещающая дублирование, сохранилась дословно. Дополнения: инструменты + ссылки + оболочка cs-* (смотрите [ссылки/companion_tooling.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/handoff/skills/handoff/references/companion_tooling.md)).

Напишите хэндофф-документ с кратким изложением текущего разговора, чтобы новый агент мог продолжить работу. Сохраните его в пути, созданном с помощью `mktemp -t handoff-XXXXXX.md` (прочитайте файл перед записью в него).

Предложите скиллы, которые следует использовать, если таковые имеются, к следующему занятию.

Не дублируйте содержимое, уже захваченное в других артефактах (PRD, планы, ADR, проблемы, фиксации, различия). Вместо этого ссылайтесь на них по пути или URL-адресу.

Если пользователь передал аргументы, рассматривайте их как описание того, на чем будет сосредоточен следующий сеанс, и соответствующим образом адаптируйте документ.

## Разделы { #sections }

- **Цель следующего сеанса** (из пользовательского аргумента или предполагаемая)
- ** Состояние игры** (что сделано, что блокирует)
- **Открытые решения** (что должен решить следующий агент)
- **Скиллы для использования** (конкретный список)
- **Артефакты** (пути/URL-адреса к PRD, планам, ADR, выпускам, филиалам, PR — не дублировать)

## Оснастка { #tooling }

Видишь [ссылки/companion_tooling.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/handoff/skills/handoff/references/companion_tooling.md). Инструменты: шаблон + дедупликация + рекомендатель. Агент: `cs-handoff-author`. Команда: `/cs:handoff`.

---

**Версия:** 1.0.0
** Производное: ** Мэтт Покок (Массачусетский технологический институт) + оболочка этого репозитория
