---
title: "Скилл командира инцидента { #incident-commander-skill } — Агентский скилл и плагин Codex"
description: "Комплексный фреймворк реагирования на инциденты - от обнаружения до разрешения и ревью после инцидента. Проверенные в боях методы SRE/ DevOps. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Скилл командира инцидента { #incident-commander-skill }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `incident-commander`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/incident-commander/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


**Категория:** Инженерная команда  
**Уровень:** МОЩНЫЙ  
** Автор:** Команда Клода по скиллам  
**Версия:** 1.0.0  
** Последнее обновление:** Февраль 2026

## Обзор { #overview }

Фреймворк реагирования на инциденты для ** инцидентов доступности/надежности** (перебои в работе, ухудшения качества, неудачные деплою): классификация серьезности, восстановление временной шкалы и ревью после инцидента.

** Это НЕ сортировка инцидентов безопасности.** Для событий безопасности (программ-вымогателей, вторжений, утечки данных, анализа IOC, судебной экспертизы NIST SP 800-61) перейдите к `incident-response`. Оба скилла используют метки SEV1-SEV4; этот оценивает операционное воздействие (пользователи, доход, SLA), в то время как `incident-response` классифицирует типы атак и методы криминалистической обработки.

## Основные характеристики { #key-features }

- ** Автоматизированная классификация серьезности** - Интеллектуальная сортировка инцидентов на основе показателей воздействия и срочности
- ** Реконструкция временной шкалы** - Преобразование разрозненных журналов и событий в связные рассказы о инцидентах.
- **Генерация ревью после инцидента** - Структурированные PIR с несколькими фреймворками RCA
- **Коммуникационные шаблоны** - Готовые шаблоны для обновлений и эскалации взаимодействия с стейкхолдерами
- ** Интеграция с рансбуком** - Создание пригодных к действию рансбуков на основе шаблонов инцидентов

## Скиллы включали { #skills-included }

### Основные инструменты { #core-tools }

1. **Классификатор инцидентов** (`incident_classifier.py`)
   - Анализирует описания инцидентов и выводит уровни серьезности
   - Рекомендует группам реагирования и первоначальные действия
   - Генерирует коммуникационные шаблоны на основе серьезности

2. ** Реконструктор временной шкалы** (`timeline_reconstructor.py`)
   - Обрабатывает события с отметками времени из нескольких источников
   - Восстанавливает хронологическую шкалу инцидента
   - Выявляет пробелы и проводит анализ продолжительности

3. **PIR-генератор** (`pir_generator.py`)
   - Создает комплексные документы для ревью после инцидента
   - Применяет несколько фреймворков RCA (5 Whys, Fishbone, Timeline).
   - Генерирует последующие элементы, пригодные для принятия мер

## Фреймворк реагирования на инциденты { #incident-response-framework }

### Система классификации степени тяжести { #severity-classification-system }

#### SEV1 - Критический сбой в работе { #sev1---critical-outage }
**Определение:** Полный сбой в обслуживании, затрагивающий всех пользователей или критически важные бизнес-функции

**Характеристики:**
- Услуги, ориентированные на клиента, полностью недоступны
- Потеря или повреждение данных, влияющие на пользователей
- Нарушения безопасности, связанные с раскрытием данных клиентов
- Системы, приносящие доход, вышли из строя
- Нарушения SLA с финансовыми штрафами

**Требования к реагированию:**
- Немедленная эскалация до дежурного инженера
- Командир инцидента назначен в течение 5 минут
- Уведомление руководителя в течение 15 минут
- Обновление страницы публичного статуса в течение 15 минут
- Создана боевая рубка
- Если понадобится, все на связи

**Частота связи:** Каждые 15 минут до разрешения

#### SEV2 - Основное воздействие { #sev2---major-impact }
**Определение:** Значительное ухудшение, влияющее на подмножество пользователей или некритические функции

**Характеристики:**
- Частичное ухудшение качества обслуживания (затронуто >25% пользователей)
- Проблемы с производительностью, вызывающие разочарование пользователей
- Некритичные функции недоступны
- Внутренние инструменты, влияющие на производительность
- Несоответствия в данных, не влияющие на работу пользователя

**Требования к реагированию:**
- Ответ инженера по вызову в течение 15 минут
- Командир по инциденту назначен в течение 30 минут
- Обновление страницы статуса в течение 30 минут
- Уведомление стейкхолдеров в течение 1 часа
- Регулярные обновления команды

**Частота связи: ** Каждые 30 минут во время активного ответа

