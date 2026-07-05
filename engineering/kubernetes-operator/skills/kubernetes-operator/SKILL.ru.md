---
name: kubernetes-operator
description: "Используйте при создании оператора Kubernetes — пользовательские контроллеры, которые согласовывают состояние CRD. Триггеры для \"построения оператора\", \"проектирования CRD\", \"согласования цикла\", \"контроллер-среда выполнения\", \"kubebuilder\", \"оператор-sdk\", \"метаконтроллер\", \"KOPF\", \"уровни возможностей оператора\" или \"пользовательский ресурс\". Поставляется CRD validator, компоновщик цикла согласования и аудитор возможностей OperatorHub (все на stdlib Python), 4 ссылки на шаблон оператора + дизайн CRD + шаблоны согласования + набор инструментов и слэш-команда /operator-аудит. ЭТО не общий скилл k8s — в частности, шаблон оператора."
context: fork
version: 2.9.0
author: claude-code-skills
license: MIT
tags: [kubernetes, operator, crd, controller-runtime, kubebuilder, operator-sdk, metacontroller, kopf, reconcile, devops]
compatible_tools: [claude-code, codex-cli, cursor, antigravity, opencode, gemini-cli]
---

# Оператор Kubernetes { #kubernetes-operator }

Создавайте операторы, которые корректно согласовываются. Большинство ошибок операторов не являются ошибками Kubernetes — это ошибки цикла согласования: отсутствующие финализаторы, блокирующие вызовы, отсутствие запроса на временные ошибки, дрейф статуса, превышение разрешений RBAC. Этот скилл детерминированно ловит их до того, как они достигнут скопления.

## Когда использовать { #when-to-use }

- Создание нового оператора Kubernetes (контроллера для CRD)
- Ревью существующего оператора на предмет пробелов в уровне возможностей
- Аудит спецификации CRD на предмет корректности статуса/условий/финализатора
- Выбор фреймворка (контроллер-среда выполнения / kubebuilder / оператор-sdk / metacontroller / KOPF)
- Проектирование интерфейса API пользовательского ресурса
- Ужесточение RBAC, избрание лидера или проверка webhook

## Когда не следует использовать { #when-not-to-use }

- Простая упаковка рулевой карты → использование `helm-chart-builder`
- Стандартные операции с kubectl / сине-зеленые деплою → использовать `senior-devops`
- Общая позиция безопасности k8s → использование `cloud-security`
- "Я хочу запустить рабочую нагрузку" — это развертывание / задание, а не оператор

## Основной принцип: оператор - это цикл согласования, а не сценарий { #core-principle-an-operator-is-a-reconcile-loop-not-a-script }

```
observe(actual) → desired = read(spec) → diff(actual, desired) → act → update(status)
                                                                          ↓
                                                                   requeue / done
```

Операторы, которые терпят неудачу, - это те, которые:
1. Рассматривайте согласование как императивное (сделайте это, затем это, затем вот это) вместо декларативного (сделайте фактическим =желаемым, идемпотентно).
2. Не запрашивайте временные сбои
3. Не используйте финализаторы, оставляя бесхозные ресурсы
4. Изменить спецификацию вместо статуса
5. Не используйте подресурс status (спецификация триггера обновления статуса согласовывает → цикл)
6. Блокировка при согласовании (длинные HTTP-вызовы, блокировки)
7. Забудьте о выборах лидера → раздвоение мозга при деплою с несколькими репликами

Приведенные ниже 3 инструмента улавливают каждый из них.

## Быстрый старт { #quick-start }

```bash
SKILL=engineering/kubernetes-operator/skills/kubernetes-operator

# Validate a CRD design
python "$SKILL/scripts/crd_validator.py" --crd config/crd/myapp.yaml

# Lint a Go reconcile function
python "$SKILL/scripts/reconcile_lint.py" --controller controllers/myapp_controller.go

# Score against OperatorHub Capability Levels (1-5)
python "$SKILL/scripts/operator_capability_audit.py" --operator-dir .
```

## 3 инструмента Python { #the-3-python-tools }

Все только для stdlib. Бегать с `--help`.

### `crd_validator.py` { #crd_validatorpy }

Проверяет CRD YAML на соответствие рекомендациям по шаблону оператора.

```bash
python scripts/crd_validator.py --crd config/crd/myapp.yaml
python scripts/crd_validator.py --crd config/crd/ --format json
```

**Проверки:**
- `spec.versions[*].subresources.status` установлен (подресурс статуса)
- `spec.scope` является `Namespaced` (не `Cluster`) , если это явно не обосновано
- Определены сингулярные и списковые типы
- `spec.versions[*].schema.openAPIV3Schema` имеет определения типов (нет `x-kubernetes-preserve-unknown-fields: true` на высшем уровне)
- Версия помечена `served: true` И `storage: true`
- Массив условий находится в схеме (позволяет `metav1.Conditions`)
- Столбцы принтера включают в себя `Age` и `Status`/`Phase`

