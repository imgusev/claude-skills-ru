---
name: "helm-chart-builder"
description: "Агент по скиллу разработки Helm chart и плагин для Claude Code, Codex, Gemini CLI, Cursor, OpenClaw — построение диаграмм, проектирование значений, шаблоны шаблонов, управление зависимостями, усиление безопасности и тестирование диаграмм. Используйте, когда: пользователь хочет создать или улучшить рулевые диаграммы, проектные значения.файлы yaml, реализуйте помощники по шаблонам, аудит безопасности диаграмм (RBAC, сетевые политики, безопасность модуля), управляйте вложенными диаграммами или запускайте helm lint/test."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  updated: 2026-03-15
---

# Построение рулевой диаграммы { #helm-chart-builder }

> Штурвальные карты производственного класса. Разумные значения по умолчанию. Безопасный по своей конструкции. Никакой перегрузки груза.

Самоуверенный воркфлоу Helm, который превращает специальные манифесты Kubernetes в поддерживаемые, тестируемые и повторно используемые диаграммы. Охватывает структуру диаграммы, дизайн значений, шаблоны шаблонов, управление зависимостями и усиление безопасности.

Не руководство по управлению — набор конкретных решений о том, как строить диаграммы, которым доверяют операторы, а разработчики не сопротивляются.

---

## Слэш-команды { #slash-commands }

| Команда | Что он делает |
|---------|-------------|
| `/helm:create` | Создайте готовую к производству схему управления с использованием наилучшей структуры |
| `/helm:review` | Проанализируйте существующую диаграмму на наличие проблем — отсутствующих меток, жестко закодированных значений, анти-шаблонов шаблонов |
| `/helm:security` | Таблица аудита проблем безопасности — RBAC, сетевые политики, безопасность модуля, обработка секретов |

---

## Когда активируется этот Скилл { #when-this-skill-activates }

Распознать эти шаблоны у пользователя:

- "Создайте диаграмму управления для этого сервиса"
- "Ревью мою рулевую карту"
- "Эта карта защищена?"
- "Создайте values.yaml"
- "Добавить зависимость от вложенной диаграммы"
- "Настройка тестов руля"
- "Руководите лучшими практиками для [тип рабочей нагрузки]"
- Любой запрос, включающий: Helm chart, values.yaml, Chart.yaml, шаблоны, помощники, _helpers.tpl, вложенные диаграммы, helm lint, helm test

Если у пользователя есть диаграмма Helm или он хочет упаковать ресурсы Kubernetes → применяется этот скилл.

---

## Воркфлоу { #workflow }

### `/helm:create` — Строительные леса для построения диаграмм { #helmcreate--chart-scaffolding }

1. **Определить тип рабочей нагрузки**
   - Веб-сервис (развертывание + Сервис + Вход)
   - Рабочий (развертывание, без обслуживания)
   - CronJob (CronJob + учетная запись службы)
   - Служба с сохранением состояния (StatefulSet + PVC + безголовый сервис)
   - Библиотечная диаграмма (без шаблонов, только помощники)

2. **Структура диаграммы строительных лесов**

   ```
   mychart/
   ├── Chart.yaml              # Chart metadata and dependencies
   ├── values.yaml             # Default configuration
   ├── values.schema.json      # Optional: JSON Schema for values validation
   ├── .helmignore             # Files to exclude from packaging
   ├── templates/
   │   ├── _helpers.tpl        # Named templates and helper functions
   │   ├── deployment.yaml     # Workload resource
   │   ├── service.yaml        # Service exposure
   │   ├── ingress.yaml        # Ingress (if applicable)
   │   ├── serviceaccount.yaml # ServiceAccount
   │   ├── hpa.yaml            # HorizontalPodAutoscaler
   │   ├── pdb.yaml            # PodDisruptionBudget
   │   ├── networkpolicy.yaml  # NetworkPolicy
   │   ├── configmap.yaml      # ConfigMap (if needed)
   │   ├── secret.yaml         # Secret (if needed)
   │   ├── NOTES.txt           # Post-install usage instructions
   │   └── tests/
   │       └── test-connection.yaml
   └── charts/                 # Subcharts (dependencies)
   ```

