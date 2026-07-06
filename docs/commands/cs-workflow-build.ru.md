---
title: "/cs-workflow-build — слэш-команда для ИИ-агентов разработки"
description: "/cs: воркфлоу-сборка <описание задачи> - Разработка и написание детерминированного воркфлоу—кода Claude (.js). Открывается с вводными вопросами. Слэш-команда для Claude Code, Codex CLI, Gemini CLI."
---

# /cs-workflow-build

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Слэш-команда</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/workflow-builder/commands/cs-workflow-build.md">Источник</a></span>
</div>


**Команда:** `/cs:workflow-build <task-description>`

Разрабатывает детерминированный мультиагентный воркфлоу-агент для инструмента воркфлоу Claude Code. Всегда открывается при вводе; никогда не записывает файл до подтверждения топологии.

## Когда запускать { #when-to-run }

- Строим новый `.claude/workflows/*.js` файл
- Автоматизация повторяющейся многоэтапной задачи для саб-агентов с новым контекстом (fresh-context)
- Принятие решения о том, требует ли вообще выполнение задачи воркфлоу (в отличие от одного агента или скилла)

## Шаг 1 — Прием (всегда первым) { #step-1--intake-always-first }

Задайте вступительный набор вопросов. Лидируй с номером 1.

1. Какую повторяемую, многоэтапную задачу вы хотите автоматизировать?
2. Какую единицу работы выполняет один саб-агент за один раз?
3. Сколько единиц измерения — известный список или обнаружено с помощью цикла?
4. Нужны ли на последующих этапах *все* предыдущие результаты сразу, или каждый элемент может выполняться сам по себе?
5. Требуется ли для какого-либо шага возврат структурированных данных (вердикт, список, оценки)?
6. Примерно на какую глубину / сколько токенов?

## Шаг 2 — Если пользователь расплывчат, сделайте вывод и предложите (не цикл вопросов) { #step-2--if-the-user-is-vague-infer-and-propose-dont-loop-on-questions }

```bash
python ../skills/workflow-builder/scripts/workflow_intake.py --task "<their request>" \
  --units unknown --stages unknown --needs-all unknown --structured unknown
```

Представьте результат в виде "вот что я бы построил и почему": рекомендуемая топология (+ занявший второе место), выбор модели для каждого этапа, ограничение бюджета и обоснование каждого выбора. Затем спросите только: "Что я должен изменить?"

## Шаг 3 — Подтвердите форму, затем создайте каркас { #step-3--confirm-the-shape-then-scaffold }

```bash
python ../skills/workflow-builder/scripts/scaffold_workflow.py \
  --topology <fan-out|pipeline|barrier|loop|judge-panel> --name <name> --description "..." \
  > .claude/workflows/<name>.js
```

## Шаг 4 — Проверка перед запуском { #step-4--validate-before-running }

```bash
python ../skills/workflow-builder/scripts/validate_workflow.py .claude/workflows/<name>.js
```

Исправляйте каждую ОШИБКУ. Предупреждения нуждаются в однострочном обосновании.

## Шаг 5 — Запустите { #step-5--run }

```bash
export CLAUDE_CODE_WORKFLOWS=1   # the feature is off by default
# Save under .claude/workflows/, then launch + monitor via /workflows.
# P = pause/resume, X = skip a sub-agent. Failed agents retry automatically.
```

## Жесткие правила (валидатор применяет их) { #the-hard-rules-validator-enforces }

1. `meta` является чистым литералом и первым оператором — никаких переменных, расширений, строк шаблона или вызовов.
2. Нет `Date.now()`, `Math.random()`, или без аргументов `new Date()` — они прерывают резюме.
3. В оркестраторе нет API файловой системы / узла — эта работа выполняется внутри `agent()`.
4. `parallel()` принимает удары (`() => agent(...)`); значение по умолчанию равно `pipeline()` если только для сцены не требуется весь предыдущий набор.
5. Защищайте каждый разомкнутый цикл счетчиком или `budget.remaining()`.
6. `results.filter(Boolean)` перед использованием параллельного/pipeline вывод.

## Выходной формат { #output-format }

```markdown
# Workflow Build: <name>
## The Decision
[intake | recommend | scaffold | validate | run]
## Recommended Topology
[fan-out | pipeline | barrier | loop | judge-panel] — why
## Model Plan
[per-stage model + reason]
## Validator Verdict
🟢 PASS | 🟡 WARN (justified) | 🔴 FAIL (with line numbers)
## Next Steps
[3 concrete actions]
```

## Связанный { #related }

- Агент: [`cs-workflow-architect`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/workflow-builder/agents/cs-workflow-architect.md)
- Скилл: [`workflow-builder`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/workflow-builder/skills/workflow-builder/SKILL.md)
- Смежный: `/cs:write-a-skill` (авторские скиллы, а не воркфлоу)

---

**Версия:** 1.0.0
