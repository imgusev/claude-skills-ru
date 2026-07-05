---
title: "Gemini CLI Skills & Plugins Guide (2026)"
description: "Установите и используйте скиллы 345 агентов с помощью Gemini CLI. Бесплатные звонки для оценки, инженерных, маркетинговых и DevOps-скилл-навыков для агента Google по кодированию."
---

# Руководство по скиллам агента CLI Gemini { #gemini-cli-agent-skills-guide }

Используйте скиллы агента 345, готовые к работе, с Gemini CLI. Все скиллы из этой коллекции совместимы со спецификацией скилла агента Gemini и устанавливаются с помощью `.gemini/skills/` каталог.

---

## Быстрая установка { #quick-install }

```bash
# Clone the repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Run the Gemini setup script (converts and installs all skills)
./scripts/gemini-install.sh

# Or convert individual skills
./scripts/convert.sh --skill frontend-design --tool gemini
./scripts/convert.sh --skill autoresearch-agent --tool gemini
```

### Как это работает { #how-it-works }

Gemini CLI считывает скиллы агента из `.gemini/skills/<skill-name>/SKILL.md` в каталоге вашего проекта. Сценарий установки преобразует все скиллы в формат, совместимый с Gemini, включая `gemini-extension.json` для реестра расширений.

---

## Зачем использовать Скиллы с Gemini CLI? { #why-use-skills-with-gemini-cli }

Бесплатный уровень Gemini CLI дает вам ** неограниченное количество ознакомительных звонков ** — идеально подходит для:

- ** Циклы автоматического поиска ** — запускайте ночные эксперименты с нулевой стоимостью API
- ** Оптимизация контента** — Юристы-оценщики LLM-judge по заголовкам, копированию, промптам
- **Ревью кода** — систематические многоходовые ревью без сжигания токенов

### Бесплатные оценщики с Gemini { #free-evaluators-with-gemini }

Скилл агента по автоматическому поиску включает в себя оценщиков LLM judge, которые работают на бесплатном уровне Gemini:

```bash
# Set up an autoresearch experiment using Gemini as the evaluator
python scripts/setup_experiment.py \
  --domain marketing \
  --name headline-optimization \
  --target content/headlines.md \
  --eval "python evaluate.py" \
  --metric ctr_score \
  --direction higher \
  --evaluator llm_judge_content

# The evaluator calls gemini CLI for scoring — free!
```

---

## Лучшие скиллы для Gemini CLI { #top-skills-for-gemini-cli }

| Скилл | Что он делает |
|-------|-------------|
| **автоматический поиск-агент** | Цикл автономного эксперимента — редактируйте, оценивайте, сохраняйте или отменяйте. Свободен с Близнецами. |
| **интерфейс-дизайн** | Производственный пользовательский интерфейс React / Tailwind с высоким качеством дизайна. |
| **pr-ревью-эксперт** | Многоходовой ревью кода: логика, безопасность, тесты, архитектура. |
| **создатель контента** | SEO-оптимизированный контент с анализом голоса бренда и фреймворками. |
| **старший-devops** | IaC, CI/CD, мониторинг и реагирование на инциденты. |
| **технический директор-консультант** | Анализ технического долга, масштабирование команды, архитектурные решения. |
| **исследователь-обобщитель** | Структурированное исследование → резюме → воркфлоу с цитированием. |
| **docker-разработка** | Оптимизация Dockerfile, многоступенчатая сборка, проверка безопасности. |

---

## Интеграция расширения Gemini { #gemini-extension-integration }

Это репозиторий включает в себя `gemini-extension.json` для расширенного реестра Gemini:

```json
{
  "name": "claude-skills",
  "version": "2.0.0",
  "description": "345 agent skills for engineering, marketing, product, and more",
  "skills": ["engineering/*", "marketing-skill/*", "product-team/*", "..."]
}
```

Увидеть [Документы по расширениям Gemini CLI](https://geminicli.com/docs/cli/skills/) для получения подробной информации об интеграции.

---

## Уровень проекта против уровня пользователя { #project-level-vs-user-level }

```bash
# Project-level (scoped to one repo)
cp -r claude-skills/.gemini/skills/ ./.gemini/skills/

# User-level (available in all projects)
mkdir -p ~/.gemini/skills/
cp -r claude-skills/.gemini/skills/* ~/.gemini/skills/
```

---

## Кросс-платформенный { #cross-platform }

Эти скиллы работают и с 10 другими агентами по кодированию:

Код Клода · OpenAI Codex · Курсор · OpenClaw · Помощник · Виндсерфинг · Килограммовый код · OpenCode · Дополнение · Антигравитация

Увидеть [полный каталог](https://github.com/alirezarezvani/claude-skills) для всех 345 скилл.

---

* Последнее обновление: март 2026 · [алирезарезвани/Клод-скиллы](https://github.com/alirezarezvani/claude-skills)*