3. **Применить диаграмму.лучшие практики yaml**

   ```
   METADATA
   ├── apiVersion: v2 (Helm 3 only — never v1)
   ├── name: matches directory name exactly
   ├── version: semver (chart version, not app version)
   ├── appVersion: application version string
   ├── description: one-line summary of what the chart deploys
   └── type: application (or library for shared helpers)

   DEPENDENCIES
   ├── Pin dependency versions with ~X.Y.Z (patch-level float)
   ├── Use condition field to make subcharts optional
   ├── Use alias for multiple instances of same subchart
   └── Run helm dependency update after changes
   ```

4. **Генерировать значения.yaml с документацией**
   - Каждое значение имеет встроенный комментарий, объясняющий назначение и тип
   - Разумные значения по умолчанию, которые работают для разработки
   - Структура, удобная для переопределения (плоская, где это возможно, вложенная только тогда, когда она логична)
   - Нет жестко заданных значений, специфичных для кластера (реестр изображений, домен, класс хранилища)

5. **Проверка подлинности**
   ```bash
   python3 scripts/chart_analyzer.py mychart/
   helm lint mychart/
   helm template mychart/ --debug
   ```

### `/helm:review` — Анализ графиков { #helmreview--chart-analysis }

1. **Проверьте структуру диаграммы**

   | Проверьте | Суровость | Исправить |
   |-------|----------|-----|
   | Отсутствует _helpers.tpl | Высокий | Создайте помощники для общих меток и селекторов |
   | Нет NOTES.txt | Средний | Добавьте инструкции после установки |
   | Нет, хелмигнор | Низкий | Создайте его, чтобы исключить файлы .git, CI, тесты |
   | Отсутствующая диаграмма.поля ямл | Средний | Добавить описание, версию приложения, сопровождающих |
   | Жестко заданные значения в шаблонах | Высокий | Извлеките в значения.yaml со значениями по умолчанию |

2. **Проверьте качество шаблона**

   | Проверьте | Суровость | Исправить |
   |-------|----------|-----|
   | Отсутствующие стандартные этикетки | Высокий | Использование `app.kubernetes.io/*` ярлыки через _helpers.tpl |
   | Отсутствие запросов на ресурсы/ ограничений | Критический | Добавьте раздел ресурсов со значениями по умолчанию.ямл |
   | Жестко закодированный тег изображения | Высокий | Использование `{{ .Values.image.repository }}:{{ .Values.image.tag }}` |
   | Нет политики imagePullPolicy | Средний | По умолчанию используется значение `IfNotPresent`, переопределяемый |
   | Отсутствующие датчики жизнеспособности/готовности | Высокий | Добавьте зонды с настраиваемыми путями и портами |
   | Отсутствие антиаффинности к капсуле | Средний | Добавьте предпочтительное антиаффинное действие к HA |
   | Дублирующий код шаблона | Средний | Извлекать в именованные шаблоны в _helpers.tpl |

3. **Проверьте значения.качество yaml**
   ```bash
   python3 scripts/values_validator.py mychart/values.yaml
   ```

4. **Сгенерировать отчет о ревью**
   ```
   HELM CHART REVIEW — [chart name]
   Date: [timestamp]

   CRITICAL: [count]
   HIGH:     [count]
   MEDIUM:   [count]
   LOW:      [count]

   [Detailed findings with fix recommendations]
   ```

### `/helm:security` — Аудит безопасности { #helmsecurity--security-audit }

1. **Аудит безопасности модуля**

   | Проверьте | Серьезность | Исправить |
   |-------|----------|-----|
   | Нет SecurityContext | Критический | Добавьте runAsNonRoot, только для чтения Rootfilesystem |
   | Запуск от имени root | Критический | Набор `runAsNonRoot: true`, `runAsUser: 1000` |
   | Доступная для записи корневая файловая система | Высокий | Набор `readOnlyRootFilesystem: true` + emptyDir для tmp |
   | Все возможности сохранены | Высокий | Отбросьте ВСЕ, добавьте только определенные необходимые заглавные буквы |
   | Привилегированный контейнер | Критический | Набор `privileged: false`, использовать определенные возможности |
   | Нет профиля seccomp | Средний | Набор `seccompProfile.type: RuntimeDefault` |
   | Разрешить масштабирование привилегий true | Высокий | Набор `allowPrivilegeEscalation: false` |

