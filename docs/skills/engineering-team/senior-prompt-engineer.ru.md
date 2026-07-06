---
title: "Старший инженер по промпту { #senior-prompt-engineer } — Агентский скилл и плагин Codex"
description: "Используйте, когда пользователь запрашивает оптимизацию промптов, разработку шаблонов промптов, оценку выходных данных LLM с помощью набора eval. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Старший инженер по промпту { #senior-prompt-engineer }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `senior-prompt-engineer`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/senior-prompt-engineer/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Разработка промптов на основе Eval, измерение качества RAG и проверка воркфлоу агента. Все здесь ** не зависит от модели по замыслу **: методы основаны на том, что они делают, а не на том, в каком поколении моделей они наблюдались, и инструменты никогда не содержат жесткого кода идентификаторов моделей или ценообразования - вы указываете текущие тарифы вашего провайдера, когда хотите получить данные в долларах.

## Правила эксплуатации { #operating-rules }

1. **Никогда не меняйте промпт без базовой линии.** Сначала фиксируйте показатели (`--analyze --output baseline.json`), затем сравните с ним каждую итерацию.
2. ** Оценка устанавливается перед оптимизацией.** 10-20 репрезентативных случаев с минимальными ожидаемыми результатами. Если у пользователя нет набора eval, создайте его с их помощью, прежде чем нажимать на промпту — оптимизация с учетом вибраций - это режим сбоя № 1.
3. ** Отдавайте предпочтение функциям платформы, а не промпт-взломам.** Если поставщик предлагает собственные структурированные выходные данные / применение схемы JSON, API-интерфейсы с использованием инструментов или кэширование промптов, используйте их вместо заклинаний "отвечать ТОЛЬКО с помощью JSON". Принудительное использование формата на уровне промптов - это запасной вариант, а не значение по умолчанию.
4. **Модели текущего поколения нуждаются в меньшем количестве строительных лесов.** Не добавляйте шаблонные цепочки рассуждений, ролевые рамки или примеры из нескольких кадров рефлексивно - модели frontier часто работают хуже с избыточными каркасами. Добавляйте каждый элемент только тогда, когда набор eval показывает, что это помогает.
5. ** Цифры затрат всегда указываются пользователем.** Ознакомьтесь с текущими ценами провайдера на Mtok и передайте их через `--price-per-mtok` (никогда не доверяйте кэшированной таблице цен — включая те, которые вы помните).

## Инструменты (точный CLI, весь stdlib) { #tools-exact-clis-all-stdlib }

### 1. Оптимизатор промптов — `scripts/prompt_optimizer.py` { #1-prompt-optimizer--scriptsprompt_optimizerpy }

Статический анализ: оценка токена, ясность/structure оценки (0-100), обнаружение неоднозначности + избыточности, извлечение примеров с несколькими кадрами.

```bash
# Full analysis (human-readable report)
python3 scripts/prompt_optimizer.py prompt.txt --analyze

# Save machine-readable baseline for later comparison
python3 scripts/prompt_optimizer.py prompt.txt --analyze --json --output baseline.json

# Token estimate; cost only if you supply your provider's current rate
python3 scripts/prompt_optimizer.py prompt.txt --tokens --model claude --price-per-mtok 3.00

# Whitespace/redundancy-trimmed version
python3 scripts/prompt_optimizer.py prompt.txt --optimize --output optimized.txt

# Extract Input/Output few-shot pairs to JSON
python3 scripts/prompt_optimizer.py prompt.txt --extract-examples --output examples.json

# Compare a revision against the saved baseline
python3 scripts/prompt_optimizer.py optimized.txt --analyze --compare baseline.json
```

`--model` принимает любую строку; выводится только семейство токенизаторов (имена, содержащие "claude" → 3,5 символа/token, в противном случае 4.0). Завершите работу с 0 в случае успеха, с 1 в случае отсутствия файла.

### 2. Оценщик RAG — `scripts/rag_evaluator.py` { #2-rag-evaluator--scriptsrag_evaluatorpy }

Измеряет качество извлечения и заземления из двух файлов JSON (форматы, напечатанные в `--help`).

