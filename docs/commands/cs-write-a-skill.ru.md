---
title: "/cs-write-a-skill — слэш-команда для ИИ-агентов разработки"
description: "/cs: напишите скилл <название или описание> — Создайте новый скилл агента с помощью трехэтапного воркфлоу Мэтта Покока (Сбор → Черновик → Ревью). Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-write-a-skill

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/write-a-skill/commands/cs-write-a-skill.md">Источник</a></span>
</div>


**Команда:** `/cs:write-a-skill <name-or-description>`

Персона автора скилла проверяет под давлением любую фиксацию нового скилла. Шесть форсирующих вопросов перед любым слиянием, соответствующие чек-листу для ревью Мэтта Покока (Matt Pocock).

## Когда запускать { #when-to-run }

- Начинаем новый скилл с нуля
- Получение скилла из исходного (лицензированного MIT) источника
- Аудит существующего скилла в соответствии с действующими стандартами
- Ревью к PR нового скилла перед слиянием

## Шесть вопросов об авторском скилле { #the-six-skill-author-questions }

### 1. Каково описание и проходит ли оно тест Мэтта по 4 правилам? { #1-whats-the-description-and-does-it-pass-matts-4-rule-test }
**Описание - это единственное, что видит ваш агент, когда принимает решение загрузить этот скилл.**
- Максимальное количество символов - 1024
- Третье лицо (без "я" / "ты" /"мы")
- Первое предложение: что он делает (глагол действия)
- Второе предложение: "Используйте, когда [конкретные триггеры]"
- Бежать `skill_description_validator.py`

### 2. Является SKILL.md меньше 100 строк? { #2-is-skillmd-under-100-lines }
**Более 100 строк = чрезмерное кондиционирование + эталонный суп ниже по потоку.**
- Если да: отлично, отправляйте его
- Если нет: разделите воркфлоу на `references/<topic>.md`; замените встроенное содержимое указателями на 1-2 строки
- Производные от оболочки скиллы (сохраняющие исходный контент) получают документированное исключение

### 3. Есть ли претензии, связанные со сроками? { #3-are-there-time-sensitive-claims }
** Финики гниют. "По состоянию на октябрь 2024 года" становится неправильным к следующему году.**
- Удалить: "по состоянию на ГГГГ", "в ГГГГ", "выпущено ГГГГ", "обновлено ГГГГ"
- Заменить на: описание шаблона, которое не зависит от даты
- Пример: не "ISO 42001 опубликован в декабре 2023 года"; используйте "ISO 42001 (первый стандарт системы управления искусственным интеллектом)".

### 4. Согласована ли терминология? { #4-is-terminology-consistent }
** Смещение синонимов сбивает с толку агентов + читателей.**
- Выберите один из них: агент ИЛИ бот, скилл ИЛИ инструмент, пользователь ИЛИ разработчик
- Используйте выбранный термин повсюду
- Задокументируйте выбор в глоссарии, если задействовано несколько стейкхолдеров

### 5. Есть ли хотя бы 2 конкретных примера (хороший + плохой, если возможно)? { #5-are-there-at-least-2-concrete-examples-good--bad-if-possible }
** Без примеров агенты конструируют с нуля и галлюцинируют.**
- Не менее 1 блока кода
- Идеально хороший/bad контраст (рисунок Мэтта)
- Примеры должны быть доступны для запуска или копирования с возможностью вставки

### 6. Являются ли ссылки глубиной в один уровень + нет циклических ссылок? { #6-are-references-one-level-deep--no-circular-refs }
**Глубокая вложенность = агент отказывается от разрешения цепочки.**
- Плоский `references/<topic>.md` планировка
- Нет `references/category/subtopic.md`
- Никаких циклов A→B→A
- Бежать `skill_structure_validator.py`

## Воркфлоу { #workflow }

```bash
# 1. Description gate
python ../skills/write-a-skill/scripts/skill_description_validator.py path/to/SKILL.md

# 2. Structure gate
python ../skills/write-a-skill/scripts/skill_structure_validator.py path/to/skill-folder/

# 3. Combined review (Matt's 6-item checklist)
python ../skills/write-a-skill/scripts/skill_review_checklist_runner.py path/to/skill-folder/

# 4. Karpathy code-quality gate (if scripts/ exist)
python ../../karpathy-coder/skills/karpathy-coder/scripts/complexity_checker.py path/to/skill-folder/scripts/
python ../../karpathy-coder/skills/karpathy-coder/scripts/assumption_linter.py path/to/skill-folder/scripts/

# 5. Attribution check (if derived)
grep -r "derived_from\|original_author" path/to/skill-folder/
```

## Выходной формат { #output-format }

```markdown
# Skill Author Review: <skill-name>
**Date:** YYYY-MM-DD

## The Decision Being Made
[gather | draft | review | validate | derive | audit]

## Description Validation
- Length: N chars (limit 1024): pass/fail
- Third person: pass/fail
- "Use when" trigger: pass/fail
- Action verb in first sentence: pass/fail

## Structure Validation
- SKILL.md present + ≤100 lines: pass/fail (N lines)
- References one level deep: pass/fail
- No circular refs: pass/fail
- scripts/ folder: present/absent (optional)

## Review Checklist (Matt's 6 items)
- [x|/] 1. Description includes triggers
- [x|/] 2. SKILL.md under 100 lines
- [x|/] 3. No time-sensitive info
- [x|/] 4. Consistent terminology
- [x|/] 5. Concrete examples included
- [x|/] 6. References one level deep

## Karpathy Code Gate (if applicable)
- complexity_checker: PASS / WARN (with findings)
- assumption_linter: CLEAN / NOISY

## Attribution (if derived skill)
- Upstream link: present/missing
- License compatibility: yes/no
- Author credit: present/missing

## Verdict
🟢 SHIP | 🟡 WARN-WITH-JUSTIFICATION | 🔴 BLOCK

## Top 3 Actions (if not green)
[3 concrete fixes with file:line references]
```

## Маршрутизация { #routing }

- `/cs:karpathy-check` — по вопросам качества кода в скриптах/
- `/cs:tdd` — для тестирования дисциплины (отличается от гейтов качества скилла)
- `/cs:decide` — для регистрации вердикта

## Связанный { #related }

- Агент: [`cs-skill-author`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/write-a-skill/agents/cs-skill-author.md)
- Скилл: [`write-a-skill`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/write-a-skill/skills/write-a-skill/SKILL.md)
- Смежный: [`engineering/karpathy-coder`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/karpathy-coder), [`engineering/autoresearch-agent`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/autoresearch-agent)

---

**Версия:** 1.0.0
** Производное: ** Скилл Мэтта Покока по написанию (MIT) + оболочка этого репозитория
