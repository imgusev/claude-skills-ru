---
name: "ai-act-readiness"
description: "/cs: ai-act-готовность к действию <система> — EU AI Act 6 - принудительный допрос с применением вопросов. Использовать во время внедрения системы искусственного интеллекта, перед развертыванием в ЕС или во время ежегодного обновления соответствия в рамках этапа выполнения обязательств по статье 113 (2025-02-02 / 2025-08-02 / 2026-08-02 / 2027-08-02)."
---

# /cs:ai-act-readiness — Закон ЕС об искусственном интеллекте, форсирующий вопросы { #csai-act-readiness--eu-ai-act-forcing-questions }

**Команда:** `/cs:ai-act-readiness <system>`

Оператор, отвечающий требованиям Закона ЕС об искусственном интеллекте, проверяет любую систему искусственного интеллекта под давлением перед развертыванием в ЕС. Шесть вопросов, цитируемых в статье, перед любым размещением в ЕС, оценкой соответствия или ежегодным обновлением соответствия требованиям.

## Когда запускать { #when-to-run }

- Во время ревью системы искусственного интеллекта (для каждой новой системы или изменения материала)
- Перед размещением системы искусственного интеллекта на рынке ЕС
- Перед подписанием декларации соответствия ЕС (статья 47)
- Во время ежегодного обновления соответствия (поэтапное выполнение статьи 113 влечет за собой новые обязательства)
- Когда меняется роль организации (разработчик становится поставщиком в соответствии со статьей 25(1) существенное изменение)
- Когда обучающее вычисление приближается к 10^ 25 провалам (статья 51 порог системного риска)

## Шесть вопросов, связанных с Законом ЕС об искусственном интеллекте { #the-six-eu-ai-act-questions }

### 1. Статья 5: Является ли это запрещенной практикой искусственного интеллекта? { #1-article-5-is-this-a-prohibited-ai-practice }
**Штраф: до 35 млн евро или 7% от оборота по всему миру.**
- 8 категорий: манипулирование подсознанием, использование уязвимостей, социальная оценка, прогнозирующая полицейская деятельность, нецелевое сканирование лица, распознавание эмоций на рабочем месте/education, биометрическая классификация по чувствительным признакам, публичная биометрическая идентификация в режиме реального времени правоохранительными органами
- Бежать `ai_system_risk_classifier.py`
- Если да, то → ОСТАНОВИТЬСЯ. Не может быть размещен на рынке ЕС. Никаких исключений, кроме исключений из статьи 5(2).

### 2. Статья 6 + Приложение III: Связано ли это с высоким риском? { #2-article-6--annex-iii-is-this-high-risk }
**Приложение III триггеры высокого риска; статья 6(3) предусматривает условное исключение.**
- 8 категорий: биометрия, критически важная инфраструктура, образование, занятость, основные услуги, правоохранительные органы, миграция, правосудие
- Исключение применяется только в том случае, если статья 6(3)(a)-(d) не содержит профилирования физических лиц
- Профилирование отменяет исключение (статья 6(3) последнее предложение)
- Бежать `ai_system_risk_classifier.py`

### 3. Статья 43: Для групп высокого риска - модуль А или модуль Н? { #3-article-43-for-high-risk-module-a-or-module-h }
**Биометрия → Модуль H (нотифицированный орган) по умолчанию; другие → модуль A, если применяются гармонизированные стандарты.**
- Бежать `conformity_assessment_planner.py`
- Модуль A (приложение VI): внутренний контроль с презумпцией соответствия при применении гармонизированных стандартов, предусмотренных статьей 40
- Модуль H (Приложение VII): полная система менеджмента качества + уполномоченный орган по биометрии или там, где отсутствуют стандарты
- Приложение IV техническая документация: 8 позиций, необходимых для размещения на рынке

### 4. Статья 25: Какую роль играет компания? { #4-article-25-what-role-does-the-company-play }
**Обязательства поставщика являются самыми тяжелыми; существенная модификация превращает разработчика в поставщика.**
- Поставщик (статья 3(3)): размещен на рынке; полный раздел III + отчетность по статье 73
- Лицо, осуществляющее развертывание (статья 3(4)): Обязательства по статье 26 + Статья 27 FRIA, если государственный сектор
- Импортер (статья 3(6)): Статья 23 проверка соответствия
- Дистрибьютор (статья 3(7)): Проверка маркировки CE по статье 24
- Уполномоченный представитель (статья 22): поставщики услуг, не входящие в ЕС, должны назначить
- Бежать `ai_act_obligation_tracker.py`

### 5. Статья 50: Выполняются ли обязательства по обеспечению прозрачности? { #5-article-50-are-transparency-obligations-satisfied }
**Вступает в силу 2 августа 2025 года.**
- Статья 50(1): раскрывать информацию о взаимодействии с ИИ физическим лицам (чат-ботам, виртуальным агентам)
- Статья 50(2): помечать синтетический контент как созданный искусственным интеллектом
- Статья 50(3): раскрытие информации о распознавании эмоций/ биометрической классификации (за пределами запретов статьи 5)
- Статья 50(4): раскрывать глубокие подделки (изображения, аудио, видео) как созданные искусственным интеллектом

