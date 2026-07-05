---
title: "Старший инженер SecOps { #senior-secops-engineer } — Агентский скилл и плагин Codex"
description: "Старший инженер SecOps по скиллу безопасности приложений, управлению уязвимостями, проверке соответствия требованиям и методам безопасной разработки. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Старший инженер SecOps { #senior-secops-engineer }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `senior-secops`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/senior-secops/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Полный набор инструментов для обеспечения безопасности, включая управление уязвимостями, проверку соответствия требованиям, методы безопасного кодирования и автоматизацию безопасности.

---

## Оглавление { #table-of-contents }

- [Основные возможности](#core-capabilities)
- [Воркфлоу](#workflows)
- [Ссылка на инструмент](#tool-reference)
- [Стандарты безопасности](#security-standards)
- [Фреймворки обеспечения соответствия](#compliance-frameworks)
- [Лучшие практики](#best-practices)

---

## Основные возможности { #core-capabilities }

### 1. Сканер безопасности { #1-security-scanner }

Сканируйте исходный код на наличие уязвимостей в системе безопасности, включая жестко закодированные секреты, SQL-инъекцию, XSS, внедрение команд и обход пути.

```bash
# Scan project for security issues
python scripts/security_scanner.py /path/to/project

# Filter by severity
python scripts/security_scanner.py /path/to/project --severity high

# JSON output for CI/CD
python scripts/security_scanner.py /path/to/project --json --output report.json
```

**Обнаруживает:**
- Жестко закодированные секреты (API-ключи, пароли, учетные данные AWS, токены GitHub, приватные ключи)
- Шаблоны SQL-инъекций (конкатенация строк, f-строки, литералы шаблона)
- Уязвимости XSS (присвоение innerHTML, небезопасные манипуляции с DOM, небезопасные шаблоны React)
- Внедрение команды (shell=True, exec, eval с пользовательским вводом)
- Обход пути (файловые операции с пользовательским вводом)

### 2. Специалист по оценке уязвимости { #2-vulnerability-assessor }

Сканируйте зависимости на наличие известных CVE в экосистемах npm, Python и Go.

```bash
# Assess project dependencies
python scripts/vulnerability_assessor.py /path/to/project

# Critical/high only
python scripts/vulnerability_assessor.py /path/to/project --severity high

# Export vulnerability report
python scripts/vulnerability_assessor.py /path/to/project --json --output vulns.json
```

**Сканирование:**
- `package.json` и `package-lock.json` (npm)
- `requirements.txt` и `pyproject.toml` (Python)
- `go.mod` (Уходи)

**Выход:**
- Идентификаторы CVE с оценками CVSS
- Затронутые версии пакетов
- Исправленные версии для исправления
- Общая оценка риска (0-100)

### 3. Средство проверки соответствия требованиям { #3-compliance-checker }

Проверьте соответствие требованиям безопасности SOC 2, PCI-DSS, HIPAA и фреймворкам GDPR.

```bash
# Check all frameworks
python scripts/compliance_checker.py /path/to/project

# Specific framework
python scripts/compliance_checker.py /path/to/project --framework soc2
python scripts/compliance_checker.py /path/to/project --framework pci-dss
python scripts/compliance_checker.py /path/to/project --framework hipaa
python scripts/compliance_checker.py /path/to/project --framework gdpr

# Export compliance report
python scripts/compliance_checker.py /path/to/project --json --output compliance.json
```

**Проверяет:**
- Реализация контроля доступа
- Шифрование в состоянии покоя и при передаче
- Ведение журнала аудита
- Надежность аутентификации (MFA, хэширование паролей)
- Охранная документация
- Средства контроля безопасности CI/CD

---

## Воркфлоу { #workflows }

### Воркфлоу 1: Аудит безопасности { #workflow-1-security-audit }

Полная оценка безопасности кодовой базы.

```bash
# Step 1: Scan for code vulnerabilities
python scripts/security_scanner.py . --severity medium
# STOP if exit code 2 — resolve critical findings before continuing
```

```bash
# Step 2: Check dependency vulnerabilities
python scripts/vulnerability_assessor.py . --severity high
# STOP if exit code 2 — patch critical CVEs before continuing
```

```bash
# Step 3: Verify compliance controls
python scripts/compliance_checker.py . --framework all
# STOP if exit code 2 — address critical gaps before proceeding
```

```bash
# Step 4: Generate combined reports
python scripts/security_scanner.py . --json --output security.json
python scripts/vulnerability_assessor.py . --json --output vulns.json
python scripts/compliance_checker.py . --json --output compliance.json
```

### Воркфлоу 2: Гейт безопасности CI/CD { #workflow-2-cicd-security-gate }

Интегрируйте проверки безопасности в пайплайн развертывания.

```yaml
# .github/workflows/security.yml
name: "security-scan"

on:
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "set-up-python"
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: "security-scanner"
        run: python scripts/security_scanner.py . --severity high

      - name: "vulnerability-assessment"
        run: python scripts/vulnerability_assessor.py . --severity critical

      - name: "compliance-check"
        run: python scripts/compliance_checker.py . --framework soc2
```

На каждом шаге пайплайн завершается сбоем из—за соответствующего кода завершения - развертывание не продолжается после критического обнаружения.

### Воркфлоу 3: Сортировка CVE { #workflow-3-cve-triage }

Отреагируйте на новое CVE, влияющее на ваше приложение.

```
1. ASSESS (0-2 hours)
   - Identify affected systems using vulnerability_assessor.py
   - Check if CVE is being actively exploited
   - Determine CVSS environmental score for your context
   - STOP if CVSS 9.0+ on internet-facing system — escalate immediately

2. PRIORITIZE
   - Critical (CVSS 9.0+, internet-facing): 24 hours
   - High (CVSS 7.0-8.9): 7 days
   - Medium (CVSS 4.0-6.9): 30 days
   - Low (CVSS < 4.0): 90 days

3. REMEDIATE
   - Update affected dependency to fixed version
   - Run security_scanner.py to verify fix (must return exit code 0)
   - STOP if scanner still flags the CVE — do not deploy
   - Test for regressions
   - Deploy with enhanced monitoring

4. VERIFY
   - Re-run vulnerability_assessor.py
   - Confirm CVE no longer reported
   - Document remediation actions
```

### Воркфлоу 4: Реагирование на инциденты { #workflow-4-incident-response }

Процедура рассмотрения инцидентов, связанных с безопасностью.

```
PHASE 1: DETECT & IDENTIFY (0-15 min)
- Alert received and acknowledged
- Initial severity assessment (SEV-1 to SEV-4)
- Incident commander assigned
- Communication channel established

PHASE 2: CONTAIN (15-60 min)
- Affected systems identified
- Network isolation if needed
- Credentials rotated if compromised
- Preserve evidence (logs, memory dumps)

PHASE 3: ERADICATE (1-4 hours)
- Root cause identified
- Malware/backdoors removed
- Vulnerabilities patched (run security_scanner.py; must return exit code 0)
- Systems hardened

PHASE 4: RECOVER (4-24 hours)
- Systems restored from clean backup
- Services brought back online
- Enhanced monitoring enabled
- User access restored

PHASE 5: POST-INCIDENT (24-72 hours)
- Incident timeline documented
- Root cause analysis complete
- Lessons learned documented
- Preventive measures implemented
- Stakeholder report delivered
```

---

## Ссылка на инструмент { #tool-reference }

### security_scanner.py { #security_scannerpy }

| Вариант | Описание |
|--------|-------------|
| `target` | Каталог или файл для сканирования |
| `--severity, -s` | Минимальная степень тяжести: критическая, высокая, средняя, низкая |
| `--verbose, -v` | Показывать файлы по мере их сканирования |
| `--json` | Выводите результаты в формате JSON |
| `--output, -o` | Запись результатов в файл |

**Коды выхода:** `0` = нет критических/высоких результатов · `1` = результаты с высокой степенью серьезности · `2` = выводы о критической степени тяжести

### vulnerability_assessor.py { #vulnerability_assessorpy }

| Вариант | Описание |
|--------|-------------|
| `target` | Каталог, содержащий файлы зависимостей |
| `--severity, -s` | Минимальная степень тяжести: критическая, высокая, средняя, низкая |
| `--verbose, -v` | Показывать файлы по мере их сканирования |
| `--json` | Выводите результаты в формате JSON |
| `--output, -o` | Запись результатов в файл |

**Коды выхода:** `0` = отсутствие критических/высоких уязвимостей · `1` = уязвимости высокой степени серьезности · `2` = уязвимости критической степени серьезности

### compliance_checker.py { #compliance_checkerpy }

| Вариант | Описание |
|--------|-------------|
| `target` | Каталог для проверки |
| `--framework, -f` | Фреймворк: soc2, pci-dss, hipaa, gdpr, все |
| `--verbose, -v` | Показывать проверки по мере их выполнения |
| `--json` | Выводите результаты в формате JSON |
| `--output, -o` | Запись результатов в файл |

**Коды выхода:** `0` = соответствует требованиям (90%+ оценка) · `1` = несоответствие требованиям (оценка 50-69%) · `2` = критические пробелы (оценка <50%)

---

## Стандарты безопасности { #security-standards }

Видишь `references/security_standards.md` для получения полного руководства OWASP Top 10, стандартов безопасного кодирования, требований к аутентификации и средств контроля безопасности API.

### Чек-лист по безопасному кодированию Coding Coding { #secure-coding-checklist }

```markdown
## Input Validation
- [ ] Validate all input on server side
- [ ] Use allowlists over denylists
- [ ] Sanitize for specific context (HTML, SQL, shell)

## Output Encoding
- [ ] HTML encode for browser output
- [ ] URL encode for URLs
- [ ] JavaScript encode for script contexts

## Authentication
- [ ] Use bcrypt/argon2 for passwords
- [ ] Implement MFA for sensitive operations
- [ ] Enforce strong password policy

## Session Management
- [ ] Generate secure random session IDs
- [ ] Set HttpOnly, Secure, SameSite flags
- [ ] Implement session timeout (15 min idle)

## Error Handling
- [ ] Log errors with context (no secrets)
- [ ] Return generic messages to users
- [ ] Never expose stack traces in production

## Secrets Management
- [ ] Use environment variables or secrets manager
- [ ] Never commit secrets to version control
- [ ] Rotate credentials regularly
```

---

## Фреймворки обеспечения соответствия { #compliance-frameworks }

Видишь `references/compliance_requirements.md` для отображения полного контроля. Бежать `compliance_checker.py` чтобы проверить приведенные ниже элементы управления:

### SOC 2 Тип II { #soc-2-type-ii }
- **CC6** Логический доступ: аутентификация, авторизация, MFA
- **CC7** Системные операции: мониторинг, ведение журнала, реагирование на инциденты
- **CC8** Управление изменениями: CI/CD, ревью кода, элементы управления развертыванием

### PCI-DSS v4.0 { #pci-dss-v40 }
- **Требование 3/4**: Шифрование в состоянии покоя и при передаче (TLS 1.2+)
- **Требование 6**: Безопасная разработка (проверка входных данных, безопасное кодирование)
- **Требование 8**: Строгая аутентификация (MFA, политика паролей)
- **Требование 10/11**: Ведение журнала аудита, SAST/DAST/тестирование на проникновение

### Правило безопасности HIPAA { #hipaa-security-rule }
- Уникальные идентификаторы пользователей и протоколы аудита для доступа к PHI (164.312(a)(1), 164.312(b))
- MFA для аутентификации физического лица/организации (164.312(d))
- Шифрование передачи по протоколу TLS (164.312(e)(1))

### GDPR { #gdpr }
- **Статья 25/32**: Конфиденциальность по замыслу, шифрование, псевдонимизация
- **Статья 33**: Уведомление о нарушении в течение 72 часов
- **Статья 17/20**: Право на удаление и переносимость данных

---

## Лучшие практики { #best-practices }

### Управление секретами { #secrets-management }

```python
# BAD: Hardcoded secret
API_KEY = "sk-1234567890abcdef"

# GOOD: Environment variable
import os
API_KEY = os.environ.get("API_KEY")

# BETTER: Secrets manager
from your_vault_client import get_secret
API_KEY = get_secret("api/key")
```

### Предотвращение SQL-инъекций { #sql-injection-prevention }

```python
# BAD: String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Предотвращение XSS { #xss-prevention }

```javascript
// BAD: Direct innerHTML assignment is vulnerable
// GOOD: Use textContent (auto-escaped)
element.textContent = userInput;

// GOOD: Use sanitization library for HTML
import DOMPurify from 'dompurify';
const safeHTML = DOMPurify.sanitize(userInput);
```

### Аутентификация { #authentication }

```javascript
// Password hashing
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

// Hash password
const hash = await bcrypt.hash(password, SALT_ROUNDS);

// Verify password
const match = await bcrypt.compare(password, hash);
```

### Заголовки безопасности { #security-headers }

```javascript
// Express.js security headers
const helmet = require('helmet');
app.use(helmet());

// Or manually set headers:
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

---

## Быстрая проверка топ-10 OWASP { #owasp-top-10-quick-check }

Быстрая 15-минутная оценка — пройдитесь по каждой категории и отметьте "пройдено / не пройдено". Для тестирования на глубоком погружении обратитесь к скиллу **security-pen-testing**.

| # | Категория | Однострочная проверка |
|---|----------|----------------|
| A01 | Нарушенный контроль доступа | Проверьте проверки ролей на каждой конечной точке; протестируйте горизонтальную эскалацию привилегий |
| A02 | Криптографические сбои | Подтверждайте TLS 1.2+ везде; никаких секретов в журналах или источниках |
| A03 | Инъекция | Запустите аудит параметризованного запроса; проверьте использование ORM raw-запроса |
| A04 | Небезопасный дизайн | Для критических потоков существует модель угроз ревью |
| A05 | Неправильная настройка системы безопасности | Проверьте, удалены ли учетные данные по умолчанию; страницы ошибок общие |
| A06 | Уязвимые компоненты | Бежать `vulnerability_assessor.py`; нулевой критический/высокий CVE |
| A07 | Сбои при авторизации | Проверьте MFA от администратора; защита от перебора активна |
| A08 | Целостность программного обеспечения и данных | Подтвердите, что пайплайн CI/CD подписывает артефакты; неподписанных deps нет |
| A09 | Ведение журнала и мониторинг | Проверка журналов аудита, фиксирующих события аутентификации; настроенные оповещения |
| A10 | SSRF | Протестируйте внутренние фильтры URL; заблокируйте конечные точки метаданных (169.254.169.254) |

> ** Требуется глубокое погружение? ** Передайте `security-pen-testing` для получения полного охвата руководства по тестированию OWASP.

---

## Секретные инструменты сканирования { #secret-scanning-tools }

Выберите подходящий сканер для каждого этапа вашего воркфлоу:

| Инструмент | Лучше всего подходит для | Язык | Предварительная фиксация | CI/CD | Пользовательские правила |
|------|----------|----------|:----------:|:-----:|:------------:|
| **gitleaks - утечки** | Пайплайны CI, сканирование полного репозитория | Иди | Да | Да | Регулярные выражения TOML |
| **обнаружение-секреты** | Перехваты предварительной фиксации, инкрементные | Питон | Да | Частичный | Основанный на плагине |
| **Трюфельный хряк** | Глубокое сканирование истории, энтропия | Иди | Нет | Да | Регулярное выражение + энтропия |

**Рекомендуемая настройка:** Используйте `detect-secrets` как крючок перед фиксацией (перехватывает секреты до того, как они попадут в историю) и `gitleaks` в CI (улавливает все, что проскальзывает).

```bash
# detect-secrets pre-commit hook (.pre-commit-config.yaml)
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']

# gitleaks in GitHub Actions
- name: gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}
```

---

## Безопасность цепочки поставок { #supply-chain-security }

Защита от подделки зависимостей и артефактов с помощью генерации SBOM, подписи артефактов и соответствия SLSA.

**Генерация SBOM:**
- **syft** — генерирует SBOM из изображений контейнеров или исходных каталогов (форматы SPDX, CycloneDX)
- **cyclonedx-cli** — CycloneDX-собственный инструментарий; объединение нескольких SBOM для моно-репозиториев

```bash
# Generate SBOM from container image
syft packages ghcr.io/org/app:latest -o cyclonedx-json > sbom.json
```

**Подписание артефакта (Sigstore/cosign):**
```bash
# Sign a container image (keyless via OIDC)
cosign sign ghcr.io/org/app:latest
# Verify signature
cosign verify ghcr.io/org/app:latest --certificate-identity=ci@org.com --certificate-oidc-issuer=https://token.actions.githubusercontent.com
```

**Обзор уровней SLSA:**
| Уровень | Требование | Что это доказывает |
|-------|-------------|----------------|
| 1 | Задокументированный процесс сборки | Происхождение существует |
| 2 | Размещенный сервис сборки, подписанный источник | Защищенное от несанкционированного доступа происхождение |
| 3 | Прочная платформа для сборки, происхождение которой не поддается фальсификации | Конструкция, защищенная от несанкционированного доступа |
| 4 | Ревью с участием двух сторон, герметичные сборки | Максимальная надежность цепочки поставок |

> **Перекрестные ссылки:** `security-pen-testing` (тестирование использования уязвимостей), `dependency-auditor` (лицензия и аудит CVE на наличие зависимостей).

---

## Справочная документация { #reference-documentation }

| Документ | Описание |
|----------|-------------|
| `references/security_standards.md` | OWASP Top 10, безопасное кодирование, аутентификация, безопасность API |
| `references/vulnerability_management_guide.md` | Сортировка CVE, оценка CVSS, воркфлоу по устранению неполадок |
| `references/compliance_requirements.md` | Сопоставления полного контроля SOC 2, PCI-DSS, HIPAA, GDPR |