#### SEV3 - Незначительное воздействие { #sev3---minor-impact }
**Определение:** Ограниченное воздействие при наличии обходных путей

**Характеристики:**
- Затронутый отдельный элемент или компонент
- затронуто <25% пользователей
- Доступные обходные пути
- Снижение производительности существенно не влияет на пользовательский интерфейс
- Несрочные предупреждения о мониторинге

**Требования к реагированию:**
- Ответ в течение 2 часов в рабочее время
- Ответ на следующий рабочий день приемлем в нерабочее время
- Уведомление внутренней команды
- Необязательное обновление страницы статуса

**Частота связи:** Только на ключевых этапах

#### SEV4 - Низкое воздействие { #sev4---low-impact }
**Определение:** Минимальное воздействие, косметические проблемы или плановое техническое обслуживание

**Характеристики:**
- Косметические ошибки
- Проблемы с документацией
- Регистрация или мониторинг пробелов
- Проблемы с производительностью без влияния на пользователя
- Проблемы со средой разработки/тестирования

**Требования к реагированию:**
- Ответ в течение 1-2 рабочих дней
- Стандартное отслеживание заявок/выпусков
- Никакой специальной эскалации не требуется

**Частота связи:** Обновления стандартного цикла разработки

### Роль командира по инциденту { #incident-commander-role }

#### Основные обязанности { #primary-responsibilities }

1. **Команда и контроль**
   - Владеть процессом реагирования на инциденты
   - Принимайте важные решения о распределении ресурсов
   - Координация действий технических групп и стейкхолдеров
   - Поддерживайте ситуационную осведомленность во всех потоках реагирования

2. **Коммуникационный центр**
   - Регулярно предоставлять обновленную информацию стейкхолдерам
   - Управление внешними коммуникациями (статусными страницами, уведомлениями клиентов)
   - Способствовать эффективной коммуникации между группами реагирования
   - Защитите сотрудников службы реагирования от внешних отвлекающих факторов

3. **Управление процессами**
   - Обеспечьте надлежащее отслеживание инцидентов и документирование
   - Стремитесь к разрешению при сохранении качества
   - Координировать хэндоффы между членами команды
   - Планируйте и выполняйте стратегии отката, если это необходимо

4. **Руководство после инцидента**
   - Обеспечьте проведение тщательных ревью после инцидента
   - Стимулировать внедрение превентивных мер
   - Делитесь полученными знаниями с более широкой организацией

#### Фреймворк для принятия решений { #decision-making-framework }

**Экстренные решения (SEV1/2):**
- Командир по инциденту обладает всеми полномочиями
- Склонность к действию, а не к анализу
- Документируйте решения для последующего ревью
- Проконсультируйтесь с экспертами в данной области, но не попадайте в блокировку

**Распределение ресурсов:**
- Может привлечь любых необходимых членов команды
- Полномочия по эскалации до высшего руководства
- Может одобрять экстренные расходы на внешние ресурсы
- Совершать звонки по каналам связи и времени

**Технические решения:**
- Обращайтесь к техническим специалистам за подробностями реализации
- Делайте окончательные выводы о компромиссах между скоростью и риском
- Утвердить стратегии отката и пересылки с фиксацией
- Координировать подходы к тестированию и валидации

### Коммуникационные шаблоны { #communication-templates }

#### Первоначальное уведомление о инциденте (SEV1/2) { #initial-incident-notification-sev12 }

```
Subject: [SEV{severity}] {Service Name} - {Brief Description}

Incident Details:
- Start Time: {timestamp}
- Severity: SEV{level}
- Impact: {user impact description}
- Current Status: {investigating/mitigating/resolved}

Technical Details:
- Affected Services: {service list}
- Symptoms: {what users are experiencing}
- Initial Assessment: {suspected root cause if known}

Response Team:
- Incident Commander: {name}
- Technical Lead: {name}
- SMEs Engaged: {list}

Next Update: {timestamp}
Status Page: {link}
War Room: {bridge/chat link}

---
{Incident Commander Name}
{Contact Information}
```

#### Краткое изложение (SEV1) { #executive-summary-sev1 }

```
Subject: URGENT - Customer-Impacting Outage - {Service Name}

Executive Summary:
{2-3 sentence description of customer impact and business implications}

Key Metrics:
- Time to Detection: {X minutes}
- Time to Engagement: {X minutes} 
- Estimated Customer Impact: {number/percentage}
- Current Status: {status}
- ETA to Resolution: {time or "investigating"}

Leadership Actions Required:
- [ ] Customer communication approval
- [ ] PR/Communications coordination  
- [ ] Resource allocation decisions
- [ ] External vendor engagement

Incident Commander: {name} ({contact})
Next Update: {time}

---
This is an automated alert from our incident response system.
```

