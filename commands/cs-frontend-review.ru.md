---
description: "Ревью Frontend engineering — отвечает на 7 форсирующих вопросов Мэтта Покока (устройство, цель LCP, рендеринг, бюджет пакета, SEO vs auth, система проектирования, WCAG), выбирает фреймворк + профиль рендеринга, делится на специалистов (a11y-аудит, performance-profiler, epic-design). Вызывает агента cs-frontend-engineer с помощью контекстной вилки."
argument-hint: "<problem or surface to review>"
---

# /cs:frontend-ревью — ревью по разработке интерфейсов { #csfrontend-review--frontend-engineering-review }

Используйте `cs-frontend-engineer` агент (использует `context: fork`) для обработки этого запроса:

**$АРГУМЕНТЫ**

## Библиотека принудительных вопросов { #forcing-question-library }

Канонический источник: `engineering-team/skills/senior-frontend/references/forcing_questions.md` (7 вопросов, по одному за ход, рекомендация + цитата из канона на каждый вопрос).

1. Основное устройство + сеть (настольный компьютер-оптоволокно / мобильный-4G / бюджетный Android / корпоративный)
2. Цель LCP на основном устройстве (миллисекунды)
3. Серверные компоненты против SPA, SSR и SSG
4. Бюджет пакета JS для каждого маршрута (КБ в сжатом виде)
5. Зависимый от SEO или защищенный от авторизации
6. Дизайн-расположение системы (Figma + токены / специальный попутный ветер / безголовый пользовательский интерфейс)
7. Цель WCAG (AA / AAA / наилучшие усилия) + владелец специальных возможностей

## Протокол маршрутизации { #routing-protocol }

1. ** Пройдите по 7 форсирующим вопросам** в `engineering-team/skills/senior-frontend/references/forcing_questions.md` По одному за ход. Рекомендую с цитируемым каноном. Отслеживать в `/tmp/frontend-grill-<date>.md`.
2. ** Критерии поверхностного уничтожения ** — например, поездки "зависящие от SEO + только для СПА". ОСТАНОВИТЕСЬ и примите решение.
3. **Запустите средство выбора детерминированного профиля:**
   ```bash
   python engineering-team/skills/senior-frontend/scripts/frontend_decision_engine.py \
     --primary-device <mobile-4g|desktop-fiber|low-end-android|corporate-network> \
     --lcp-target-ms <N> --seo-dependent <true|false> \
     --auth-walled <true|false> --team-size <N>
   ```
4. ** Нанесите на поверхность соответствующий профиль + компромисс, занявший второе место** (если в пределах 15%).
5. ** Разделитесь на специалистов** (по одному, сначала в глубину):
   - `a11y-audit` для базовой линии WCAG (всегда)
   - `performance-profiler` для аудита пакета CWV baseline + bundle
   - `epic-design` только для `astro-or-static` маркетинговые поверхности
   - `apple-hig-expert` только для собственных поверхностей Apple-platform-native surfaces
   - `dependency-auditor` перед любым крупным релизом
   - `cs-karpathy-reviewer` перед любым совершением

## Ожидаемый результат (дайджест из ≤ 200 слов) { #output-expectations--200-word-digest }

- Совпадающий профиль + причина
- Три цели CWV (LCP, INP, CLS) на p75 на основном устройстве
- Бюджет пакета JS для каждого маршрута в KB-gzip
- Назван владелец a11y
- Список вызванных специалистов + пути к артефактам
- Рекомендуемый следующий дополнительный скилл

## Анти-паттерны { #anti-patterns }

- ❌ Рекомендуем использовать Next App Router в качестве универсального маршрутизатора по умолчанию. Устройство + SEO + авторизация определяют рендеринг.
- ❌ Установка "быстрого" в качестве цели. Выберите число в ms.
- ❌ Пропуск `a11y-audit` на поверхности, обращенной к клиенту.
- ❌ Переопределение логики профилирования производительности. Раскошелиться на `performance-profiler`.

## Настройка { #customization }

Профили живут по адресу `engineering-team/skills/senior-frontend/profiles/`. Четыре встроенных: `next-app-router`, `remix-or-sveltekit`, `vite-spa`, `astro-or-static` Скопируйте один из них в `<your-org>.json` и отрегулируйте, чтобы добавить значения вашей организации по умолчанию.

## Связанные команды { #related-commands }

- `/cs:fullstack-review` — объектив с полным стеком (родительский)
- `/cs:backend-review` — для контракта API на стороне потребителя
- `/cs:engineer-grill` — перекрестная роль 21-решетка вопросов
- `/karpathy-check` — Карпатия 4-ревью принципа
