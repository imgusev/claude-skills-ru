---
title: "ТРЯПИЧНЫЙ архитектор { #rag-architect } — Агентский скилл для Codex и OpenClaw"
description: "Используйте, когда пользователь просит спроектировать пайплайн RAG, выбрать стратегию фрагментации или модель встраивания, выбрать векторную базу. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# ТРЯПИЧНЫЙ архитектор { #rag-architect }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `rag-architect`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/rag-architect/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Проектируйте, настраивайте и оценивайте производственные пайплайны RAG с помощью трех детерминированных инструментов. Запускайте инструменты в соответствии с фактическим корпусом и требованиями — не выбирайте размеры блоков или базы данных интуитивно.

## Жесткие правила { #hard-rules }

1. **Никогда не указывайте названия моделей или цены поставщиков в качестве текущих фактов.** Встраиваемые модели и ценообразование в векторных базах данных меняются в течение нескольких месяцев. Порекомендуйте * уровень* (см. таблицу ниже), назовите кандидата текущего поколения и попросите пользователя свериться со страницей актуальных цен поставщика.
2. **Каждый проект заканчивается оценочным прогоном.** ТРЯПИЧНЫЙ дизайн без `retrieval_evaluator.py` цифры - это гипотеза, а не конечный результат.
3. ** Разбиение на фрагменты осуществляется на основе корпуса.** Запуск `chunking_optimizer.py` ознакомьтесь с реальными документами, прежде чем выбирать стратегию.

## Встраивание уровней модели (шаблон, а не прайс-лист) { #embedding-model-tiers-pattern-not-price-list }

| Уровень | Примеры текущего поколения (проверьте перед использованием) | Когда |
|---|---|---|
| Быстрый / автономный хостинг | `all-MiniLM-L6-v2`, `bge-small` | Экономичный, маломасштабный, в режиме реального времени |
| Сбалансированный открытый | `all-mpnet-base-v2`, `bge-large`, `e5-large` | Качество без зависимости от API |
| Качественный API | `text-embedding-3-large`, `voyage-3-large` | Общий поиск с приоритетом точности |
| Код | `voyage-code-3`, Кодовое семейство | Корпуса поиска по коду |

**Ценовая дисциплина:** постройте модель затрат с помощью таблицы—заполнителя - столбцов `model | $/1M tokens (verify) | dims | as-of date` — и попросите пользователя ввести реальные цифры. То же самое для векторных баз данных (Pinecone/Weaviate/Qdrant/Chroma/pgvector): критерии выбора (управляемые или размещаемые самостоятельно, масштабирование, фильтрация, существующие Postgres) являются надежными; цифры в долларах - нет.

## Воркфлоу { #workflow }

Все пути относительно этой папки с скиллами. Цепочка выходных данных: анализ корпуса → проектирование → оценка.

### 1. Проанализируйте корпус и выделите фрагменты { #1-analyze-the-corpus-and-pick-chunking }

```bash
python3 chunking_optimizer.py /path/to/docs --extensions .md .txt -o chunking.json
```

Испускает `chunking.json` с `corpus_info`, в соответствии со стратегией `strategy_results`, а `recommendation`, и `sample_chunks`. Используйте `recommendation.strategy` и его конфигурацию; показать пользователю 2-3 `sample_chunks` чтобы они могли проверять границы разумного.

### 2. Спроектируйте пайплайн в соответствии с требованиями { #2-design-the-pipeline-from-requirements }

Напишите JSON-файл требований с этими ключами (все необходимые): `document_types[]`, `document_count`, `avg_document_size` (символы), `queries_per_day`, `query_patterns[]`, `latency_requirement`, `budget_monthly`, `accuracy_priority` (0-1), `cost_priority` (0-1), `maintenance_complexity`.

```bash
python3 rag_pipeline_designer.py requirements.json -o design.json
```

Испускает `design.json` с `chunking`, `embedding`, `vector_db`, `retrieval`, `reranking`, `evaluation`, `total_cost`, `architecture_diagram` (русалка), и `config_templates`. Представьте схему; обозначьте каждый `cost_monthly` приведите цифру в качестве оценки для проверки (правило 1).

### 3. Оцените качество поиска { #3-evaluate-retrieval-quality }

Подготовить `queries.json` (список `{id, text}` или `{"queries": [...]}`) и `ground_truth.json` (`{query_id: [relevant_doc_ids]}`), затем:

```bash
python3 retrieval_evaluator.py queries.json /path/to/docs ground_truth.json --k-values 3 5 10 -o eval.json
```

Сообщает точность@k, отзыв@k, MRR, NDCG@k, плюс `poor_precision_examples` / `poor_recall_examples` для анализа отказов.

### 4. цикл проверки { #4-verification-loop }

Дизайн выполняется только тогда, когда:

1. `eval.json` соответствует целевым показателям — типичные значения: точность при 5 ≥ 0,8, отзыв при 10 ≥ 0,85 (устанавливается пользователем в зависимости от варианта использования).
2. Если цель ниже: проверьте списки с плохими примерами, затем измените ** одну** переменную (стратегия фрагментации → повторно запустите шаг 1; уровень внедрения; добавьте повторный ранжирование; гибридный поиск) и повторно запустите шаг 3. Повторите.
3. К каждой рекомендуемой модели /цене в поставляемом продукте прилагается примечание "проверьте текущую цену/доступность модели" с указанием текущей даты.

## Ссылки { #references }

- `references/chunking_strategies_comparison.md` — стратегические компромиссы, реализуемые оптимизатором
- `references/embedding_model_benchmark.md` — бенчмарк * методология* (датированный снимок; предупреждение о застарелости вверху)
- `references/rag_evaluation_framework.md` — определения показателей (достоверность, релевантность, точность/отзыв/NDCG)