2. **Аудит RBAC**

   | Проверьте | Серьезность | Исправить |
   |-------|----------|-----|
   | Нет учетной записи ServiceAccount | Средний | Создайте выделенный SA, не используйте по умолчанию |
   | automountServiceAccountToken значение true | Средний | Установите значение false, если только pod не нуждается в доступе к API K8s |
   | ClusterRole вместо роли | Средний | Используйте роль, ограниченную пространством имен, если только это не требуется для всего кластера |
   | Разрешения с подстановочными знаками | Критический | Используйте конкретные названия ресурсов и глаголы |
   | Вообще никакого RBAC | Низкий | Приемлемо, если pod не нуждается в доступе к K8s API |

3. **Аудит сети и секретов**

   | Проверьте | Серьезность | Исправить |
   |-------|----------|-----|
   | Нет сетевой политики | Средний | Добавить правила по умолчанию-запрещать вход + явно разрешать |
   | Секреты в ценностях.ямл | Критический | Используйте внешние секреты оператора или закрытые секреты |
   | Нет бюджета на субсидирование | Средний | Добавьте PDB с minAvailable для рабочих нагрузок HA |
   | Хост-сеть: верно | Высокий | Удалять без крайней необходимости (например, плагин CNI) |
   | Идентификатор хоста или hostIPC | Критический | Никогда не используйте в графиках приложений |

4. **Создание отчета о безопасности**
   ```
   SECURITY AUDIT — [chart name]
   Date: [timestamp]

   CRITICAL: [count]
   HIGH:     [count]
   MEDIUM:   [count]
   LOW:      [count]

   [Detailed findings with remediation steps]
   ```

---

## Оснастка { #tooling }

### `scripts/chart_analyzer.py` { #scriptschart_analyzerpy }

Утилита CLI для статического анализа каталогов рулевых диаграмм.

