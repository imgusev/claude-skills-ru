---
title: "Разработка Docker { #docker-development } — Агентский скилл для Codex и OpenClaw"
description: "Скилл агента разработки Docker и контейнеров и плагин для оптимизации файлов Docker, оркестрации docker-compose, многоэтапных сборок и усиления. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Разработка Docker { #docker-development }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `docker-development`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/docker-development/skills/docker-development/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> Изображения меньшего размера. Более быстрые сборки. Защищайте контейнеры. Никаких догадок.

Самоуверенный воркфлоу Docker, который превращает раздутые файлы Docker в контейнеры производственного класса. Охватывает оптимизацию, многоэтапные сборки, оркестрацию compose и усиление безопасности.

Не учебник по Docker — это набор конкретных решений о том, как создавать контейнеры, которые не тратят впустую время, пространство или атакуют поверхность.

---

## Слэш-команды { #slash-commands }

| Команда | Что он делает |
|---------|-------------|
| `/docker:optimize` | Проанализируйте и оптимизируйте файл Dockerfile с точки зрения размера, скорости и кэширования слоев |
| `/docker:compose` | Создайте или улучшите docker-compose.yml с использованием лучших практик |
| `/docker:security` | Аудит файла Docker или запущенного контейнера на предмет проблем с безопасностью |

---

## Когда активируется этот Скилл { #when-this-skill-activates }

Распознать эти шаблоны у пользователя:

- "Оптимизируйте этот файл Dockerfile"
- "Моя сборка Docker выполняется медленно"
- "Создайте docker-compose для этого проекта"
- "Защищен ли этот файл Dockerfile?"
- "Уменьшите размер моего изображения Docker"
- "Настройка многоступенчатых сборок"
- "Лучшие практики Docker для [язык/фреймворк]"
- Любой запрос, включающий: Dockerfile, docker-compose, контейнер, размер изображения, кэш сборки, безопасность Docker

Если у пользователя есть Dockerfile или он хочет что-то поместить в контейнер → применяется этот скилл.

---

## Воркфлоу { #workflow }

### `/docker:optimize` — Оптимизация файла Dockerfile { #dockeroptimize--dockerfile-optimization }

1. **Анализ текущего состояния**
   - Прочитайте файл Dockerfile
   - Определите базовое изображение и его размер
   - Подсчитайте количество слоев (каждый ЗАПУСК/КОПИРОВАНИЕ/ДОБАВЛЕНИЕ = 1 слой)
   - Проверьте наличие распространенных анти-шаблонов

2. **Примените чек-лист оптимизации к своим задачам.**

   ```
   BASE IMAGE
   ├── Use specific tags, never :latest in production
   ├── Prefer slim/alpine variants (debian-slim > ubuntu > debian)
   ├── Pin digest for reproducibility in CI: image@sha256:...
   └── Match base to runtime needs (don't use python:3.12 for a compiled binary)

   LAYER OPTIMIZATION
   ├── Combine related RUN commands with && \
   ├── Order layers: least-changing first (deps before source code)
   ├── Clean package manager cache in the same RUN layer
   ├── Use .dockerignore to exclude unnecessary files
   └── Separate build deps from runtime deps

   BUILD CACHE
   ├── COPY dependency files before source code (package.json, requirements.txt, go.mod)
   ├── Install deps in a separate layer from code copy
   ├── Use BuildKit cache mounts: --mount=type=cache,target=/root/.cache
   └── Avoid COPY . . before dependency installation

   MULTI-STAGE BUILDS
   ├── Stage 1: build (full SDK, build tools, dev deps)
   ├── Stage 2: runtime (minimal base, only production artifacts)
   ├── COPY --from=builder only what's needed
   └── Final image should have NO build tools, NO source code, NO dev deps
   ```

3. **Сгенерировать оптимизированный файл Dockerfile**
   - Примените все соответствующие оптимизации
   - Добавляйте встроенные комментарии, объясняющие каждое решение
   - Сообщить о предполагаемом уменьшении размера

4. **Проверка подлинности**
   ```bash
   python3 scripts/dockerfile_analyzer.py Dockerfile
   ```

### `/docker:compose` — Конфигурация создания Docker { #dockercompose--docker-compose-configuration }

1. **Идентификация служб**
   - Приложение (веб, API, рабочий)
   - База данных (postgres, mysql, redis, mongo)
   - Кэш (redis, memcached)
   - Очередь (rabbitmq, kafka)
   - Обратный прокси (nginx, traefik, caddy)

