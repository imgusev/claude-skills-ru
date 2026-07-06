---
name: a11y-audit
description: "Просканируйте интерфейсный проект на предмет нарушений доступности WCAG 2.2 и исправьте их. Использование: /a11y-аудит [путь]"
argument-hint: "[path]"
---

# /a11y-аудит { #a11y-audit }

Просканируйте интерфейсный проект на наличие проблем с доступом к WCAG 2.2, покажите исправления и, при необходимости, проверьте цветовой контраст.

## Использование { #usage }

```bash
/a11y-audit                     # Scan current project
/a11y-audit ./src               # Scan specific directory
/a11y-audit ./src --fix         # Scan and auto-fix what's possible
```

## Что он делает { #what-it-does }

### Шаг 1: Сканирование { #step-1-scan }

Запустите сканер a11y в целевом каталоге:

```bash
python3 {skill_path}/scripts/a11y_scanner.py {path} --json
```

Проанализируйте выходные данные в формате JSON. Сгруппируйте результаты по степени тяжести (критический → серьезный → средней тяжести → незначительный).

Отображение сводной информации:
```
A11y Audit: ./src
  Critical: 3 | Serious: 7 | Moderate: 12 | Minor: 5
  Files scanned: 42 | Files with issues: 15
```

### Шаг 2: Исправьте { #step-2-fix }

Для каждого вывода (начиная с критического):

1. Прочитайте поврежденный файл
2. Показать нарушение с контекстом (до)
3. Примените исправление из `engineering-team/a11y-audit/skills/a11y-audit/references/framework-a11y-patterns.md`
4. Показать результат (после)

** Автоматически устраняемые проблемы ** (применяйте без запроса):
- Пропавший без вести `alt=""` на декоративных изображениях
- Пропавший без вести `lang` атрибут на `<html>`
- `tabindex` значения > 0 → установить в 0
- Пропавший без вести `type="button"` на кнопках без отправки
- Удаление контура без замены → добавить `:focus-visible` стили

**Проблемы, требующие ввода данных пользователем ** (показать исправление, попросить применить):
- Отсутствует текст alt (требуется описание от пользователя)
- Отсутствующие метки формы (нужен текст метки)
- Реструктуризация заголовка (может повлиять на макет)
- Изменения роли ARIA (могут повлиять на функциональность)

### Шаг 3: Проверка контрастности { #step-3-contrast-check }

Если присутствуют CSS-файлы, запустите средство проверки контрастности:

```bash
python3 {skill_path}/scripts/contrast_checker.py --batch {path}
```

Для каждой неудачной цветовой пары предложите доступные альтернативы.

### Шаг 4: Отчет { #step-4-report }

Сгенерируйте отчет о Markdown по адресу `a11y-report.md`:
- Краткое изложение (пройдено/не пройдено, количество проблем)
- Результаты для каждого файла с различиями до/после
- Оставшиеся элементы для ревью вручную
- Охват критериями WCAG

## Ссылка на Скилл { #skill-reference }

- `engineering-team/a11y-audit/skills/a11y-audit/SKILL.md`
- `engineering-team/a11y-audit/skills/a11y-audit/scripts/a11y_scanner.py`
- `engineering-team/a11y-audit/skills/a11y-audit/scripts/contrast_checker.py`
- `engineering-team/a11y-audit/skills/a11y-audit/references/wcag-quick-ref.md`
- `engineering-team/a11y-audit/skills/a11y-audit/references/aria-patterns.md`
- `engineering-team/a11y-audit/skills/a11y-audit/references/framework-a11y-patterns.md`
