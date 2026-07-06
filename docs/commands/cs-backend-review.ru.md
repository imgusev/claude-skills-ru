---
title: "/cs-backend-review — слэш-команда для ИИ-агентов разработки"
description: "Ревью по бэкенд—инжинирингу - отвечает на 7 форсирующих вопросов Мэтта Покока (соотношение чтения / записи + QPS, аренда, синхронизация против. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-backend-review

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/commands/cs-backend-review.md">Источник</a></span>
</div>


Используйте `cs-backend-engineer` агент (использует `context: fork`) для обработки этого запроса:

**$ARGUMENTS**

## Библиотека принудительных вопросов { #forcing-question-library }

Канонический источник: `engineering-team/skills/senior-backend/references/forcing_questions.md` (7 вопросов, по одному за ход, рекомендация + цитата из канона на каждый вопрос).

1. Читать/write коэффициент + годовой доход p99 QPS
2. Модель аренды (одиночная / общая / изолированная мультитенантная)
3. Запрос на синхронизацию/response против асинхронности (очереди) против управляемости событиями
4. Уровень конфиденциальности данных (общедоступный / внутренний / PII / PHI / PCI)
5. Монолит / модульный монолит / микросервисы (обоснование размера команды)
6. RPO и RTO
7. SLO + именованная ошибка - бюджетный потребитель

## Протокол маршрутизации { #routing-protocol }

1. ** Пройдите по 7 форсирующим вопросам** в `engineering-team/skills/senior-backend/references/forcing_questions.md` По одному за ход. Рекомендую с цитируемым каноном. Отслеживать в `/tmp/backend-grill-<date>.md`.
2. ** Критерии поверхностного уничтожения** — например, отключение "микросервисов, размер команды 5" (Newman's MonolithFirst). ОСТАНОВИТЕСЬ и примите решение.
3. **Запустите средство выбора детерминированного профиля:**
   ```bash
   python engineering-team/skills/senior-backend/scripts/backend_decision_engine.py \
     --team-size <N> --qps-p99 <N> --read-write-ratio <ratio> \
     --tenancy <single-tenant|shared-multi-tenant|isolated-multi-tenant> \
     --data-sensitivity <public|pii|phi|pci> \
     --pattern <monolith|modular-monolith|domain-bounded-services|microservices|serverless> \
     --language-preference <typescript|python|go|rust|java|kotlin|dotnet>
   ```
4. ** Используйте соответствующий профиль + именованную цепочку утверждающих ** для изменений стека / миграции схемы / внешних служб.
5. **Раскошеливаться на специалистов в порядке зависимости:**
   - `slo-architect` ВО—ПЕРВЫХ - никакого SLO, никакого дизайна
   - `api-design-reviewer` — Контракт с API
   - `database-designer` + `database-schema-designer` — схема + ERD
   - `migration-architect` — только при изменении существующей схемы
   - `observability-designer` — золотые сигналы + оповещения
   - `ci-cd-pipeline-builder` — пайплайн, соответствующий заданной частоте вращения
   - `senior-security` + `adversarial-reviewer` — перед публичным запуском
   - `ra-qm-team/*` — если чувствительность данных регулируется PHI / PCI /
   - `cs-karpathy-reviewer` — перед любым совершением

## Ожидаемый результат (дайджест из ≤ 200 слов) { #output-expectations--200-word-digest }

- Совпадающий профиль + причина
- Три целевых значения SLO (задержка p50, p99 + время безотказной работы)
- RPO + RTO
- Именованная цепочка утверждающих (технический руководитель + дежурный по вызову + администратор базы данных + ...)
- Список вызванных специалистов + пути к артефактам
- Рекомендуемый следующий дополнительный скилл

## Анти-паттерны { #anti-patterns }

- ❌ Рекомендовать Kafka / event-driven, прежде чем называть вторую команду, которой это нужно.
- ❌ Рекомендовать микросервисы без команды размером ≥ 30 человек + команда платформы + независимость от ограниченного контекста.
- ❌ Разработка API без разветвления на `api-design-reviewer`.
- ❌ Рекомендуется использовать базу данных без QPS + read/write соотношение (вопрос 1 остался без ответа).
- ❌ Автоматическое утверждение миграции производственной схемы. Всегда называйте on-call + администратор базы данных.

## Настройка { #customization }

Профили живут по адресу `engineering-team/skills/senior-backend/profiles/`. Четыре встроенных: `node-express`, `fastapi-python`, `django-monolith`, `go-or-rust-microservice` Скопируйте один из них в `<your-org>.json` и отрегулируйте ограничения /уровень SLO / цепочку утверждающих.

## Связанные команды { #related-commands }

- `/cs:fullstack-review` — объектив с полным стеком (родительский)
- `/cs:frontend-review` — для стороны потребителя API
- `/cs:engineer-grill` — перекрестная роль 21-решетка вопросов
- `/slo-design` — явный SLO-дизайн с помощью slo-архитектора
- `/karpathy-check` — Карпатия 4-ревью принципа
