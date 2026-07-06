---
name: code-to-prd
description: "Перепроектируйте кодовую базу интерфейса в PRD. Использование: /code-to-prd [путь]"
argument-hint: "[path]"
---

# /code-to-prd { #code-to-prd }

Преобразуйте кодовую базу внешнего интерфейса в полный документ требований к продукту.

## Использование { #usage }

```bash
/code-to-prd                    # Analyze current project
/code-to-prd ./src              # Analyze specific directory
/code-to-prd /path/to/project   # Analyze external project
```

## Что он делает { #what-it-does }

1. **Сканировать** — Запустить `codebase_analyzer.py` для обнаружения фреймворка, маршрутов, API, перечислений и структуры проекта
2. **Эшафот** — Запуск `prd_scaffolder.py` чтобы создать `prd/` каталог с README.md , заглушки для каждой страницы и файлы приложений
3. **Анализ** — Пройдитесь по каждой странице, следуя воркфлоу фазы 2: поля, взаимодействия, зависимости API, взаимосвязи страниц
4. **Сгенерировать** — Создать окончательный PRD со всеми страницами, словарем перечислений, инвентарем API и картой взаимосвязей страниц

## Шаги { #steps }

### Шаг 1: Проанализируйте { #step-1-analyze }

Определите путь к проекту (по умолчанию: текущий каталог). Запустите интерфейсный анализатор:

```bash
python3 {skill_path}/scripts/codebase_analyzer.py {project_path} -o .code-to-prd-analysis.json
```

Отобразите сводку результатов: фреймворк, количество страниц, количество API, количество перечислений.

### Шаг 2: Строительные леса { #step-2-scaffold }

Сгенерируйте каркас каталога PRD:

```bash
python3 {skill_path}/scripts/prd_scaffolder.py .code-to-prd-analysis.json -o prd/
```

### Шаг 3: Заполните { #step-3-fill }

Для каждой страницы в инвентаре следуйте инструкциям SKILL.md Фаза 2 Воркфлоу:
- Прочитайте файлы компонентов страницы
- Поля документа, взаимодействия, зависимости API, взаимосвязи страниц
- Заполните соответствующий `prd/pages/` заглушка

Работайте пакетами по 3-5 страниц для больших проектов (>15 страниц). Запрашивайте подтверждение у пользователя после каждой партии.

### Шаг 4: Завершение работы { #step-4-finalize }

Заполните файлы приложения:
- `prd/appendix/enum-dictionary.md` — найдены все перечисления и коды состояния
- `prd/appendix/api-inventory.md` — сводная ссылка на API
- `prd/appendix/page-relationships.md` — карта навигации и сопоставления данных

Очистите временный файл анализа:
```bash
rm .code-to-prd-analysis.json
```

## Выход { #output }

А `prd/` каталог, содержащий:
- `README.md` — обзор системы, карта модулей, список страниц
- `pages/*.md` — один файл на страницу с полями, взаимодействиями, API
- `appendix/*.md` — словарь перечислений, инвентаризация API, взаимосвязи страниц

## Ссылка на Скилл { #skill-reference }

- `product-team/code-to-prd/skills/code-to-prd/SKILL.md`
- `product-team/code-to-prd/skills/code-to-prd/scripts/codebase_analyzer.py`
- `product-team/code-to-prd/skills/code-to-prd/scripts/prd_scaffolder.py`
- `product-team/code-to-prd/skills/code-to-prd/references/prd-quality-checklist.md`