```bash
python3 scripts/rag_evaluator.py --contexts retrieved.json --questions eval_set.json
python3 scripts/rag_evaluator.py --contexts ctx.json --questions q.json --k 10 --json
python3 scripts/rag_evaluator.py --contexts ctx.json --questions q.json --output report.json --verbose
python3 scripts/rag_evaluator.py --contexts ctx.json --questions q.json --compare baseline_report.json
```

Сообщает о релевантности контексту, точности @k, охвате, верности ответов, обоснованности. Рассматривайте релевантность < 0,80 как проблему поиска (разбиение на фрагменты/embedding/filtering), а не проблема с промптом — исправьте поиск перед перезаписью промпта генерации.

### 3. Агент- оркестратор — `scripts/agent_orchestrator.py` { #3-agent-orchestrator--scriptsagent_orchestratorpy }

Проверяет конфигурации агента (YAML/JSON): подключение инструмента, отсутствие требуемой конфигурации, риск цикла, оценки токенов.

```bash
python3 scripts/agent_orchestrator.py agent.yaml --validate
python3 scripts/agent_orchestrator.py agent.yaml --visualize --format mermaid
python3 scripts/agent_orchestrator.py agent.yaml --estimate-cost --runs 100 \
    --input-price-per-mtok 3.00 --output-price-per-mtok 15.00
```

Без двух ценовых флажков, `--estimate-cost` сообщает только об оценках токенов. Тот `model:` поле в конфигурации является информационным — принимается любое название модели.

## Воркфлоу { #workflows }

### Оптимизация промпта (оцененный гейт) { #prompt-optimization-eval-gated }

1. **Исходный уровень:** `python3 scripts/prompt_optimizer.py current_prompt.txt --analyze --json --output baseline.json`
2. ** Диагностика** из отчета: неоднозначные глаголы ("анализировать", "обрабатывать"), избыточные блоки, отсутствующий выходной контракт, пустая трата токенов.
3. **Применяйте по одному изменению за раз**, в таком порядке использования кредитного плеча:
   | Симптом | Исправить |
   |---------|-----|
   | Деформированный/unparseable выход | Собственные структурированные выходные данные / схема JSON, если API поддерживает это; явная схема в промпте в противном случае |
   | Противоречивые ответы в разных прогонах | Ужесточите инструкции + добавьте 2-3 контрастных примера (один из них почти точно показывает, чего не следует делать) |
   | Пропускает крайние случаи | Явно перечислите крайние случаи; добавьте правило "когда не уверен, делай X". |
   | Раздувание токена при повторных вызовах | Сначала переместите префикс stable (системные правила, примеры), чтобы применялось кэширование промптов; сократите избыточность |
   | Неправильные рассуждения о сложных случаях | Запросите пошаговое обоснование * в пустом поле, которое потребитель игнорирует*, или воспользуйтесь расширенным режимом мышления поставщика |
4. **Повторный анализ и сравнение:** `python3 scripts/prompt_optimizer.py revised.txt --analyze --compare baseline.json`
5. **Гейт Eval (должен быть пройден перед отправкой):** запустите пересмотренный промпт поверх набора eval, запишите проход для каждого случая/fail к `eval_results.json`, затем утверждайте:
   ```bash
   python3 scripts/prompt_optimizer.py revised.txt --analyze --json --output revised.json \
     && python3 -c "
   import json, sys
   r = json.load(open('revised.json')); b = json.load(open('baseline.json'))
   ok = r['clarity_score'] >= b['clarity_score'] and r['token_count'] <= b['token_count'] * 1.10
   sys.exit(0 if ok else 1)"
   echo "gate exit=$?"   # 0 = ship; 1 = regression, iterate again
   ```
   Соедините этот структурный гейт с оценкой на уровне вашей задачи: в ревизии не должно быть потеряно ни одного ранее пройденного случая оценки (правило отсутствия регрессии).

### Пример дизайна с несколькими кадрами { #few-shot-example-design }

