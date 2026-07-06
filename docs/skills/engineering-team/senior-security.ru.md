---
title: "Старший инженер по безопасности — Моделирование угроз + Маршрутизатор безопасности { #senior-security-engineer--threat-modeling--security-router } — Агентский скилл и плагин Codex"
description: "Используйте, когда пользователь запрашивает моделирование угроз STRIDE, оценку рисков DREAD, анализ угроз на основе диаграммы потоков данных или. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Старший инженер по безопасности — Моделирование угроз + Маршрутизатор безопасности { #senior-security-engineer--threat-modeling--security-router }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `senior-security`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/senior-security/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Этот скилл сам выполняет ровно одну работу — ** Моделирование угроз STRIDE / DREAD ** (плюс быстрое секретное сканирование) — и направляет все остальные запросы безопасности специалисту по скиллу, которому принадлежит эта полоса. Не дублируйте здесь родственный контент; вместо этого проложите маршрут.

## Таблица маршрутизации (сначала прочтите это) { #routing-table-read-this-first }

| Пользователь хочет... | Маршрут к | Почему этот скилл владеет им |
|---|---|---|
| Оценка уязвимости, методология ручного тестирования, тестирование OWASP Top 10 | [`skills/security-pen-testing`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/security-pen-testing) | Корабли `vulnerability_scanner.py` + `dependency_auditor.py` с контрактами с кодом выхода |
| Сортировка инцидентов, классификация SEV, судебно-медицинская экспертиза, локализация | [`skills/incident-response`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/incident-response) | Таксономия SEV1–SEV4, фазы NIST SP 800-61, `incident_triage.py` |
| Команда по отключению производства (инциденты, не связанные с безопасностью) | [`skills/incident-commander`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/incident-commander) | Классификатор серьезности + временная шкала + инструменты для вскрытия |
| Мониторинг безопасности, соглашения об уровне обслуживания CVE, проверки соответствия требованиям (SOC 2 и т.д.), заголовки безопасности | [`skills/senior-secops`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/senior-secops) | `security_scanner.py` + `compliance_checker.py`, Таблица CVE SLA |
| Враждебный/adversarial ревью кода | [`skills/adversarial-reviewer`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/adversarial-reviewer) | ревью 3-персоны с БЛОКИРОВКОЙ/ПРОБЛЕМАМИ/ЧИСТЫМ вердиктом |
| Ревью защищенного кода как часть общего ревью | [`skills/code-reviewer`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/code-reviewer) | Языковая диспетчеризация + регрессионные настройки |
| Пути эскалации IAM в облаке, доступ к S3, группы безопасности | [`skills/cloud-security`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/cloud-security) | `cloud_posture_check.py` с кодами выхода для каждой проверки |
| Поиск угроз, проверка IOC, обнаружение аномалий | [`skills/threat-detection`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/threat-detection) | аномалия z-балла + инструмент для определения стойкости IOC |
| Red-планирование взаимодействия с командой, цепочки убийств ATT и CK | [`skills/red-team`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/red-team) | `engagement_planner.py` с гейтом авторизации |
| Поверхность атаки LLM/AI (инъекция промпта, отравление) | [`skills/ai-security`](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/ai-security) | Нанесенный на карту АТЛАСОМ `ai_threat_scanner.py` |

Если запрос охватывает полосы пропускания (например, "защитите эту новую архитектуру"), сначала выполните модель угроз здесь — ее выходные данные (приоритетные угрозы + меры по смягчению) сообщают вам, какие из них загружать следующими. Никогда не загружайте сразу несколько скилл безопасности умозрительно.

## Чем владеет этот скилл: Пошаговое моделирование угроз { #what-this-skill-owns-stride-threat-modeling }

### Воркфлоу { #workflow }

1. **Область применения: ** активы для защиты, границы доверия, потоки данных (внешние объекты, процессы, хранилища данных, потоки потоков).
2. **Сгенерировать модель угрозы** для каждого компонента:
   ```bash
   python3 scripts/threat_modeler.py --component "User Authentication" --assets "credentials,sessions" --json --output threats.json
   ```
   Выходные данные: категория СТЕПЕНИ опасности для каждой угрозы, оценка DREAD (ущерб, воспроизводимость, возможность использования, затронутые пользователи, обнаруживаемость — каждая от 1 до 10) и предлагаемые меры по смягчению последствий. Повторяется для каждого элемента DFD; `--interactive` обходит вопросы, определяющие сферу охвата; `--list-threats` показывает базу данных угроз.
3. **Потребляйте выходные данные:** сортируйте `threats.json` по убывающей оценке СТРАХА; все, что в среднем имеет значение ≥ 7, нуждается в именованном владельце по смягчению последствий до того, как проект будет представлен. Сопоставьте каждое смягчение с ответственной родственной полосой (например, угрозы IAM → `cloud-security`, угрозы инъекций → `code-reviewer`).
4. ** Быстрая проверка секретности ** пока у вас открыта кодовая база:
   ```bash
   python3 scripts/secret_scanner.py /path/to/project --format json --severity high
   ```
   Более 20 шаблонов (ключи AWS, токены GitHub, закрытые ключи, общие учетные данные). Любой критический/high блоки поиска объединяются до тех пор, пока не будут повернуты и перемещены в секретный менеджер.
5. ** Гейт проверки: ** для каждого элемента DFD учитывается ≥ 1 шаговая строка, для каждой угрозы с DREAD ≥ 7 есть защита owner +, а секретное сканирование завершается с нулевым значением high./critical выводы. Повторно запустите оба инструмента после устранения неполадок — этот повторный запуск является сигналом "Готово", а не документом.

### ШАГ на элемент матрицы { #stride-per-element-matrix }

| Элемент DFD | S | Т | R | Я | D | E |
|-------------|---|---|---|---|---|---|
| Внешняя сущность | X | | X | | | |
| Процесс | X | X | X | X | X | X |
| Хранилище данных | | X | X | X | X | |
| Поток данных | | X | | X | X | |

(S=Подмена →аутентификация, T=Вмешательство →целостность, R=Отказ → журналы аудита, I=Раскрытие информации →шифрование/access управление, D=DoS→ограничение скорости/redundancy, E=Повышение уровня→наименьшие привилегии.)

## Ссылки (загружаются по запросу) { #references-load-on-demand }

| Документ | Содержание |
|----------|---------|
| [ссылки/threat-modeling-guide.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/senior-security/references/threat-modeling-guide.md) | Методология STRIDE, деревья атак, оценка СТРАХА, создание DFD |
| [ссылки/security-architecture-patterns.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/senior-security/references/security-architecture-patterns.md) | Нулевое доверие, глубокая защита, шаблоны аутентификации, безопасность API |
| [ссылки/cryptography-implementation.md](https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/senior-security/references/cryptography-implementation.md) | AES-GCM, Ed25519, хэширование паролей (Argon2id), управление ключами |

Ссылки на архитектуру и криптографию сохраняются, поскольку их не отправляет ни один родственник; для * работы* эти элементы управления (сканирование, соответствие требованиям, мониторинг) по-прежнему направляются к `senior-secops`.
