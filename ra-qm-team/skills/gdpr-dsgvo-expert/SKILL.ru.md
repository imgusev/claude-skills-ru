---
name: "gdpr-dsgvo-expert"
description: Автоматизация соблюдения требований GDPR и немецкого DSGVO. Сканирует кодовые базы на предмет рисков для конфиденциальности, формирует документацию DPIA, отслеживает запросы о правах субъектов данных в соответствии со статьей 12(3) в течение одного месяца. Используйте при проведении оценки соответствия требованиям GDPR, аудита конфиденциальности, планировании защиты данных, формировании DPIA или управлении правами субъектов данных (DSAR) (например, "проверьте этот сервис на наличие рисков, связанных с GDPR", "отслеживайте крайний срок запроса доступа"). Окончательные решения о соответствии направляются генеральному директору или юрисконсульту.
---

# Эксперт по GDPR/DSGVO { #gdprdsgvo-expert }

Инструменты и руководство по соблюдению Общего регламента ЕС по защите данных (GDPR) и немецкого Bundesdatenschutzgesetz (BDSG).

---

## Оглавление { #table-of-contents }

- [Инструменты](#tools)
  - [Средство проверки соответствия требованиям GDPR](#gdpr-compliance-checker)
  - [Генератор DPIA](#dpia-generator)
  - [Отслеживание прав субъекта данных](#data-subject-rights-tracker)
- [Справочные руководства](#reference-guides)
- [Воркфлоу](#workflows)

---

## Инструменты { #tools }

### Средство проверки соответствия требованиям GDPR { #gdpr-compliance-checker }

Сканирует базы кода на предмет потенциальных проблем с соблюдением GDPR, включая шаблоны персональных данных и рискованные методы работы с кодом.

```bash
# Scan a project directory
python scripts/gdpr_compliance_checker.py /path/to/project

# JSON output for CI/CD integration
python scripts/gdpr_compliance_checker.py . --json --output report.json
```

**Обнаруживает:**
- Образцы персональных данных (электронная почта, телефон, IP-адреса)
- Данные специальной категории (медицинские, биометрические, религиозные)
- Финансовые данные (кредитные карты, IBAN)
- Рискованные шаблоны кода:
  - Регистрация персональных данных
  - Отсутствующие механизмы получения согласия
  - Хранение данных на неопределенный срок
  - Незашифрованные конфиденциальные данные
  - Отключена функция удаления

**Выход:**
- Оценка соответствия требованиям (0-100)
- Классификация рисков (критический, высокий, средний)
- Приоритетные рекомендации со ссылками на статьи GDPR

---

### Генератор DPIA { #dpia-generator }

Формирует документацию по оценке воздействия на защиту данных в соответствии с требованиями статьи 35.

```bash
# Get input template
python scripts/dpia_generator.py --template > input.json

# Generate DPIA report
python scripts/dpia_generator.py --input input.json --output dpia_report.md
```

**Особенности:**
- Автоматическая оценка порогового значения DPIA
- Идентификация рисков на основе характеристик обработки
- Правовая основа требования к документации
- Рекомендации по смягчению последствий
- Генерация отчета по Markdown

**Оценены триггеры DPIA:**
- Систематический мониторинг (статья 35(3)(c))
- Крупномасштабные данные по специальным категориям (статья 35(3)(b))
- Автоматизированное принятие решений (статья 35(3)(a))
- Одобренные EDPB критерии высокого риска (WP248 rev.01)

---

### Отслеживание прав субъектов данных { #data-subject-rights-tracker }

Управляет запросами о правах субъекта данных в соответствии со статьями 15-22 GDPR.

```bash
# Add new request
python scripts/data_subject_rights_tracker.py add \
  --type access --subject "John Doe" --email "john@example.com"

# List all requests
python scripts/data_subject_rights_tracker.py list

# Update status
python scripts/data_subject_rights_tracker.py status --id DSR-202601-0001 --update verified

# Generate compliance report
python scripts/data_subject_rights_tracker.py report --output compliance.json

# Generate response template
python scripts/data_subject_rights_tracker.py template --id DSR-202601-0001
```

**Поддерживаемые права:**

| Верно | Статья | Крайний срок |
|-------|---------|----------|
| Доступ | Статья 15 | Один месяц (статья 12(3)) |
| Исправление | Статья 16 | Один месяц (статья 12(3)) |
| Стирание | Статья 17 | Один месяц (статья 12(3)) |
| Ограничение | Статья 18 | Один месяц (статья 12(3)) |
| Портативность | Статья 20 | Один месяц (статья 12(3)) |
| Возражение | Статья 21 | Один месяц (статья 12(3)) |
| Автоматизированные решения | Статья 22 | Один месяц (статья 12(3)) |

**Особенности:**
- Отслеживание крайних сроков с просроченными предупреждениями
- Воркфлоу для проверки подлинности
- Генерация шаблона ответа
- Отчетность о соблюдении требований

---

## Справочные руководства { #reference-guides }

### Руководство по соблюдению GDPR { #gdpr-compliance-guide }
`references/gdpr_compliance_guide.md`

Всеобъемлющее руководство по внедрению, охватывающее:
- Правовые основания для обработки (статья 6)
- Требования к особой категории (статья 9)
- Реализация прав субъекта данных
- Требования к подотчетности (статья 30)
- Международные переводы (глава V)
- Уведомление о нарушении (статьи 33-34)

### Немецкие требования к БДСМ { #german-bdsg-requirements }
`references/german_bdsg_requirements.md`

Специфичные для Германии требования, включая:
- Порог назначения на должность DPO (§ 38 BDSG - 20+ сотрудников)
- Обработка данных о занятости (§ 26 BDSG)
- Правила видеонаблюдения (§ 4 BDSG)
- Требования к кредитному рейтингу (§ 31 BDSG)
- Государственные законы о защите данных (Landesdatenschutzgesetze)
- Права на совместное определение деятельности совета по труду

### Методология DPIA { #dpia-methodology }
`references/dpia_methodology.md`

Пошаговый процесс DPIA:
- Пороговые критерии оценки
- Одобренные EDPB индикаторы высокого риска (WP248 rev.01)
- Методология оценки рисков
- Категории мер по смягчению последствий
- Консультации генерального директора и надзорного органа
- Шаблоны и чек-листы

---

## Воркфлоу { #workflows }

### Воркфлоу 1: Оценка новых операций по обработке { #workflow-1-new-processing-activity-assessment }

```
Step 1: Run compliance checker on codebase
        → python scripts/gdpr_compliance_checker.py /path/to/code

Step 2: Review findings and compliance score
        → Address critical and high issues

Step 3: Determine if DPIA required
        → Check references/dpia_methodology.md threshold criteria

Step 4: If DPIA required, generate assessment
        → python scripts/dpia_generator.py --template > input.json
        → Fill in processing details
        → python scripts/dpia_generator.py --input input.json --output dpia.md

Step 5: Document in records of processing activities
```

### Воркфлоу 2: Обработка запроса субъекта данных { #workflow-2-data-subject-request-handling }

```
Step 1: Log request in tracker
        → python scripts/data_subject_rights_tracker.py add --type [type] ...

Step 2: Verify identity (proportionate measures)
        → python scripts/data_subject_rights_tracker.py status --id [ID] --update verified

Step 3: Gather data from systems
        → python scripts/data_subject_rights_tracker.py status --id [ID] --update in_progress

Step 4: Generate response
        → python scripts/data_subject_rights_tracker.py template --id [ID]

Step 5: Send response and complete
        → python scripts/data_subject_rights_tracker.py status --id [ID] --update completed

Step 6: Monitor compliance
        → python scripts/data_subject_rights_tracker.py report
```

### Воркфлоу 3: Проверка соответствия требованиям BDSG в Германии { #workflow-3-german-bdsg-compliance-check }

```
Step 1: Determine if DPO required
        → 20+ employees processing personal data automatically
        → OR processing requires DPIA
        → OR business involves data transfer/market research

Step 2: If employees involved, review § 26 BDSG
        → Document legal basis for employee data
        → Check works council requirements

Step 3: If video surveillance, comply with § 4 BDSG
        → Install signage
        → Document necessity
        → Limit retention

Step 4: Register DPO with supervisory authority
        → See references/german_bdsg_requirements.md for authority list
```

---

## Ключевые концепции GDPR { #key-gdpr-concepts }

### Правовые основы (статья 6) { #legal-bases-art-6 }

- **Согласие**: Маркетинг, информационные бюллетени, аналитика (должно предоставляться свободно, конкретно, информированно)
- **Контракт**: Выполнение заказа, оказание услуг
- **Юридические обязательства**: Налоговый учет, трудовое право
- **Законные интересы**: Предотвращение мошенничества, безопасность (требуется проверка баланса)

### Данные особой категории (статья 9) { #special-category-data-art-9 }

Требуется явное согласие или исключение из статьи 9(2):
- Медицинские данные
- Биометрические данные
- Расовое/этническое происхождение
- Политические взгляды
- Религиозные убеждения
- Членство в профсоюзе
- Генетические данные
- Сексуальная ориентация

### Права субъекта данных { #data-subject-rights }

Все права должны быть выполнены в течение ** одного месяца с момента получения** (статья 12(3)). Крайний срок составляет календарный месяц, а не 30 дней, и может быть продлен еще на ** два месяца** для сложных или многочисленных запросов — субъект данных должен быть проинформирован о продлении (с указанием причин) в течение первого месяца.:
- **Доступ**: Предоставьте копию данных и информацию об обработке
- **Исправление**: Исправьте неточные данные
- **Удаление**: Удаление данных (за исключением юридических обязательств)
- **Ограничение**: Ограничьте обработку до тех пор, пока проблемы не будут решены
- **Переносимость**: Предоставление данных в машиночитаемом формате
- **Возражение**: Прекратить обработку на основании законных интересов

### Немецкие дополнения к БДСМ { #german-bdsg-additions }

| Тема | Секция БДСГ | Ключевое требование |
|-------|--------------|-----------------|
| Порог DPO | § 38 | более 20 сотрудников = обязательный DPO |
| Занятость | § 26 | Подробные правила сбора данных о сотрудниках |
| Видео | § 4 | Вывески и пропорциональность |
| Подсчет очков | § 31 | Объяснимые алгоритмы |
