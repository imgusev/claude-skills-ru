---
title: "/cs-md-document — слэш-команда для ИИ-агентов разработки"
description: "Преобразуйте Markdown в расширенной форме (спецификации, RFC, отчеты, планы, пояснения) в однофайловый интерактивный HTML-документ. Запускает. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-md-document

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/markdown-html/commands/cs-md-document.md">Источник</a></span>
</div>


Преобразуйте Markdown в **$ARGUMENTS** в однофайловый интерактивный HTML-документ.

## Предполетные гейты (отказывать, никогда не перекрывать) { #pre-flight-gates-refuse-never-override }

1. **Введите < 100 строк** → отклонить (Markdown выигрывает ниже порогового значения для каждого Shihipar). `wc -l <path>` для подтверждения.
2. **Дизайн-система не онбординг** → мусор, поверхность `/cs:design-system`.
3. **Выходной каталог недоступен для записи ** → отказаться, запросить у пользователя альтернативный через `--out`.

## Пайплайн { #pipeline }

```bash
# 1. Classify (if not already routed by orchestrator)
python3 markdown-html/skills/markdown-html-orchestrator/scripts/doctype_classifier.py \
    --input "<path>.md" --output json \
  | python3 markdown-html/skills/markdown-html-orchestrator/scripts/route_explainer.py

# 2. Resolve the output path
python3 markdown-html/skills/markdown-html-orchestrator/scripts/output_path_resolver.py \
    --input "<path>.md" --doctype document

# 3. Parse → render → inject
python3 markdown-html/skills/md-document/scripts/markdown_parser.py \
    --input "<path>.md" --output /tmp/sections.json
python3 markdown-html/skills/md-document/scripts/html_renderer.py \
    --sections /tmp/sections.json --output <resolved-out>.html
python3 markdown-html/skills/md-document/scripts/interactivity_injector.py \
    --file <resolved-out>.html \
    --features search,copycode,smoothscroll,scrollspy
```

## Что поставляется в HTML-коде { #what-ships-in-the-html }

- Sticky-заголовок боковой панели (по умолчанию; настраивается с помощью `toc.behavior` в дизайн-системе)
- Шпион прокрутки: `aria-current="location"` в записи оглавления для рассматриваемого раздела
- Строка поиска (Esc очищается): фильтрует, какие разделы H2 видны
- Кнопки копирования кода на каждом `<pre>` (ванильный `navigator.clipboard` с `execCommand` запасной вариант)
- Плавная прокрутка при нажатии на ссылку TOC
- Prism.js подсветка синтаксиса (автозагрузчик выбирает только те языки, которые используются в этом документе)
- 12 пользовательских свойств brand CSS из системы проектирования `derived_palette`
- `@media (prefers-reduced-motion: reduce)` удостоенный чести
- Удобная печать с помощью встроенной таблицы стилей печати браузера (нет `@page` переопределения, необходимые для документов)

## Жесткие правила { #hard-rules }

- Выход один `.html` файл. Нет мультифайлового вывода, нет извлеченных CSS / JS, нет папок ресурсов.
- Внешний CDN: `fonts.googleapis.com` + `cdn.jsdelivr.net` (Призма). Больше ничего.
- Нет среды выполнения JS-фреймворка. Только Vanilla JS + IntersectionObserver.
- Повторный запуск с теми же входными данными записывает `doc-{slug}-2.html` и т.д. (суффикс столкновения).

## Выход { #output }

Возвращает: строки ввода, путь вывода, примененный стиль оформления, 3 основные используемые функции, один форсирующий вопрос.

## Ссылки { #references }

Видишь `markdown-html/skills/md-document/references/`:
- `information_density_patterns.md` — Шихипар + Туфте + Ваттенбергер
- `toc_and_nav_ux.md` — NN/g + WCAG + ARIA
- `single_file_html_discipline.md` — Обоснование артефакта для одного файла
