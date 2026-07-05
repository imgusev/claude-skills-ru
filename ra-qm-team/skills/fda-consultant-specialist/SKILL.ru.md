---
name: "fda-consultant-specialist"
description: Консультант по регулированию FDA для компаний, производящих медицинское оборудование. Содержит руководство по пути 510 (k)/PMA/ De Novo, QMSR (21 CFR 820, который включает в себя ISO 13485:2016 по ссылке с 2026-02-02; ранее QSR), оценки HIPAA и кибербезопасность устройств. Используйте, когда пользователь упоминает FDA submission, 510(k), PMA, De Novo, QMSR, QSR, ISO 13485 для FDA, премаркет, предикатное устройство, существенную эквивалентность, медицинское устройство HIPAA или кибербезопасность FDA.
---

# Специалист-консультант FDA { #fda-consultant-specialist }

Консультации FDA по нормативным вопросам для производителей медицинского оборудования, касающиеся путей подачи заявок, Регламента системы менеджмента качества (QMSR, 21 CFR, часть 820 — ранее QSR), соответствия требованиям HIPAA и требований к кибербезопасности устройств.

## Оглавление { #table-of-contents }

- [Выбор пути FDA](#fda-pathway-selection)
- [510(k) Процесс подачи заявки](#510k-submission-process)
- [Соответствие требованиям QMSR (ранее QSR)](#qmsr-compliance-formerly-qsr)
- [HIPAA для медицинских устройств](#hipaa-for-medical-devices)
- [Кибербезопасность устройств](#device-cybersecurity)
- [Ресурсы](#resources)

---

## Выбор пути FDA { #fda-pathway-selection }

Определите соответствующий путь регулирования FDA на основе классификации устройств и доступности предикатов.

### Фреймворк для принятия решений { #decision-framework }

```
Predicate device exists?
├── YES → Substantially equivalent?
│   ├── YES → 510(k) Pathway
│   │   ├── No design changes → Abbreviated 510(k)
│   │   ├── Manufacturing only → Special 510(k)
│   │   └── Design/performance → Traditional 510(k)
│   └── NO → PMA or De Novo
└── NO → Novel device?
    ├── Low-to-moderate risk → De Novo
    └── High risk (Class III) → PMA
```

### Сравнение путей { #pathway-comparison }

| Тропинка | Когда использовать | Временная шкала | Плата за пользование (2024 финансовый год) |
|---------|-------------|----------|-------------------|
| 510(k) Традиционный | Предикат существует, дизайн меняется | 90 дней | 21 760 долларов США (2024 финансовый год) |
| 510(k) Специальный | Меняется только производство | 30 дней | 21 760 долларов США (2024 финансовый год) |
| 510(k) Сокращенный | Руководство/соответствие стандартам | 30 дней | 21 760 долларов США (2024 финансовый год) |
| Заново | Новый, низкий-умеренный риск | 150 дней | 134 676 долларов США (2024 финансовый год) |
| ПМА | Класс III, без сказуемого | более 180 дней | $425 000+ (2024 финансовый год) |

> Плата за пользование устанавливается ежегодно в соответствии с MDUFA. Проверьте сборы за текущий финансовый год по адресу fda.gov (График пользовательских сборов MDUFA) до составления бюджета; тарифы для малого бизнеса отличаются.

### Стратегия предварительной подачи заявок { #pre-submission-strategy }

1. Определите код продукта и классификацию
2. Поиск предикатов в базе данных 510(k)
3. Оценить возможность существенной эквивалентности
4. Подготовьте дополнительные вопросы для FDA
5. Запланируйте предварительную встречу, если это необходимо

**Ссылка:** Смотрите [fda_submission_guide.md](references/fda_submission_guide.md) для матриц принятия решений о путях и требований к представлению.

---

## 510(k) Процесс подачи заявки { #510k-submission-process }

### Воркфлоу { #workflow }

```
Phase 1: Planning
├── Step 1: Identify predicate device(s)
├── Step 2: Compare intended use and technology
├── Step 3: Determine testing requirements
└── Checkpoint: SE argument feasible?

Phase 2: Preparation
├── Step 4: Complete performance testing
├── Step 5: Prepare device description
├── Step 6: Document SE comparison
├── Step 7: Finalize labeling
└── Checkpoint: All required sections complete?

Phase 3: Submission
├── Step 8: Assemble submission package
├── Step 9: Submit via eSTAR
├── Step 10: Track acknowledgment
└── Checkpoint: Submission accepted?

Phase 4: Review
├── Step 11: Monitor review status
├── Step 12: Respond to AI requests
├── Step 13: Receive decision
└── Verification: SE letter received?
```

### Обязательные разделы (21 CFR 807.87) { #required-sections-21-cfr-80787 }

| Раздел | Содержание |
|---------|---------|
| Сопроводительное письмо | Тип отправки, идентификатор устройства, контактная информация |
| Форма 3514 | Титульный лист для ревью на премаркете CDRH |
| Описание устройства | Физическое описание, принципы работы |
| Показания к применению | Форма 3881, контингент пациентов, условия использования |
| Сравнение SE | Параллельное сравнение с предикатом |
| Тестирование производительности | Стенд, биосовместимость, электробезопасность |
| Документация по программному обеспечению | Уровень беспокойства, анализ опасности (IEC 62304) |
| Маркировка | IFU, этикетки на упаковках, предупреждения |
| 510(k) Краткое изложение | Публичное резюме представления |

### Распространенные проблемы с RTA { #common-rta-issues }

| Проблема | Предотвращение |
|-------|------------|
| Недостающая плата за пользование | Подтвердите платеж перед отправкой |
| Неполная форма 3514 | Ревью все поля, убедитесь в наличии подписи |
| Предикат не идентифицирован | Подтвердите K-номер в базе данных FDA |
| Неадекватное сравнение SE | Учитывайте все технологические характеристики |

---

## Соответствие требованиям QMSR (ранее QSR) { #qmsr-compliance-formerly-qsr }

Требования к Регламенту системы менеджмента качества (QMSR) для производителей медицинских изделий в соответствии с 21 CFR, часть 820.

> ** Переход к QMSR (вступает в силу 2026-02-02): ** Окончательное правило FDA по QMSR (89 FR 7496) внесло поправки в 21 CFR, часть 820, чтобы включить ** ISO 13485:2016 по ссылке** и удалило устаревшую структуру подразделов QSR (820.20–820.198). Эти номера подразделов являются ** историческими** и больше не существуют в CFR; соответствующие требования теперь вытекают из положений ISO 13485:2016 плюс сохраненные/перенумерованные разделы 820.10 (требования, вкл. стандарт ISO 13485), 820.35 (записи) и 820.45 (контроль маркировки устройств и упаковки). 21 Части 801, 803, 806 и 830 CFR остаются без изменений. Приведенные ниже устаревшие номера QSR сохраняются только в качестве привычного индекса, каждый из которых соответствует своему текущему пункту стандарта ISO 13485.

### Ключевые подсистемы качества (устаревший индекс QSR → текущее положение ISO 13485:2016) { #key-quality-subsystems-legacy-qsr-index--current-iso-134852016-clause }

| Унаследованный раздел QSR (исторический, до 2026 года) | Название | Текущие полномочия в рамках QMSR | Сосредоточься |
|-------------------------------------------|-------|------------------------------|-------|
| 820.20 | Ответственность руководства | ISO 13485 §5.1, 5.5, 5.6 | Политика в области качества, организационная структура, ревью руководства |
| 820.30 | Элементы управления проектированием | ISO 13485 §7.3 | Ввод, вывод, ревью, верификация, валидация |
| 820.40 | Управление документами | ISO 13485 §4.2.4 | Утверждение, распространение, контроль изменений |
| 820.50 | Контроль за закупками | ISO 13485 §7.4 | Квалификация поставщика, данные о закупках |
| 820.70 | Производственный контроль | ISO 13485 §6.3, 6.4, 7.5 | Валидация процессов, экологический контроль |
| 820.100 | КАПА | ISO 13485 §8.5.2, 8.5.3 | Анализ первопричин, корректирующие действия |
| 820.181 | Основная запись устройства | ISO 13485 §4.2.3 (файл медицинского устройства) + 21 CFR 820.35 | Спецификации, процедуры, критерии приемлемости |

### Управление воркфлоу при проектировании (ISO 13485 §7.3; устаревший QSR 820.30) { #design-controls-workflow-iso-13485-73-legacy-qsr-82030 }

```
Step 1: Design Input
└── Capture user needs, intended use, regulatory requirements
    Verification: Inputs reviewed and approved?

Step 2: Design Output
└── Create specifications, drawings, software architecture
    Verification: Outputs traceable to inputs?

Step 3: Design Review
└── Conduct reviews at each phase milestone
    Verification: Review records with signatures?

Step 4: Design Verification
└── Perform testing against specifications
    Verification: All tests pass acceptance criteria?

Step 5: Design Validation
└── Confirm device meets user needs in actual use conditions
    Verification: Validation report approved?

Step 6: Design Transfer
└── Release to production with DMR complete
    Verification: Transfer checklist complete?
```

### Процесс CAPA (ISO 13485 §8.5.2/8.5.3; устаревший QSR 820.100) { #capa-process-iso-13485-852853-legacy-qsr-820100 }

1. **Идентификация**: Документирование несоответствия или потенциальной проблемы
2. ** Исследовать**: Выполнить анализ первопричин (5 причин, Рыбья кость)
3. **План**: Определение корректирующих/предупреждающих действий
4. **Внедрить**: Выполнить действия, обновить документацию
5. **Проверить**: Подтвердить завершение внедрения
6. **Эффективность**: Мониторинг на предмет рецидива (30-90 дней)
7. **Закрытие**: Одобрение руководства и закрытие

**Ссылка:** Смотрите [qsr_compliance_requirements.md](references/qsr_compliance_requirements.md) для исторической структуры QSR с полным сопоставлением положений QMSR/ISO 13485:2016.

---

## HIPAA для медицинских устройств { #hipaa-for-medical-devices }

Требования HIPAA к устройствам, которые создают, хранят, передают или получают доступ к защищенной медицинской информации (PHI).

### Применимость { #applicability }

| Тип устройства | HIPAA применяется |
|-------------|---------------|
| Автономная диагностика (без передачи данных) | Нет |
| Подключенное устройство, передающее данные пациента | Да |
| Устройство с интеграцией EHR | Да |
| SaMD, хранящий информацию о пациенте | Да |
| Оздоровительное приложение (без диагностики) | Только если хранит PHI |

### Требуемые меры предосторожности { #required-safeguards }

```
Administrative (§164.308)
├── Security officer designation
├── Risk analysis and management
├── Workforce training
├── Incident response procedures
└── Business associate agreements

Physical (§164.310)
├── Facility access controls
├── Workstation security
└── Device disposal procedures

Technical (§164.312)
├── Access control (unique IDs, auto-logoff)
├── Audit controls (logging)
├── Integrity controls (checksums, hashes)
├── Authentication (MFA recommended)
└── Transmission security (TLS 1.2+)
```

### Этапы оценки рисков { #risk-assessment-steps }

1. Инвентаризация всех систем, обрабатывающих ePHI
2. Потоки документальных данных (сбор, хранение, передача)
3. Выявление угроз и уязвимостей
4. Оценить вероятность и воздействие
5. Определите уровни риска
6. Внедрять средства контроля
7. Документируйте остаточный риск

**Ссылка:** Смотрите [hipaa_compliance_framework.md](references/hipaa_compliance_framework.md) для чек-листов внедрения и шаблонов BAA.

---

## Кибербезопасность устройств { #device-cybersecurity }

Требования FDA к кибербезопасности подключенных медицинских устройств.

### Предрыночные требования { #premarket-requirements }

| Элемент | Описание |
|---------|-------------|
| Модель угрозы | Пошаговый анализ, деревья атак, границы доверия |
| Средства контроля безопасности | Аутентификация, шифрование, контроль доступа |
| СБОМ | Спецификация программного обеспечения (CycloneDX или SPDX) |
| Тестирование безопасности | Тестирование на проникновение, сканирование уязвимостей |
| План защиты от уязвимостей | Процесс раскрытия информации, управление исправлениями |

### Классификация уровней устройств { #device-tier-classification }

**Уровень 1 (более высокий риск):**
- Подключается к сети/Интернету
- Инцидент с кибербезопасностью может нанести вред пациенту

**Уровень 2 (стандартный риск):**
- Все остальные подключенные устройства

### Обязательства на постмаркетинговом рынке { #postmarket-obligations }

1. Отслеживайте NVD и ICS-CERT на наличие уязвимостей
2. Оценка применимости к компонентам устройства
3. Разрабатывайте и тестируйте исправления
4. Общайтесь с клиентами
5. Отчитываться перед FDA в соответствии с рекомендациями

### Скоординированное раскрытие уязвимостей { #coordinated-vulnerability-disclosure }

```
Researcher Report
    ↓
Acknowledgment (48 hours)
    ↓
Initial Assessment (5 days)
    ↓
Fix Development
    ↓
Coordinated Public Disclosure
```

**Ссылка:** Смотрите [device_cybersecurity_guidance.md](references/device_cybersecurity_guidance.md) для получения примеров формата SBOM и шаблонов моделирования угроз.

---

## Ресурсы { #resources }

### сценарии/ { #scripts }

| Сценарий | Цель |
|--------|---------|
| `fda_submission_tracker.py` | Этапы и сроки подачи заявки на трек 510(k)/PMA/De Novo |
| `qsr_compliance_checker.py` | Оценка документации по СМК в соответствии с устаревшим чек-листом QSR, соответствующим стандарту ISO 13485:2016 (QMSR) |
| `hipaa_risk_assessment.py` | Оценить гарантии HIPAA в программном обеспечении медицинского оборудования |

### ссылки/ { #references }

| Файл | Содержание |
|------|---------|
| `fda_submission_guide.md` | 510(k), De Novo, требования к представлению PMA и чек-листы |
| `qsr_compliance_requirements.md` | Историческая структура QSR с отображением QMSR/ISO 13485:2016, шаблоны реализации |
| `hipaa_compliance_framework.md` | Гарантии правил безопасности HIPAA и требования BAA |
| `device_cybersecurity_guidance.md` | Требования FDA к кибербезопасности, SBOM, моделирование угроз |
| `fda_capa_requirements.md` | Процесс CAPA, анализ первопричин, проверка эффективности |

### Примеры использования { #usage-examples }

```bash
# Track FDA submission status
python scripts/fda_submission_tracker.py /path/to/project --type 510k

# Assess QMS documentation (legacy QSR section keys, mapped to ISO 13485 under QMSR)
python scripts/qsr_compliance_checker.py /path/to/project --section 820.30  # legacy checklist key = ISO 13485 §7.3 (design & development)

# Run HIPAA risk assessment
python scripts/hipaa_risk_assessment.py /path/to/project --category technical
```
