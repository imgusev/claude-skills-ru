---
title: "Конструктор пайплайнов CI/CD { #cicd-pipeline-builder } — Агентский скилл для Codex и OpenClaw"
description: "Генерируйте прагматичные пайплайны CI/CD на основе обнаруженных сигналов стека проекта — быстрая генерация базовой линии, повторяемые проверки, этапы. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Конструктор пайплайнов CI/CD { #cicd-pipeline-builder }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `ci-cd-pipeline-builder`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/ci-cd-pipeline-builder/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Уровень:** МОЩНЫЙ  
**Категория:** Инженерия  
**Домен:** DevOps / Автоматизация

## Обзор { #overview }

Используйте этот скилл для создания прагматичных пайплайнов CI/CD на основе обнаруженных сигналов стека проекта, а не догадок. В нем основное внимание уделяется быстрому созданию базовых данных, повторяемым проверкам и этапам развертывания с учетом требований окружающей среды.

## Основные возможности { #core-capabilities }

- Определение языка/среды выполнения/инструментария из файлов репозитория
- Рекомендуемые этапы КИ (`lint`, `test`, `build`, `deploy`)
- Генерировать действия GitHub или стартовые пайплайны GitLab CI
- Включите кэширование и матричную стратегию, основанную на обнаруженном стеке
- Выдает машиночитаемый вывод обнаружения для автоматизации
- Приведите логику пайплайна в соответствие с файлами блокировки проекта и командами сборки

## Когда использовать { #when-to-use }

- Загрузка CI для нового репозитория
- Замена хрупких скопированных файлов пайплайна
- Переход между действиями GitHub и GitLab CI
- Аудит соответствия шагов пайплайна фактическому стеку
- Создание воспроизводимой базовой линии перед пользовательским упрочнением

## Ключевые Воркфлоу { #key-workflows }

### 1. Обнаружение стека { #1-detect-stack }

```bash
python3 scripts/stack_detector.py --repo . --format text
python3 scripts/stack_detector.py --repo . --format json > detected-stack.json
```

Поддерживает ввод через stdin или `--input` файл для автономного анализа полезных нагрузок.

### 2. Сгенерируйте Пайплайн на основе обнаружения { #2-generate-pipeline-from-detection }

```bash
python3 scripts/pipeline_generator.py \
  --input detected-stack.json \
  --platform github \
  --output .github/workflows/ci.yml \
  --format text
```

Или сквозной из репозитория напрямую:

```bash
python3 scripts/pipeline_generator.py --repo . --platform gitlab --output .gitlab-ci.yml
```

### 3. Проверка перед объединением { #3-validate-before-merge }

1. Подтвердите наличие команд в проекте (`test`, `lint`, `build`).
2. Запустите сгенерированный пайплайн локально, где это возможно.
3. Убедитесь, что необходимые секреты/переменные env задокументированы.
4. Сохраняйте гейт заданий на деплою с помощью защищенных филиалов/сред.

### 4. Безопасно добавляйте этапы развертывания { #4-add-deployment-stages-safely }

- Начните только с CI (`lint/test/build`).
- Добавьте промежуточное депло с явным контекстом среды.
- Добавьте производственное депло с ручным гейтом/утверждением.
- Сохраняйте команды раскатки/отката назад явными и доступными для проверки.

## Интерфейсы сценариев { #script-interfaces }

- `python3 scripts/stack_detector.py --help`
  - Обнаруживает сигналы стека из файлов репозитория
  - Считывает необязательный ввод JSON из stdin/`--input`
- `python3 scripts/pipeline_generator.py --help`
  - Генерирует GitHub/GitLab YAML из полезной нагрузки обнаружения
  - Записывает в стандартный вывод или `--output`

## Ссылки { #references }

- [ссылки/пайплайн-дизайн-примечания.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/ci-cd-pipeline-builder/references/pipeline-design-notes.md) — распространенные подводные камни, лучшие практики, эвристики обнаружения, стратегия генерации, заметки о решениях платформы, чек-лист проверки перед слиянием и рекомендации по масштабированию
- [ссылки/github-actions-шаблоны.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/ci-cd-pipeline-builder/references/github-actions-templates.md)
- [ссылки/gitlab-ci-шаблоны.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/ci-cd-pipeline-builder/references/gitlab-ci-templates.md)
- [ссылки/развертывание-гейты.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/ci-cd-pipeline-builder/references/deployment-gates.md)
- [README.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/ci-cd-pipeline-builder/README.md)