1. Сначала определите контракт задачи (форма ввода, форма вывода, политика граничного регистра).
2. Начните с ** нулевых примеров ** и измерьте — современные модели часто не нуждаются в них. Добавляйте примеры только для кластеров сбоев, выявленных при оценке.
3. При добавлении: максимум 3-5, упорядочено просто → ребро → минус (что НЕ извлекать), отформатировано идентично реальному контракту вывода.
4. Проверка согласованности: `python3 scripts/prompt_optimizer.py prompt_with_examples.txt --extract-examples --output examples.json` и убедитесь, что каждая извлеченная пара анализируется в соответствии с вашей схемой.
5. Повторно запустите набор eval; если случай проходит только потому, что он похож на пример, добавьте отложенный вариант в набор eval.

### Структурированный дизайн выходных данных { #structured-output-design }

1. Сначала напишите схему JSON (типы, перечисления, required, maxLength).
2. ** Предпочитайте собственное применение API**: структурированные выходные данные / схема ответа / параметры вызова инструмента гарантируют форму; текст промпта не может.
3. Запасной вариант (API без поддержки схемы): включите схему, отображаемую в виде правил для каждого поля + один допустимый пример, и укажите "выводить только объект JSON".
4. Гейт: передача 10 выходных данных eval через средство проверки схемы (`python3 -c "import json,sys; [json.loads(l) for l in sys.stdin]"` как минимум); необходимо выполнить синтаксический анализ 10/10, в противном случае вернитесь к шагу 2.

### Цикл настройки тряпки { #rag-tuning-loop }

1. Строить `questions.json` (идентификатор, вопрос, справочный ответ) и фиксировать текущие результаты поиска в `contexts.json`.
2. `python3 scripts/rag_evaluator.py --contexts contexts.json --questions questions.json --output rag_baseline.json`
3. Сначала исправьте ** самый низкий показатель **: релевантность → разбиение на части/embeddings/metadata фильтры; верность → инструкции по обоснованию + "отвечать только из контекста" + требование цитирования; охват → расширение поиска k / запроса.
4. Гейт: `python3 scripts/rag_evaluator.py --contexts new_contexts.json --questions questions.json --compare rag_baseline.json` — каждая метрика должна быть ≥ базовой; любая регрессия блокирует изменение.

### Ревью конфигурации агента { #agent-config-review }

1. `python3 scripts/agent_orchestrator.py agent.yaml --validate` — должен завершиться с пройденной проверкой; исправьте все ошибки и предупреждения (отсутствующая конфигурация инструмента, неограниченные итерации, риск цикла).
2. Проверьте контекстную дисциплину: описание каждого инструмента не более 1-2 предложений, минимальное количество инструментов для задания, стабильная системная промпта размещена первой (удобна для кэширования), ограничение итерации + присутствует условие раннего выхода.
3. Бюджет: `--estimate-cost --runs N` с вашими текущими ценами; если стоимость/run превышает бюджет, сокращает инструменты или контекст, прежде чем понизить рейтинг модели.

## Ссылки { #references }

| Файл | Содержит | Загружается, когда пользователь спрашивает о |
|------|----------|---------------------------|
| `references/prompt_engineering_patterns.md` | 10 шаблонов промптов с вводом/output примеры | "какой шаблон?", дизайн с несколькими кадрами, декомпозиция, мета-промпт |
| `references/llm_evaluation_frameworks.md` | Оценочные показатели, методы подсчета очков, A/B тестирование | "как оценить?", "измерить качество", "сравнить промпты" |
| `references/agentic_system_design.md` | Архитектуры агентов (реагирование, планирование-выполнение, использование инструментов) | "создать агента", "вызов инструмента", "мультиагентныйагент" |

## Связанные скиллы { #related-skills }

- `engineering-team/skills/senior-ml-engineer` — развертывание модели и обслуживание (этот скилл прекращается при промпт/eval слой)
- `engineering/rag-architect` — Архитектура системы RAG (этот скилл измеряет качество RAG; он проектирует пайплайн)
- `engineering/agent-designer` — полное проектирование системы агента (этот скилл проверяет конфигурации; этот разрабатывает архитектуру)
