---
title: "Корабельные гейты { #ship-gate } — Агентский скилл для Codex и OpenClaw"
description: ">. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Корабельные гейты { #ship-gate }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `ship-gate`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/ship-gate/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Предварительный аудит, который сканирует кодовую базу и передает отчеты/fail/manual
по 8 категориям, прежде чем что-либо отправится.

## Поведение перехвата { #intercept-behavior }

Когда пользователь говорит "запустить в производство", "депло", "отправить его", "начать работу"
или аналогичные фразы, связанные с намерением депло, не приступайте к развертыванию. Вместо этого:

1. Спросите: "Вы запустили корабельные гейты? Хотите, чтобы я просканировал сейчас?"
2. Если да, выполните полный аудит, приведенный ниже.
3. Если пользователь говорит, что он уже запустил его, спросите, когда. Если более 24 часов
   назад или, если с тех пор код изменился, рекомендуем выполнить повторный запуск.

## Как это работает { #how-it-works }

### Шаг 1: Обнаружение стека { #step-1-detect-stack }

Выполните эти проверки, чтобы идентифицировать стек проекта:

```
Framework detection:
  package.json exists        -> Node.js project
    "next" in dependencies   -> Next.js
    "react" in dependencies  -> React (if not Next.js)
    "vue" in dependencies    -> Vue
    "svelte" in dependencies -> Svelte
    "astro" in dependencies  -> Astro
    "express" in dependencies -> Express
    "fastify" in dependencies -> Fastify
    "hono" in dependencies   -> Hono
  requirements.txt or pyproject.toml -> Python project
    "django" present         -> Django
    "flask" present          -> Flask
    "fastapi" present        -> FastAPI
  go.mod exists              -> Go project
  Cargo.toml exists          -> Rust project

Database detection:
  "@supabase/supabase-js" in package.json -> Supabase
  supabase/ directory exists              -> Supabase
  "prisma" in dependencies                -> Prisma (check schema for DB type)
  "mongoose" in dependencies              -> MongoDB
  "pg" or "postgres" in dependencies      -> PostgreSQL
  firebase.json or .firebaserc exists     -> Firebase

Deploy target detection:
  vercel.json or .vercel/ exists          -> Vercel
  netlify.toml exists                     -> Netlify
  Dockerfile exists                       -> Docker/VPS
  fly.toml exists                         -> Fly.io
  railway.json exists                     -> Railway
  .platform/applications.yaml            -> Platform.sh

Auth detection:
  "@clerk" in dependencies                -> Clerk
  "next-auth" in dependencies             -> NextAuth
  "@supabase/auth-helpers" in deps        -> Supabase Auth
  "firebase/auth" in imports              -> Firebase Auth

AI/LLM detection:
  "openai" in dependencies                -> OpenAI
  "@anthropic-ai/sdk" in dependencies     -> Claude API
  "@google/generative-ai" in deps         -> Gemini
```

Сообщите об обнаруженном стеке, прежде чем продолжить. Это определяет, какие проверки
являются релевантными. Проверяет, помечен ли определенный стек в `references/checks.md`
пропускаются, если этот стек не обнаружен.

### Шаг 2: Запустите автоматические проверки { #step-2-run-automated-checks }

Запустите категории в таком порядке: SEC, DB, CODE, DEP, AI, ДЕПЛО, FE, OBS.
Безопасность и база данных на первом месте, потому что они дают наиболее важные результаты.

Для каждой категории запустите все проверки с возможностью автоматического сканирования из
`references/checks.md` используя шаблоны в `references/patterns.md`.

Сообщайте о ходе выполнения после завершения каждой категории:
```
[1/8] Security: 3 FAIL, 12 PASS, 3 SKIP
[2/8] Database: 1 FAIL, 5 PASS, 6 SKIP
...
```

Сообщайте о результатах в виде:
- ПРОПУСК: проверка пройдена
- ОШИБКА: проблема найдена (с указанием пути к файлу и номера строки)
- ПРОПУСТИТЬ: неприменимо к этому стеку

### Шаг 3: Ручное подтверждение { #step-3-manual-confirmation }