#### Шаблон для общения с клиентами { #customer-communication-template }

```
We are currently experiencing {brief description of issue} affecting {scope of impact}. 

Our engineering team was alerted at {time} and is actively working to resolve the issue. We will provide updates every {frequency} until resolved.

What we know:
- {factual statement of impact}
- {factual statement of scope}
- {brief status of response}

What we're doing:
- {primary response action}
- {secondary response action}

Workaround (if available):
{workaround steps or "No workaround currently available"}

We apologize for the inconvenience and will share more information as it becomes available.

Next update: {time}
Status page: {link}
```

### Управление стейкхолдерами { #stakeholder-management }

#### Классификация стейкхолдеров { #stakeholder-classification }

**Внутренние стейкхолдеры:**
- **Инженерное лидерство** - Технические решения и распределение ресурсов
- **Управление продуктом** - Оценка воздействия на потребителя и последствий для функций
- ** Служба поддержки клиентов** - Общение с пользователями и управление заявками в службу поддержки
- **Управление продажами/учетными записями** - Управление взаимоотношениями с клиентами для корпоративных клиентов
- **Исполнительная команда** - Принятие решений, влияющих на бизнес, и одобрение внешних коммуникаций
- **Законодательство/соответствие требованиям** - Нормативная отчетность и оценка ответственности

**Внешние стейкхолдеры:**
- **Клиенты** - Доступность услуг и информирование о влиянии
- **Партнеры** - Влияние доступности API и интеграции
- **Поставщики** - Зависимости от сторонних сервисов и эскалация поддержки
- **Регулирующие органы** - Отчетность о соблюдении требований для регулируемых отраслей
- **Общественность/СМИ** - Прозрачность при отключениях, связанных с общественностью

#### Частота общения стейкхолдеров { #communication-cadence-by-stakeholder }

| Стейкхолдер | СЕВ1 | СЕВ2 | СЕВ3 | СЕВ4 |
|-------------|------|------|------|------|
| Инженерное лидерство | В режиме реального времени | 30 минут | 4 часа | Ежедневно |
| Исполнительная команда | 15 минут | 1 час | ЭОД | Еженедельно |
| Служба поддержки клиентов | В режиме реального времени | 30 минут | 2 часа | По мере необходимости |
| Клиенты | 15 минут | 1 час | Необязательный | Нет |
| Партнеры | 30 минут | 2 часа | Необязательный | Нет |

### Фреймворк для генерации Рансбуков { #runbook-generation-framework }

#### Динамические компоненты Рансбука { #dynamic-runbook-components }

1. **Обнаружение плейбуков**
   - Определения предупреждений о мониторинге
   - Сортировочные деревья принятия решений
   - Точки триггера эскалации
   - Первоначальные ответные действия

2. **Плейбуки с ответами**
   - Пошаговые процедуры смягчения последствий
   - Инструкции по откату
   - Контрольные точки проверки
   - Контрольно-пропускные пункты связи

3. **Восстановление плейбуков**
   - Процедуры восстановления сервиса
   - Проверка согласованности данных
   - Проверка производительности
   - Процессы уведомления пользователей

#### Структура шаблона Рансбука { #runbook-template-structure }

```markdown
# {Service/Component} Incident Response Runbook

## Quick Reference
- **Severity Indicators:** {list of conditions for each severity level}
- **Key Contacts:** {on-call rotations and escalation paths}
- **Critical Commands:** {list of emergency commands with descriptions}

## Detection
### Monitoring Alerts
- {Alert name}: {description and thresholds}
- {Alert name}: {description and thresholds}

### Manual Detection Signs
- {Symptom}: {what to look for and where}
- {Symptom}: {what to look for and where}

## Initial Response (0-15 minutes)
1. **Assess Severity**
   - [ ] Check {primary metric}
   - [ ] Verify {secondary indicator}
   - [ ] Classify as SEV{level} based on {criteria}

2. **Establish Command**
   - [ ] Page Incident Commander if SEV1/2
   - [ ] Create incident tracking ticket
   - [ ] Join war room: {link/bridge info}

3. **Initial Investigation**
   - [ ] Check recent deployments: {deployment log location}
   - [ ] Review error logs: {log location and queries}
   - [ ] Verify dependencies: {dependency check commands}

## Mitigation Strategies
### Strategy 1: {Name}
**Use when:** {conditions}
**Steps:**
1. {detailed step with commands}
2. {detailed step with expected outcomes}
3. {validation step}

**Rollback Plan:**
1. {rollback step}
2. {verification step}

### Strategy 2: {Name}
{similar structure}

## Recovery and Validation
1. **Service Restoration**
   - [ ] {restoration step}
   - [ ] Wait for {metric} to return to normal
   - [ ] Validate end-to-end functionality

2. **Communication**
   - [ ] Update status page
   - [ ] Notify stakeholders
   - [ ] Schedule PIR

## Common Pitfalls
- **{Pitfall}:** {description and how to avoid}
- **{Pitfall}:** {description and how to avoid}

## Reference Information
→ See references/reference-information.md for details

## Usage Examples

### Example 1: Database Connection Pool Exhaustion

```bash
# Classify the incident
echo '{"description": "Users reporting 500 errors, database connections timing out", "affected_users": "80%", "business_impact": "high"}' | python scripts/incident_classifier.py