### `reconcile_lint.py` { #reconcile_lintpy }

Поддерживает функцию согласования контроллера Go для защиты от шаблонов.

```bash
python scripts/reconcile_lint.py --controller controllers/myapp_controller.go
```

**Проверки (эвристика на основе регулярных выражений):**
- Возвраты являются `(ctrl.Result, error)` форма
- Ошибки триггер ненулевого запроса (`return ctrl.Result{Requeue: true}, err`)
- `client.Update()` в спецификации объект помечен (контроллеры должны обновлять только статус)
- `time.Sleep` внутренняя выверка помечена (используйте `RequeueAfter`)
- HTTP-вызовы без отмены контекста помечаются
- Пропавший без вести `defer` после добавления финализатора
- Нет `IsConditionTrue` / `SetCondition` вызывает, когда в CRD присутствуют условия
- Функция согласования превышает 80 строк (извлечение подпрограмм)

### `operator_capability_audit.py` { #operator_capability_auditpy }

Оценивает оператора по 5 уровням возможностей OperatorHub.

```bash
python scripts/operator_capability_audit.py --operator-dir .
```

**Уровни:**
- **L1 — Базовая установка: ** CRD определен, контроллер депло его
- **L2 — Плавные обновления: ** PDBS, веб-хуки для преобразования, стратегия перекоса версий
- **L3 — Полный жизненный цикл:** резервное копирование, восстановление, восстановление после сбоев
- **L4 — Глубокая аналитика: ** конечная точка метрик, правила Prometheus, оповещения
- **L5 — Автопилот:** автоматическое масштабирование, автонастройка, обнаружение аномалий

Сообщает о текущем уровне + конкретных следующих шагах для продвижения на один уровень.

## Ландшафт оснастки { #tooling-landscape }

Выберите фреймворк, основанный на языке и сложности. Видишь `references/tooling_landscape.md`.

| Фреймворк | Язык | Лучше всего подходит для | Техническое обслуживание |
|---|---|---|---|
| **контроллер-среда выполнения** | Иди | Производственный контроль низкого уровня | Активный (sig-api-оборудование) |
| **конструктор кубов** | Иди | Стандартные строительные леса, самоуверенные | Активный (сиги Kubernetes) |
| **оператор-sdk** | Перейти / Управлять / Ансибл | Команды OpenShift / смешанной парадигмы | Активный (Красная шляпа) |
| **метаконтроллер** | Любой (на основе webhook) | Команды полиглотов, избегающие идти | Менее активный |
| **КОПФ** | Питон | Магазины Python, сначала асинхронные | Активный (сообщество) |
| **java-оператор-sdk** | Java | Магазины JVM | Активный (Red Hat / Java SIG) |

Правила принятия решений:
- Новый оператор + Перейти в магазин → kubebuilder
- Новый оператор + магазин Python → KOPF
- Новый оператор + не удается выбрать язык → метаконтроллер
- Цель OpenShift → оператор-sdk

## Принципы проектирования CRD { #crd-design-principles }

Видишь `references/crd_design.md` для получения полной информации. Краткие правила:

1. ** статус - это источник истины для представления контроллера о мире.** Спецификация - это то, что хочет пользователь; статус - это то, что наблюдал контроллер.
2. **Используйте подресурс status.** Без этого обновления статуса повторно запускают триггер согласования (цикл).
3. **Условия использования.** `Ready`, `Reconciling`, `Degraded` Каждый из них несет в себе причину и послание.
4. ** Добавьте финализаторы.** Без финализаторов удаление приводит к перегрузке контроллера и потере внешних ресурсов.
5. ** Обновите свой CRD с 1-го дня.** `v1alpha1` → `v1beta1` → `v1`. Спланируйте веб-крючок для конверсии.
6. ** Проверка с помощью схемы OpenAPI v3.** Не полагайтесь на контроллер для проверки, которая должна завершиться неудачей при входе.
7. **Использование `additionalPrinterColumns` для `kubectl get`.** Показать `Age`, `Phase`, `Ready` как минимум.
8. **Разместите свои CRD в пространстве имен, если только они не управляют ресурсами кластера.**

## Согласовать принципы цикла { #reconcile-loop-principles }

Видишь `references/reconcile_loop.md` для получения полной информации. Краткие правила:

1. ** Идемпотентно.** Согласование одного и того же состояния дважды → тот же результат, ноль побочных эффектов.
2. ** Прочитайте один раз, решите, действуйте.** Не наблюдайте за миром повторно во время примирения.
3. ** Статус обновления, а не спецификация.** Спецификация принадлежит пользователю.
4. **Возвращает ошибки, которые запрашиваются.** Используйте `ctrl.Result{RequeueAfter: ...}` для известных переходных случаев.
5. ** Никогда не блокируйте.** Нет `time.Sleep`. Никаких длинных HTTP-вызовов без контекста.
6. **Используйте кэш.** Считывайте через кэшированный клиент контроллера; выходите из кэша только по определенной причине.
7. **Выбор лидера при запуске >1 реплики.** В противном случае включите режим с одной репликой.
8. **Установите ссылки на владельца.** Каскадное удаление - это бесплатный подарок шаблона оператора.

## Воркфлоу { #workflows }

### Воркфлоу 1: Загрузите новый оператор (Go + kubebuilder) { #workflow-1-bootstrap-a-new-operator-go--kubebuilder }

```
1. Pick a Group/Version/Kind: e.g., apps.example.com/v1alpha1, kind=MyApp
2. kubebuilder init --domain example.com --repo github.com/org/myapp-operator
3. kubebuilder create api --group apps --version v1alpha1 --kind MyApp
4. Run crd_validator.py on config/crd/bases/apps.example.com_myapps.yaml
   → Fix every WARN before writing controller code
5. Implement the reconcile function (Karpathy principle 2: simplest correct version first)
6. Run reconcile_lint.py on controllers/myapp_controller.go
7. Run operator_capability_audit.py --operator-dir . — confirm L1
8. Test in a kind cluster: kubectl apply -f config/samples/
9. Add status conditions; aim for L2 in the same PR
```

### Воркфлоу 2: Аудит существующего оператора { #workflow-2-audit-an-existing-operator }

```
1. Run operator_capability_audit.py --operator-dir <path>
2. Run crd_validator.py --crd config/crd/
3. Run reconcile_lint.py --controller controllers/
4. Triage findings:
   - FAIL → block release; fix before next deploy
   - WARN → file an issue; fix in next 30 days
5. Document current capability level in README; commit
6. Plan one capability level advancement per quarter
```

### Воркфлоу 3: Выберите фреймворк { #workflow-3-choose-a-framework }

```
1. Identify primary language constraint (team skill)
2. Identify deployment target (vanilla k8s vs OpenShift)
3. Identify operator complexity (single CRD vs multi-CRD vs cluster-wide)
4. Cross-reference with references/tooling_landscape.md
5. Build a 1-week proof-of-concept before committing
```

## Ссылки { #references }

- `references/operator_pattern.md` — что такое оператор, когда использовать против альтернатив
- `references/crd_design.md` — Принципы проектирования CRD, управление версиями, веб-хуки для преобразования
- `references/reconcile_loop.md` — согласование шаблонов, обработка ошибок, идемпотентность
- `references/tooling_landscape.md` — сравнение фреймворка + дерево решений

## Слэш-команда { #slash-command }

`/operator-audit` — Запустите все 3 инструмента в репозитории оператора и создайте отчет Markdown.

## Шаблоны активов { #asset-templates }

- `assets/crd_template.yaml` — CRD с подресурсом статуса, условиями, подсказкой финализатора, столбцами принтера
- `assets/reconcile_skeleton.go` — Контроллер Go согласовывает функцию с идемпотентностью, условиями, финализаторами, шаблонами запросов

## Анти-паттерны { #anti-patterns }

- **`time.Sleep(30 * time.Second)` внутри выверки** — блокирует другие выверки. Использование `RequeueAfter`.
- **`r.Client.Update(ctx, obj)` чтобы установить статус** — используйте `r.Status().Update(ctx, obj)` вместо этого.
- ** Нет выборов лидера + 2+ реплики ** — раздвоение мозга.
- **Нет финализатора** — внешние ресурсы остаются бесхозными при удалении.
- **CRD без подресурса статуса** — обновления статуса триггера согласовывают спецификации (бесконечный цикл).
- **Функция согласования > 200 строк** — извлекает подпрограммы reconcileXxx для каждого условия.
- **`x-kubernetes-preserve-unknown-fields: true` в корне спецификации** — отменяет проверку.
- **Обязательное согласование** — "при создании выполните A; при обновлении выполните B; при удалении выполните C". Неправильная форма. Согласовать = сделать актуальным = желаемым, независимо от того, как мы сюда попали.

## Поддающийся проверке успех { #verifiable-success }

Команда, использующая этот скилл, должна достичь:

- 100% новых сертификатов проходят проверку `crd_validator.py` перед слиянием
- Все функции согласования выполняются `reconcile_lint.py` строгий режим
- Операторы достигают уровня возможностей OperatorHub 3 (полный жизненный цикл) до публичного выпуска
- Среднее время исправления ошибки согласования: <1 дня (в производстве нет бесконечных циклов)