### 6. Статьи 51-55: Является ли это GPAI? Есть ли у этого системный риск? { #6-articles-51-55-is-this-a-gpai-does-it-have-systemic-risk }
**GPAI работает параллельно; системный риск превышает 10^25 провалов.**
- Статья 3(63): определение модели искусственного интеллекта общего назначения
- Статья 51: презумпция системного риска (обучающее вычисление за ≥ 10^25 провалов) или назначение комиссии
- Статья 53: все поставщики GPAI — Техническая документация в приложении XI, последующая информация в приложении XII, политика в области авторских прав, обучение - краткое изложение данных
- Статья 55: дополнительные обязательства GPAI в отношении системных рисков - оценка моделей, состязательное тестирование, отчетность о инцидентах, кибербезопасность
- Статья 54: Поставщики услуг GPAI, не входящие в ЕС, должны назначить уполномоченного представителя

## Воркфлоу { #workflow }

```bash
# 1. Risk classification
python ra-qm-team/skills/eu-ai-act-specialist/scripts/ai_system_risk_classifier.py systems.json

# 2. If high-risk: conformity assessment
python ra-qm-team/skills/eu-ai-act-specialist/scripts/conformity_assessment_planner.py system.json

# 3. Per-role obligation matrix
python ra-qm-team/skills/eu-ai-act-specialist/scripts/ai_act_obligation_tracker.py roles.json

# 4. Cross-framework reuse (ISO 42001 etc.)
python ../../skills/compliance-os/scripts/cross_framework_mapper.py program.json
```

## Выходной формат { #output-format }

```markdown
# EU AI Act Readiness: <system>
**Date:** YYYY-MM-DD
**Article Citations:** Every verdict below cites the specific Article.

## The Decision Being Made
[classify | conformity-route | obligation-scope | annual-refresh]

## Risk Classification
- Tier: prohibited | high_risk | limited_risk | minimal_risk
- Citation: Article X(Y) + Annex Z if applicable
- Rationale: <Article-cited rationale>
- GPAI: yes/no
- Systemic-risk GPAI: yes/no (per Article 51 10^25 FLOPs threshold)

## Conformity Assessment (if high-risk)
- Module: A | A_with_caveats | H | sectoral
- Citation: Article 43 + Annex VI/VII
- Notified body required: yes | no | optional
- Annex IV pack status: complete | in-progress | not-started

## Obligation Matrix
- Total obligations: N
- By deadline phase: 2025-02-02=A, 2025-08-02=B, 2026-08-02=C, 2027-08-02=D
- Highest-priority unmet obligation: <Article + description>

## Transparency (Article 50)
- 50(1) interaction disclosure: yes | no
- 50(2) synthetic content marking: yes | no | NA
- 50(3) emotion recognition disclosure: yes | no | NA
- 50(4) deepfake disclosure: yes | no | NA

## Cross-Framework Reuse
- ISO 42001 evidence applicable to Article 17 QMS: yes/no
- ISO 27001 evidence applicable to Article 15 cybersecurity: yes/no
- GDPR DPIA usable for Article 27 FRIA: yes/no

## Verdict
🟢 READY-FOR-EU | 🟡 GAPS-IDENTIFIED | 🔴 NOT-READY | 🚫 PROHIBITED

## Top 3 Actions
[3 concrete next steps with owner + Article-tied deadline]

## Legal Review Required
[Article-level ambiguities flagged for outside counsel: novel cases, GPAI threshold disputes, Article 5 boundary cases, Article 25 substantial-modification questions]
```

## Маршрутизация { #routing }

- `/cs:compliance-readiness` — для просмотра нескольких фреймворков (в сочетании с ISO 42001 + GDPR)
- `/cs:aims-audit` — для глубокого погружения по стандарту ISO 42001
- `/cs:caio-review` — для принятия управленческих стратегических решений по ИИ
- `/cs:gc-review` — для юридического ревью по новому делу (порог GPAI, граница статьи 5, существенное изменение)
- `/cs:decide` — для регистрации вердикта
- `/cs:freeze 30` — об обязательствах ЕС по запуску (нормативное воздействие)

## Связанный { #related }

- Агент: [`cs-ai-act-compliance`](../../agents/cs-ai-act-compliance.md)
- Скилл: [`eu-ai-act-specialist`](../../../ra-qm-team/skills/eu-ai-act-specialist/SKILL.md)
- Смежный: `../../skills/compliance-os/`, `../aims-audit/`, `../compliance-readiness/`, `../../../ra-qm-team/skills/gdpr-dsgvo-expert/`

---

**Версия:** 1.0.0
