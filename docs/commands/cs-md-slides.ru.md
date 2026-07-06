---
title: "/cs-md-slides — слэш-команда для ИИ-агентов разработки"
description: "Преобразуйте колоду Markdown (слайды, разделенные границами --- HR или заголовками # H1, с необязательными <!-- примечания: ... --> блоки заметок. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-md-slides

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/markdown-html/commands/cs-md-slides.md">Источник</a></span>
</div>


Преобразуйте колоду Markdown в **$ARGUMENTS** в однофайловую интерактивную HTML-презентацию.

## Предполетные гейты (отказывать, никогда не перекрывать) { #pre-flight-gates-refuse-never-override }

1. **Введите < 100 строк** → отклонить (Markdown выигрывает ниже порога Shihipar).
2. **Дизайн-система не онбординг** → мусор, поверхность `/cs:design-system`.
3. **Нет четких границ слайда ** (автоматический режим: требуется ≥ 3 часов или ≥ 5 Ч1) → отклонить, направить в md-документ.
4. ** 1-слайдовая колода ** → отказаться (это плакат, а не колода).
5. **`--strict-notes` с охватом заметок < 50%** → отклонить.
6. **Выходной каталог недоступен для записи** → отказать, запросить у пользователя `--out`.

## Пайплайн { #pipeline }

```bash
# 1. Resolve output path (doctype=slides → deck- prefix)
python3 markdown-html/skills/markdown-html-orchestrator/scripts/output_path_resolver.py \
    --input "<path>.md" --doctype slides

# 2. Split slides on --- HR or H1 (auto-detect)
python3 markdown-html/skills/md-slides/scripts/slide_splitter.py \
    --input "<path>.md" --boundary auto --output /tmp/slides.json

# 3. Extract <!-- notes: ... --> blocks per slide
python3 markdown-html/skills/md-slides/scripts/presenter_notes_parser.py \
    --slides /tmp/slides.json --output /tmp/deck.json

# 4. Render single-file HTML deck
python3 markdown-html/skills/md-slides/scripts/deck_html_renderer.py \
    --slides /tmp/deck.json --title "<deck title>" \
    --output <resolved-out>.html
```

## Что поставляется в HTML-коде { #what-ships-in-the-html }

- **Все слайды в виде `<section class="slide">`** с одним видимым контентом за раз (контролируемый CSS, не требующий JS-контента)
- ** Навигация с клавиатуры**:
  - `→` / `Space` / `PgDn` → следующий слайд
  - `←` / `PgUp` → предыдущий слайд
  - `Home` / `End` → первый / последний слайд
  - `P` → переключить режим презентатора
  - `Esc` → выход из режима презентатора
- ** Режим презентатора ** — разделенный просмотр: текущий слайд (ширина 60%) + панель (ширина 40% с часами + заметки диктора + предварительный просмотр следующего слайда)
- **Глубокая привязка URL-хэша** — `#3` переходит к слайду 3; обходит слайды взад/вперед; делится `deck.html#5` чтобы приземлиться на слайде 5
- ** Индикатор выполнения ** вверху (3 пикселя); счетчик перемещений в правом нижнем углу
- **Печать в формате PDF ** с помощью встроенного диалогового окна печати браузера: `@media print` делает каждый слайд одной страницей (`Cmd+P` / `Ctrl+P`)
- **`prefers-reduced-motion`** удостоенный чести
- **12 фирменных CSS-токенов** из design-system; design_style влияет на плотность верстки

## Жесткие правила { #hard-rules }

- Выход один `.html` файл. Нет мультифайлового вывода.
- Внешний CDN: `fonts.googleapis.com` всегда; `cdn.jsdelivr.net` (Призма) только тогда, когда `--syntax` пройдено.
- Нет среды выполнения JS-фреймворка. Обработчики событий Vanilla JS + keyboard.
- Повторный запуск с теми же входными данными записывает `deck-{slug}-2.html` и так далее.

## Полезные флаги { #useful-flags }

- `--boundary {auto,hr,h1}` — режим границы слайда (по умолчанию: авто)
- `--title "My Talk"` — устанавливает `<title>` и название вкладки
- `--syntax` — включить Prism.js CDN для блоков кода (по умолчанию отключен; деки редко нуждаются в нем)
- `--strict-notes` — отказаться, если < 50% слайдов содержат примечания докладчика (используйте, когда необходим режим докладчика)

## Выход { #output }

Возвращает: количество слайдов, процент охвата примечаний, путь вывода, примененный стиль оформления, используемые основные функции, один форсирующий вопрос.

## Ссылки { #references }

Видишь `markdown-html/skills/md-slides/references/`:
- `presentation_ux.md` — Аткинсон + Рейнольдс + Тафте + NN/g + Вайншенк + Марп/reveal.js/Большая конвергенция
- `keyboard_nav_patterns.md` — reveal.js / Big / Spectacle ключевая карта + WCAG 2.1.1 + 2.4.3 + MDN KeyboardEvent
- `single_file_deck_conventions.md` — Big + Marp + Pandoc + WCAG 2.3.3 + @media print