2. **Применяйте лучшие практики составления**

   ```
   SERVICES
   ├── Use depends_on with condition: service_healthy
   ├── Add healthchecks for every service
   ├── Set resource limits (mem_limit, cpus)
   ├── Use named volumes for persistent data
   └── Pin image versions

   NETWORKING
   ├── Create explicit networks (don't rely on default)
   ├── Separate frontend and backend networks
   ├── Only expose ports that need external access
   └── Use internal: true for backend-only networks

   ENVIRONMENT
   ├── Use env_file for secrets, not inline environment
   ├── Never commit .env files (add to .gitignore)
   ├── Use variable substitution: ${VAR:-default}
   └── Document all required env vars

   DEVELOPMENT vs PRODUCTION
   ├── Use compose profiles or override files
   ├── Dev: bind mounts for hot reload, debug ports exposed
   ├── Prod: named volumes, no debug ports, restart: unless-stopped
   └── docker-compose.override.yml for dev-only config
   ```

3. **Сгенерировать файл compose**
   - Вывод docker-compose.yml с проверками работоспособности, сетями, томами
   - Сгенерируйте .env.example со всеми необходимыми задокументированными переменными
   - Добавить аннотации к профилю разработчика/продукта

### `/docker:security` — Аудит безопасности контейнеров { #dockersecurity--container-security-audit }

1. **Аудит файла Dockerfile**

   | Проверьте | Серьезность | Исправить |
   |-------|----------|-----|
   | Запуск от имени root | Критический | Добавить `USER nonroot` после создания пользователя |
   | Использование :последнего тега | Высокий | Привязать к конкретной версии |
   | Секреты в ENV/ARG | Критический | Используйте секреты BuildKit: `--mount=type=secret` |
   | КОПИРОВАТЬ с помощью широкого глобуса | Средний | Используйте определенные пути, добавьте .dockerignore |
   | Ненужное РАЗОБЛАЧЕНИЕ | Низкий | Открывайте только те порты, которые использует приложение |
   | Никакой ПРОВЕРКИ ЗДОРОВЬЯ | Средний | Добавляйте проверку работоспособности с соответствующим интервалом |
   | Привилегированные инструкции | Высокий | Избегайте `--privileged`, отбрасывать возможности |
   | Сохраненный кэш менеджера пакетов | Низкий | Очистите в том же рабочем слое |

2. **Проверка безопасности во время выполнения**

   | Проверьте | Серьезность | Исправить |
   |-------|----------|-----|
   | Контейнер, запущенный от имени root | Критический | Установите пользователя в Dockerfile или compose |
   | Доступная для записи корневая файловая система | Средний | Использование `read_only: true` в compose |
   | Все возможности сохранены | Высокий | Отбросьте все, добавьте только необходимое: `cap_drop: [ALL]` |
   | Никаких ограничений по ресурсам | Средний | Набор `mem_limit` и `cpus` |
   | Режим сети хоста | Высокий | Используйте мост или пользовательскую сеть |
   | Чувствительные крепления | Критический | Никогда не монтируйте /etc, /var/run/docker.носок в толчке |
   | Драйвер журнала не настроен | Низкий | Набор `logging:` с ограничениями по размеру |

3. **Создание отчета о безопасности**
   ```
   SECURITY AUDIT — [Dockerfile/Image name]
   Date: [timestamp]

   CRITICAL: [count]
   HIGH:     [count]
   MEDIUM:   [count]
   LOW:      [count]

   [Detailed findings with fix recommendations]
   ```

---

## Оснастка { #tooling }

### `scripts/dockerfile_analyzer.py` { #scriptsdockerfile_analyzerpy }

Утилита CLI для статического анализа файлов Docker.

**Особенности:**
- Количество слоев и предложения по оптимизации
- Анализ базового изображения с оценкой размера
- Обнаружение анти-паттернов (более 15 правил)
- Отмечена проблема безопасности
- Многоступенчатое обнаружение и проверка сборки
- Вывод JSON и текста

**Использование:**
```bash
# Analyze a Dockerfile
python3 scripts/dockerfile_analyzer.py Dockerfile

# JSON output
python3 scripts/dockerfile_analyzer.py Dockerfile --output json

# Analyze with security focus
python3 scripts/dockerfile_analyzer.py Dockerfile --security

# Check a specific directory
python3 scripts/dockerfile_analyzer.py path/to/Dockerfile
```

