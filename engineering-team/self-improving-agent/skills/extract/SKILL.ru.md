---
name: "extract"
description: "Превратите проверенный шаблон или решение для отладки в автономный многоразовый скилл с помощью SKILL.md , справочные материалы и примеры. Используется, когда пользователь запускает /si:extract или запрашивает упаковать повторяющееся решение из памяти в скилл."
---

# /si:извлекать — Создавать скиллы из шаблонов { #siextract--create-skills-from-patterns }

Преобразует повторяющийся шаблон или решение для отладки в автономный, переносимый скилл, который может быть установлен в любом проекте.

## Использование { #usage }

```
/si:extract <pattern description>                  # Interactive extraction
/si:extract <pattern> --name docker-m1-fixes       # Specify skill name
/si:extract <pattern> --output ./skills/            # Custom output directory
/si:extract <pattern> --dry-run                     # Preview without creating files
```

## Когда извлекать { #when-to-extract }

Обучение дает право на получение скилла, если любой из этих параметров верен:

| Критерий | Сигнал |
|---|---|
| **Повторяющийся** | Одна и та же проблема в более чем 2 проектах |
| **Неочевидный** | Требовалась реальная отладка, чтобы обнаружить |
| **Широко применимый** | Не привязан к одной конкретной кодовой базе |
| **Комплексное решение** | Многоступенчатое исправление, о котором легко забыть |
| **Помечено пользователем** | "Сохраните это как скилл", "Я хочу использовать это повторно" |

## Воркфлоу { #workflow }

### Шаг 1: Определите шаблон { #step-1-identify-the-pattern }

Прочтите описание пользователя. Автоматический поиск в памяти связанных записей:

```bash
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"
grep -rni "<keywords>" "$MEMORY_DIR/"
```

Если они найдены в автоматической памяти, используйте эти записи в качестве исходного материала. Если нет, используйте непосредственно описание пользователя.

### Шаг 2: Определите сферу применения скилла { #step-2-determine-skill-scope }

Задать (максимум 2 вопроса):
- "Какую проблему это решает?" (если не ясно)
- "Следует ли сюда включать примеры кода?" (если применимо)

### Шаг 3: Сгенерируйте название скилла { #step-3-generate-skill-name }

Правила присвоения имен:
- Строчные буквы, дефисы между словами
- Описательный, но краткий (2-4 слова)
- Примеры: `docker-m1-fixes`, `api-timeout-patterns`, `pnpm-workspace-setup`

**Зарезервированные фрагменты — не должны фигурировать в названии скилла:**
- `claude`
- `anthropic`

Чтобы получить скиллы о самом коде Claude, воспользуйтесь `cc-` префикс вместо:
- ❌ `claude-code-settings` → ✅ `cc-settings`
- ❌ `claude-code-maintenance` → ✅ `cc-maintenance`
- ❌ `claude-mcp-tools` → ✅ `cc-mcp-tools`
- ❌ `claude-plugin-development` → ✅ `cc-plugin-development`

Перед написанием каталога скилл сверьте предлагаемое название с этим списком.
Если присутствует зарезервированный фрагмент, преобразуйте его (удалите фрагмент или замените
 `claude*`/`anthropic*` префикс с `cc-`) и подтвердите это у пользователя.

### Шаг 4: Создайте файлы с скиллами { #step-4-create-the-skill-files }

** Порождать `skill-extractor` агент** для фактической генерации файла.

Агент создает:

```
<skill-name>/
├── SKILL.md            # Main skill file with frontmatter
├── README.md           # Human-readable overview
└── reference/          # (optional) Supporting documentation
    └── examples.md     # Concrete examples and edge cases
```

### Шаг 5: SKILL.md структура { #step-5-skillmd-structure }

Сгенерированный SKILL.md необходимо следовать этому формату:

```markdown
---
name: "skill-name"
description: "<one-line description>. Use when: <trigger conditions>."
---

# <Skill Title>

> One-line summary of what this skill solves.

## Quick Reference

| Problem | Solution |
|---------|----------|
| {{problem 1}} | {{solution 1}} |
| {{problem 2}} | {{solution 2}} |

## The Problem

{{2-3 sentences explaining what goes wrong and why it's non-obvious.}}

## Solutions

### Option 1: {{Name}} (Recommended)

{{Step-by-step with code examples.}}

### Option 2: {{Alternative}}

{{For when Option 1 doesn't apply.}}

## Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Option 1 | {{pros}} | {{cons}} |
| Option 2 | {{pros}} | {{cons}} |

## Edge Cases

- {{edge case 1 and how to handle it}}
- {{edge case 2 and how to handle it}}
```

### Шаг 6: Качественные гейты { #step-6-quality-gates }

Перед завершением работы проверьте:

- [ ] SKILL.md имеет действительный YAML frontmatter с `name` и `description`
- [ ] `name` соответствует названию папки (строчные буквы, дефисы)
- [ ] `name` не содержит зарезервированных фрагментов `claude` или `anthropic` (использовать `cc-` префикс для скилла кода Клода)
- [ ] Описание включает в себя условия "Использовать, когда:" для триггера
- [ ] Решения являются самодостаточными (внешний контекст не требуется)
- [ ] Примеры кода являются полными и пригодными для копирования и вставки
- [ ] Нет жестко заданных значений для конкретного проекта (пути, URL-адреса, учетные данные)
- [ ] Никаких ненужных зависимостей

### Шаг 7: Отчет { #step-7-report }

```
✅ Skill extracted: {{skill-name}}

Files created:
  {{path}}/SKILL.md          ({{lines}} lines)
  {{path}}/README.md         ({{lines}} lines)
  {{path}}/reference/examples.md  ({{lines}} lines)

Install: /plugin install (copy to your skills directory)
Publish: clawhub publish {{path}}

Source: MEMORY.md entries at lines {{n, m, ...}} (retained — the skill is portable, the memory is project-specific)
```

## Примеры { #examples }

### Извлечение шаблона отладки { #extracting-a-debugging-pattern }

```
/si:extract "Fix for Docker builds failing on Apple Silicon with platform mismatch"
```

Создает `docker-m1-fixes/SKILL.md` с:
- Сообщение об ошибке несоответствия платформы
- Три решения (флаг сборки, Dockerfile, docker-compose)
- Таблица компромиссов
- Примечание о производительности эмуляции Rosetta 2

### Извлечение шаблона воркфлоу { #extracting-a-workflow-pattern }

```
/si:extract "Always regenerate TypeScript API client after modifying OpenAPI spec"
```

Создает `api-client-regen/SKILL.md` с:
- Почему необходима ручная регенерация
- Точная последовательность команд
- Фрагмент интеграции CI
- Распространенные режимы отказа

## Советы { #tips }

- Извлеките шаблоны, которые сэкономили бы время в *другом* проекте
- Сосредоточьтесь на скиллах — по одной задаче на скилл
- Включите сообщения об ошибках, которые люди будут искать
- Проверьте свой скилл, прочитав его без первоначального контекста — имеет ли это смысл?