**Особенности:**
- Проверка структуры диаграммы (необходимые файлы, расположение каталогов)
- Обнаружение анти-шаблона по шаблону (жестко закодированные значения, отсутствующие метки, отсутствие ограничений по ресурсам)
- Диаграмма.проверка метаданных yaml
- Проверка стандартных этикеток (app.kubernetes.io /*)
- Базовые проверки безопасности
- Вывод JSON и текста

**Использование:**
```bash
# Analyze a chart directory
python3 scripts/chart_analyzer.py mychart/

# JSON output
python3 scripts/chart_analyzer.py mychart/ --output json

# Security-focused analysis
python3 scripts/chart_analyzer.py mychart/ --security
```

### `scripts/values_validator.py` { #scriptsvalues_validatorpy }

Утилита CLI для проверки значений.yaml противоречит лучшим практикам.

**Особенности:**
- Охват документации (встроенные комментарии)
- Проверка согласованности типов
- Обнаружение жестко закодированных секретов
- Анализ качества значений по умолчанию
- Анализ глубины структуры
- Проверка соглашения об именовании
- Вывод JSON и текста

**Использование:**
```bash
# Validate values.yaml
python3 scripts/values_validator.py values.yaml

# JSON output
python3 scripts/values_validator.py values.yaml --output json

# Strict mode (fail on warnings)
python3 scripts/values_validator.py values.yaml --strict
```

---

## Шаблоны Шаблонов { #template-patterns }

### Шаблон 1: Стандартные метки (_helpers.tpl) { #pattern-1-standard-labels-_helperstpl }

```yaml
{{/*
Common labels for all resources.
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels (subset of common labels — must be immutable).
*/}}
{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### Схема 2: Условные ресурсы { #pattern-2-conditional-resources }

```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "mychart.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
```

### Образец 3: Спецификация модуля с усиленной защитой { #pattern-3-security-hardened-pod-spec }

```yaml
spec:
  serviceAccountName: {{ include "mychart.serviceAccountName" . }}
  automountServiceAccountToken: false
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: {{ .Chart.Name }}
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
      image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
      imagePullPolicy: {{ .Values.image.pullPolicy }}
      resources:
        {{- toYaml .Values.resources | nindent 8 }}
      volumeMounts:
        - name: tmp
          mountPath: /tmp
  volumes:
    - name: tmp
      emptyDir: {}
```

---

## Ценности и принципы проектирования { #values-design-principles }

```
STRUCTURE
├── Flat over nested (image.tag > container.spec.image.tag)
├── Group by resource (service.*, ingress.*, resources.*)
├── Use enabled: true/false for optional resources
├── Document every key with inline YAML comments
└── Provide sensible development defaults

NAMING
├── camelCase for keys (replicaCount, not replica_count)
├── Boolean keys: use adjectives (enabled, required) not verbs
├── Nested keys: max 3 levels deep
└── Match upstream conventions (image.repository, image.tag, image.pullPolicy)

ANTI-PATTERNS
├── Hardcoded cluster URLs or domains
├── Secrets as default values
├── Empty strings where null is correct
├── Deeply nested structures (>3 levels)
├── Undocumented values
└── values.yaml that doesn't work without overrides
```

---

## Управление зависимостями { #dependency-management }

```
SUBCHARTS
├── Use Chart.yaml dependencies (not requirements.yaml — Helm 3)
├── Pin versions: version: ~15.x.x (patch float)
├── Use condition: to make optional: condition: postgresql.enabled
├── Use alias: for multiple instances of same chart
├── Override subchart values under subchart name key in values.yaml
└── Run helm dependency update before packaging

LIBRARY CHARTS
├── type: library in Chart.yaml — no templates directory
├── Export named templates only — no rendered resources
├── Use for shared labels, annotations, security contexts
└── Version independently from application charts
```

---

## Проактивные триггеры { #proactive-triggers }

Отмечайте их, не спрашивая:

- **Нет _helpers.tpl** → Создайте его. Для каждой диаграммы нужны стандартные метки и помощники по полному имени.
- **Жестко закодированный тег изображения в шаблоне** → Извлечь в values.yaml. Теги должны быть переопределяемыми.
- **Нет запросов на ресурсы / ограничений ** → Добавьте их. Модули без ограничений могут привести к истощению узла.
- **Запуск от имени root** → Добавить SecurityContext. Никаких исключений для производственных графиков.
- **Нет NOTES.txt ** → Создайте его. Пользователям нужны инструкции после установки.
- **Секреты в ценностях.значения yaml по умолчанию** → Удалите их. Используйте заполнители с комментариями, объясняющими, как предоставлять секреты.
- **Нет пробников живучести/готовности ** → Добавьте их. Kubernetes должен знать, исправен ли модуль.
- **Отсутствует приложение.kubernetes.метки ввода-вывода** → Добавить через _helpers.tpl. Требуется для правильного отслеживания ресурсов.

---

## Установка { #installation }

### Однострочник (любой инструмент) { #one-liner-any-tool }
```bash
git clone https://github.com/imgusev/claude-skills-ru.git
cp -r claude-skills/engineering/helm-chart-builder ~/.claude/skills/
```

### Установка с несколькими инструментами { #multi-tool-install }
```bash
./scripts/convert.sh --skill helm-chart-builder --tool codex|gemini|cursor|windsurf|openclaw
```

### Открытый коготь { #openclaw }
```bash
clawhub install cs-helm-chart-builder
```

---

## Связанные скиллы { #related-skills }

- **старший-devops** — Более широкий охват DevOps (CI/CD, IaC, мониторинг). Дополняющий — используйте helm-chart-builder для работы с конкретными диаграммами, senior-devops для пайплайна и инфраструктуры.
- **docker-разработка** — Создание контейнеров. Комплементарная разработка - docker-создает образы, helm-chart-builder деплою их в Kubernetes.
- **ci-cd-пайплайн-строитель** — строительство пайплайна. Комплементарный — helm-chart-builder определяет артефакт развертывания, ci-cd-пайплайн-builder автоматизирует его доставку.
- **старший-безопасность** — Безопасность приложений. Дополнительный — helm-chart-builder охватывает безопасность на уровне Kubernetes (RBAC, pod security), senior-security охватывает угрозы на уровне приложений.