Для проверок, которые невозможно автоматизировать (протестировано восстановление из резервной копии,
существует план отката, промежуточный тест пройден), представьте их в виде чек-листа и попросите пользователя
подтвердить каждую из них.

### Шаг 4: Вердикт { #step-4-verdict }

Классифицируйте результаты по трем степеням серьезности:
- КРИТИЧНО: необходимо исправить перед отправкой (секреты раскрыты, авторизация на маршрутах отсутствует,
  нет HTTPS, векторов SQL-инъекций, нет RLS в таблицах Supabase)
- ВЫСОКИЙ: следует исправить перед отправкой (без границ ошибок, без ограничения скорости,
  консоль.журналы в рабочем состоянии, разбивка на страницы отсутствует)
- РЕКОМЕНДАЦИЯ: рекомендуется, но не блокируется (нет тегов OG, нет пользовательского 404,
  никакой аналитики, никакого SBOM)

Конечный результат:

```
SHIP GATE REPORT
================
Stack: Next.js + Supabase + Vercel
Scan time: 12s

CRITICAL (3 items, must fix)
  FAIL  [SEC-01] API key found in src/lib/api.ts:14
  FAIL  [DB-07] RLS not enabled on "profiles" table
  FAIL  [SEC-05] No CSRF protection on /api/checkout

HIGH (5 items, should fix)
  FAIL  [CODE-01] 12 console.log statements in production code
  FAIL  [CODE-03] Empty catch block in src/utils/auth.ts:45
  FAIL  [DEP-04] 3 critical npm audit vulnerabilities
  FAIL  [DEPLOY-05] No rollback plan documented
  MANUAL [DEPLOY-06] Staging test not confirmed

ADVISORY (4 items, recommended)
  FAIL  [FE-01] Missing OG meta tags
  FAIL  [FE-03] No custom 404 page
  PASS  [OBS-01] Error monitoring configured
  SKIP  [AI-01] No AI/LLM usage detected

VERDICT: DO NOT SHIP (3 critical issues)
Fix critical items and re-run.
```

Если критических предметов не осталось, вердикт таков: ГОТОВО К ОТПРАВКЕ.
Если остаются только товары высокого качества, вердикт таков: ОТПРАВЛЯЙТЕ С ОСТОРОЖНОСТЬЮ (признайте риски).

## Категории { #categories }

Восемь категорий, каждая с кодовым префиксом. Полная информация о регистрации в
`references/checks.md`.

| Префикс | Категория | Авто | Руководство пользователя | Инструмент |
|--------|----------|------|--------|------|
| СЕК. | Безопасность | 15 | 3 | 0 |
| ДБ | База данных | 7 | 5 | 0 |
| ДЕПЛОЮ | Развертывание | 3 | 8 | 0 |
| КОД | Качество кода | 11 | 0 | 1 |
| Искусственный интеллект | Безопасность AI/LLM | 5 | 3 | 0 |
| ДЕП | Зависимости | 5 | 0 | 1 |
| FE | Качество интерфейса | 7 | 3 | 0 |
| ОБС | Наблюдаемость | 2 | 5 | 0 |

## Сфера применения { #scope }

Этот скилл проводит аудит. Это не исправляется. Когда он обнаруживает проблемы, он сообщает
о них с указанием местоположения файлов и указаниями по устранению. Пользователь или другой
скилл (систематическая отладка, бэкенд-шаблоны, shadcn-стек) обрабатывает
исправление.

Этот скилл не:
- Настройка пайплайнов CI/CD
- Инфраструктура обеспечения
- Настройка инструментов мониторинга
- Запускается после развертывания (только для предварительного деплою)

## Точки интеграции { #integration-points }

- **karpathy-coder**: запуск ship-гейта после прохождения проверки karpathy - сначала простота, затем готовность к производству
- ** состязательный рецензент**: ревью глубокой безопасности для элементов, помеченных на гейтах как критические
- ** ручное тестирование безопасности**: методология тестирования на проникновение для получения результатов категории SEC
- **code-reviewer**: общий ревью качества кода дополняет автоматические проверки ship-гейта
