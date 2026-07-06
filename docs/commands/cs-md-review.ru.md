---
title: "/cs-md-review — слэш-команда для ИИ-агентов разработки"
description: "Преобразуйте PR-запись Markdown или ревью кода (с блоками ``diff и > [!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT] выносками серьезности) в однофайловый. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-md-review

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/markdown-html/commands/cs-md-review.md">Источник</a></span>
</div>


Преобразуйте ревью в Markdown по адресу **$ARGUMENTS** в виде однофайлового HTML-ревью с 2 столбцами.

## Предполетные гейты (отказывать, никогда не перекрывать) { #pre-flight-gates-refuse-never-override }

1. **Введите < 100 строк** → отклонить (Markdown выигрывает ниже порога Shihipar).
2. **Дизайн-система не онбординг** → мусор, поверхность `/cs:design-system`.
3. **`--reviewer` отсутствует** → отклонить (при ревью кода должен быть указан рецензент-человек).
4. **Никаких отличий нет** → отклонить, направить в `md-document` вместо этого.
5. **Выходной каталог недоступен для записи ** → отказать, запросить у пользователя альтернативный через `--out`.

## Пайплайн { #pipeline }

```bash
# 1. Resolve output path (uses doctype=review → review- prefix)
python3 markdown-html/skills/markdown-html-orchestrator/scripts/output_path_resolver.py \
    --input "<path>.md" --doctype review

# 2. Parse diff hunks
python3 markdown-html/skills/md-review/scripts/diff_parser.py \
    --input "<path>.md" --output /tmp/hunks.json

# 3. Extract severity-tagged annotations, attached to nearest hunk
python3 markdown-html/skills/md-review/scripts/annotation_extractor.py \
    --input "<path>.md" --diff-blocks /tmp/hunks.json --output /tmp/annotations.json

# 4. Render — --reviewer is mandatory
python3 markdown-html/skills/md-review/scripts/review_html_renderer.py \
    --diff-blocks /tmp/hunks.json --annotations /tmp/annotations.json \
    --reviewer "<reviewer-name>" --title "<PR title>" \
    --output <resolved-out>.html
```

## Что поставляется в HTML-коде { #what-ships-in-the-html }

- ** Верхний переход-навигация ** — каждая находка со значком серьезности (цвет + значок + aria-метка) + предварительный просмотр 80 символов + ссылка для перехода; учитывается в заголовке ("3 БЛОКИРУЮЩИХ · 2 ОСНОВНЫХ · 1 НИЧТОЖЕСТВО")
- **2-столбчатые строки** — единая разница слева (номера строк с обеих сторон, знаки +/−, сложение/deletion оттенки bg из маркеров design-system), карточки с аннотациями справа
- **Код серьезности** — БЛОКИРАТОР = вычисленный цвет опасности (акцент повернут на 120° в сторону красного), ОСНОВНОЙ = `--md-warn`, НЕЗНАЧИТЕЛЬНЫЙ = `--md-link`, ГНИДА = `--md-text-muted`. На каждом значке есть значок (■ / ▲ / ● / ◦) + aria-ярлык для WCAG 1.4.1
- **Полоса одобрения** — при наличии маркеров LGTM и отсутствии результатов, полоса с тонировкой "Успешно"
- **Раздел общих замечаний** — для не привязанных аннотаций
- **Нижний колонтитул рецензента** — "Рецензент: \<имя\>" (обязательно)
- **Отзывчивый** — 2- столбец сворачивается до размера менее 900 пикселей

## Жесткие правила { #hard-rules }

- Выход один `.html` файл. Нет внешнего CSS/JS. Единственным внешним является Google Fonts CSS (цвета Prism — diff не конфликтуют с подсветкой синтаксиса).
- Нет среды выполнения JS-фреймворка. Страница полностью статична; переходные навигационные ссылки являются простыми привязками.
- Серьезность никогда не зависит только от цвета (WCAG 1.4.1).
- Повторный запуск с теми же входными данными записывает `review-{slug}-2.html` и так далее.

## Пользовательское соглашение о строгости { #custom-severity-convention }

```bash
--severity-convention "critical,important,suggestion,nit"
```

Меняет местами названия уровней; позиция 0 является наиболее серьезной. Значение по умолчанию: `BLOCKER,MAJOR,MINOR,NIT` (Google * Руководство разработчика по ревью кода*).

## Выход { #output }

Возвращает: количество фрагментов, количество аннотаций, разбивку по степени серьезности, путь вывода, имя рецензента, один форсирующий вопрос.

## Ссылки { #references }

Видишь `markdown-html/skills/md-review/references/`:
- `diff_rendering_canon.md` — Формат POSIX diff + соглашения GitHub /GitLab + difftastic + SWE в Google
- `severity_coding.md` — WCAG 1.4.1 + ревью таксономии Google + обозначение Дона Нормана
- `pr_annotation_ux.md` — Конвергентный 2-col UX от GitHub / GitLab/Reviewable/CodeStream
