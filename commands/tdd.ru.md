---
name: tdd
description: "Запустите красно-зеленый воркфлоу TDD-рефакторинга — сначала сгенерируйте неудачные тесты, переведите в зеленый цвет, затем проверьте пробелы в покрытии. Использование: /tdd <сгенерировать|покрытие|проверить> [цель]"
argument-hint: <generate|coverage|validate> [file-or-dir]
---

# /tdd { #tdd }

Запустите первый тестовый воркфлоу для `$ARGUMENTS` используя скилл руководства по TDD. Первое слово из `$ARGUMENTS` выбирает режим (`generate`, `coverage`, или `validate`); остальное - это целевой файл или каталог. Если `$ARGUMENTS` пусто, спросите, какой режим и цель.

> ** Примечание по инструментам: ** скрипты tdd-guide являются ** библиотечными модулями Python, а не инструментами CLI ** — импортируйте их; не вызывайте их как команды. Доступные для запуска шаблоны приведены ниже.

## Режимы { #modes }

### `/tdd generate <file-or-dir>` — сначала напишите неудачные тесты { #tdd-generate---write-failing-tests-first }

1. Читать `engineering-team/skills/tdd-guide/SKILL.md` и `engineering-team/skills/tdd-guide/references/tdd-best-practices.md` для красно-зеленой дисциплины рефакторинга и таксономии тестовых примеров (счастливый путь, крайние случаи, случаи ошибок)
2. Обнаружьте тестовый фреймворк проекта — используйте `engineering-team/skills/tdd-guide/references/framework-guide.md` для соглашений Jest/Vitest/pytest/JUnit
3. Напишите тесты ** перед ** любой реализацией; запустите их и подтвердите, что они завершились неудачей (красный)
4. Реализуйте минимальный код для прохождения (зеленый), затем проведите рефакторинг, оставив тесты зелеными
5. При необходимости используйте библиотеку для создания шаблонов-заглушек:

```bash
cd engineering-team/skills/tdd-guide/scripts && python3 -c "
from test_generator import TestGenerator, TestFramework
g = TestGenerator(framework=TestFramework.PYTEST, language='python')
cases = g.generate_from_requirements({'acceptance_criteria': [
    {'id': 'AC1', 'description': 'validates email format'},
    {'id': 'AC2', 'description': 'rejects duplicate emails'}]})
print(g.generate_test_file('registration', cases))
"
```

### `/tdd coverage <coverage-report>` — анализ пробелов по отношению к пороговому значению { #tdd-coverage---analyze-gaps-against-a-threshold }

1. Сначала создайте отчет о реальном охвате с помощью встроенного runner проекта (`pytest --cov --cov-report=lcov`, `vitest run --coverage`, `jest --coverage`)
2. Проанализируйте его и перечислите приоритетные пробелы:

```bash
cd engineering-team/skills/tdd-guide/scripts && python3 -c "
from coverage_analyzer import CoverageAnalyzer
a = CoverageAnalyzer()
a.parse_coverage_report(open('<path-to-lcov-or-json>').read(), 'lcov')  # or 'json' / 'xml'
print(a.calculate_summary())
for gap in a.identify_gaps(threshold=80.0): print(gap)
"
```

(Вход для проверки на дым доступен по адресу `engineering-team/skills/tdd-guide/assets/sample_coverage_report.lcov`.)

3. Для каждого пробела вернитесь к `/tdd generate` — пробелы в охвате заполняются тестами, а не оправданиями

### `/tdd validate <test-file>` — ревью качества теста { #tdd-validate---review-test-quality }

Прочтите тестовый файл и проверьте его на соответствие `engineering-team/skills/tdd-guide/references/tdd-best-practices.md`:

- [ ] Каждый тест содержит по крайней мере одно значимое утверждение (тестов без утверждений не существует)
- [ ] Рассмотрены крайние случаи и пути к ошибкам, а не только счастливый путь
- [ ] Тесты независимы (нет связи порядков, нет общего изменяемого состояния)
- [ ] Имена тестов описывают поведение, а не реализацию
- [ ] Никакого тестирования личных внутренних компонентов — только поведение

Сообщайте о сбоях с конкретными предложениями по переписыванию.

## Интеграция CI { #ci-integration }

Для подключения пороговых значений покрытия к CI выполните следующие действия `engineering-team/skills/tdd-guide/references/ci-integration.md`.

## Активы репо (проверенные пути) { #repo-assets-verified-paths }

- Скилл: `engineering-team/skills/tdd-guide/SKILL.md` (+ `HOW_TO_USE.md`)
- Лучшие практики: `engineering-team/skills/tdd-guide/references/tdd-best-practices.md`
- Конвенции о фреймворках: `engineering-team/skills/tdd-guide/references/framework-guide.md`
- Интеграция CI: `engineering-team/skills/tdd-guide/references/ci-integration.md`
- Библиотечные модули: `engineering-team/skills/tdd-guide/scripts/` (test_generator, coverage_analyzer, tdd_workflow, fixture_generator, metrics_calculator — только для импорта)
- Выборочные входные данные: `engineering-team/skills/tdd-guide/assets/`