### `scripts/compose_validator.py` { #scriptscompose_validatorpy }

Утилита CLI для проверки файлов docker-compose.

**Особенности:**
- Проверка зависимости сервиса
- Обнаружение присутствия при проверке работоспособности
- Анализ конфигурации сети
- Проверка подключения тома
- Аудит переменной среды
- Обнаружение конфликта портов
- Оценка наилучшей практики

**Использование:**
```bash
# Validate a compose file
python3 scripts/compose_validator.py docker-compose.yml

# JSON output
python3 scripts/compose_validator.py docker-compose.yml --output json

# Strict mode (fail on warnings)
python3 scripts/compose_validator.py docker-compose.yml --strict
```

---

## Многоэтапные шаблоны построения { #multi-stage-build-patterns }

### Шаблон 1: Скомпилированный язык (Go, Rust, C++) { #pattern-1-compiled-language-go-rust-c }

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server ./cmd/server

# Runtime stage
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

### Образец 2: Node.js / Машинописный текст { #pattern-2-nodejs--typescript }

```dockerfile
# Dependencies stage
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production=false

# Build stage
FROM deps AS builder
COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001
COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY package.json ./
USER appuser
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Шаблон 3: Python { #pattern-3-python }

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
COPY --from=builder /install /usr/local
COPY . .
USER appuser
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Дерево принятия решений по базовому изображению { #base-image-decision-tree }

```
Is it a compiled binary (Go, Rust, C)?
├── Yes → distroless/static or scratch
└── No
    ├── Need a shell for debugging?
    │   ├── Yes → alpine variant (e.g., node:20-alpine)
    │   └── No → distroless variant
    ├── Need glibc (not musl)?
    │   ├── Yes → slim variant (e.g., python:3.12-slim)
    │   └── No → alpine variant
    └── Need specific OS packages?
        ├── Many → debian-slim
        └── Few → alpine + apk add
```

---

## Проактивные триггеры { #proactive-triggers }

Отмечайте их, не спрашивая:

- **Dockerfile использует :последнюю версию** → Предлагает привязать к определенному тегу версии.
- **No .dockerignore** → Создайте его. Как минимум: `.git`, `node_modules`, `__pycache__`, `.env`.
- **СКОПИРУЙТЕ . . перед установкой зависимостей** → Сбой кэша. Измените порядок, чтобы сначала установить deps.
- **Запуск от имени root** → Добавить инструкцию ПОЛЬЗОВАТЕЛЯ. Никаких исключений для производства.
- **Секреты в ENV или ARG** → Используйте секретные монтировки BuildKit. Никогда не выпекайте секреты слоями.
- **Объем изображения более 1 ГБ** → Требуется многоэтапная сборка. Нет причин для создания такого большого производственного изображения.
- ** Нет проверки работоспособности ** → Добавьте ее. Оркестраторам (Compose, K8s) это необходимо для правильного управления жизненным циклом.
- **apt-получить без очистки в том же слое** → `rm -rf /var/lib/apt/lists/*` в том же ПРОГОНЕ.

---

## Установка { #installation }

### Однострочник (любой инструмент) { #one-liner-any-tool }
```bash
git clone https://github.com/imgusev/claude-skills-ru.git
cp -r claude-skills-ru/engineering/docker-development ~/.claude/skills/
```

### Установка с несколькими инструментами { #multi-tool-install }
```bash
./scripts/convert.sh --skill docker-development --tool codex|gemini|cursor|windsurf|openclaw
```

### Открытый коготь { #openclaw }
```bash
clawhub install cs-docker-development
```

---

## Связанные скиллы { #related-skills }

- **старший-devops** — Более широкий охват DevOps (CI/CD, IaC, мониторинг). Дополнительное использование docker-разработки для работы с конкретными контейнерами, senior-devops для пайплайна и инфраструктуры.
- **старший-безопасность** — Безопасность приложений. Дополнительная разработка - docker- охватывает безопасность контейнеров, senior-security - угрозы прикладного уровня.
- **агент автоматического поиска ** - Может оптимизировать время сборки Docker или размеры изображений в качестве измеримых экспериментов.
- **ci-cd-пайплайн-строитель** — строительство пайплайна. Комплементарная разработка - docker-создает контейнеры, ci-cd-пайплайн-builder деплою их.