# Reconstruct timeline from logs
python scripts/timeline_reconstructor.py --input assets/sample_timeline_events.json --output timeline.md

# Generate PIR after resolution
python scripts/pir_generator.py --incident assets/sample_incident_data.json --timeline timeline.md --output pir.md
```

### Пример 2: Инцидент, ограничивающий скорость API { #example-2-api-rate-limiting-incident }

```bash
# Quick classification from stdin
echo "API rate limits causing customer API calls to fail" | python scripts/incident_classifier.py --format text

# Build timeline from multiple sources
python scripts/timeline_reconstructor.py --input assets/simple_timeline_events.json --detect-phases --gap-analysis

# Generate comprehensive PIR
python scripts/pir_generator.py --incident assets/sample_incident_pir_data.json --rca-method fishbone --action-items
```

## Лучшие практики { #best-practices }

### Во время реагирования на инцидент { #during-incident-response }

1. **Сохраняйте спокойное лидерство**
   - Сохраняйте спокойствие под давлением
   - Делайте решающие звонки с неполной информацией
   - Выражайте уверенность, признавая при этом неуверенность

2. **Документируйте все**
   - Все предпринятые действия и их результаты
   - Обоснование решения, особенно для спорных вызовов
   - Хронология событий по мере их возникновения

3. **Эффективная коммуникация**
   - Используйте понятный язык, не содержащий жаргона
   - Предоставляйте регулярные обновления, даже если нет никакой новой информации
   - Активно управлять ожиданиями стейкхолдеров

4. **Техническое совершенство**
   - Предпочитайте откаты рискованным исправлениям под давлением
   - Проверьте исправления перед объявлением разрешения
   - Планируйте вторичные сбои и каскадные эффекты

### После инцидента { #post-incident }

1. ** Безупречная культура**
   - Сосредоточьтесь на системных сбоях, а не на отдельных ошибках
   - Поощряйте честное сообщение о том, что пошло не так
   - Отмечайте возможности для обучения и совершенствования

2. **Дисциплина по элементам действия**
   - Назначьте конкретных владельцев и сроки выполнения работ
   - Публично отслеживать прогресс
   - Расставляйте приоритеты, основываясь на риске и усилиях

3. **Обмен знаниями**
   - Широко распространяйте PIR в рамках организации
   - Обновлять рансбуки на основе извлеченных уроков
   - Проводите учебные занятия по типичным режимам отказа

4. **Постоянное совершенствование**
   - Ищите закономерности в нескольких инцидентах
   - Инвестируйте в оснастку и автоматизацию
   - Регулярно проводите ревью и обновление процессов

## Интеграция с существующими инструментами { #integration-with-existing-tools }

### Мониторинг и оповещение { #monitoring-and-alerting }
- Интеграция PagerDuty/Opsgenie для эскалации
- Datadog/Grafana для метрик и дашбордов
- ELK/Splunk для логарифмического анализа и корреляции

### Коммуникационные платформы { #communication-platforms }
- Slack/Команды для координации действий в боевой рубке
- Масштабирование/встреча для видеомостов
- Поставщики страниц статуса (Statuspage.io и т.д.)

### Системы документирования { #documentation-systems }
- Слияние/Концепция для хранения PIR
- GitHub/GitLab для управления версиями рансбука
- JIRA/Linear для отслеживания элементов действий

### Управление изменениями { #change-management }
- Интеграция пайплайна CI/CD
- Системы отслеживания развертывания
- Платформы с фич-флагами для быстрого отката

