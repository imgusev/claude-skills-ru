---
title: "Вопросы регулирования и Скиллы по управлению качеством — Router { #regulatory-affairs--quality-management-skills--router } — Агентский скилл для комплаенса"
description: "Маршрутизатор/ индекс для 15 скилл по регулированию и управлению качеством, включенных в этот плагин (ISO 13485 QMS, MDR ЕС 2017/745, заявки FDA в. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Вопросы регулирования и Скиллы по управлению качеством — Router { #regulatory-affairs--quality-management-skills--router }

<div class="page-meta" markdown>
<span class="meta-badge">:material-shield-check-outline: Регуляторика и качество</span>
<span class="meta-badge">:material-identifier: `ra-qm-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/ra-qm-team/skills/ra-qm-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install ra-qm-skills</code>
</div>


Этот плагин включает в себя ** 15 скилл соответствия требованиям ** для организаций HealthTech/MedTech-технологий (этот маршрутизатор является 16-й папкой в разделе `ra-qm-team/skills/`). Каждый скилл является самодостаточным.

## Таблица маршрутизации { #routing-table }

Сопоставьте запрос, затем загрузите `ra-qm-team/skills/<skill>/SKILL.md`. Если несколько строк совпадают, сначала задайте один уточняющий вопрос.

| Сигналы запроса | Скилл | Путь |
|---|---|---|
| Стратегия регулирования, выбор пути, планирование подачи заявок | руководитель по нормативно-правовым вопросам | `skills/regulatory-affairs-head/` |
| Ревью руководства, ключевые показатели качества, управление QMR | менеджер по качеству-qmr | `skills/quality-manager-qmr/` |
| Внедрение системы менеджмента качества ISO 13485, управление технологическими процессами | менеджер по качеству-СМК-iso13485 | `skills/quality-manager-qms-iso13485/` |
| ISO 14971 анализ рисков, FMEA, файлы рисков | специалист по управлению рисками | `skills/risk-management-specialist/` |
| Анализ первопричин, корректирующие/превентивные действия | капа-офицер | `skills/capa-officer/` |
| Контроль документооборота, 21 CFR, часть 11, DHF/DMR/DHR | качество-документация-менеджер | `skills/quality-documentation-manager/` |
| Внутренний аудит ISO 13485, классификация NC | смк-аудит-эксперт | `skills/qms-audit-expert/` |
| Планирование и проведение аудита по стандарту ISO 27001 | isms-аудит-эксперт | `skills/isms-audit-expert/` |
| Разработка ISMS, оценка рисков безопасности | менеджер по информационной безопасности-iso27001 | `skills/information-security-manager-iso27001/` |
| Классификация MDR ЕС, технические файлы, PSUR | mdr-745-специалист | `skills/mdr-745-specialist/` |
| FDA 510(k)/PMA/De Novo, QMSR | fda-консультант-специалист | `skills/fda-consultant-specialist/` |
| GDPR/DSGVO, DPIA, права субъектов данных | gdpr-dsgvo-эксперт | `skills/gdpr-dsgvo-expert/` |
| Классификация рисков в соответствии с Законом ЕС об ИИ, обязательства | eu-ai-act-специалист | `skills/eu-ai-act-specialist/` |
| Система управления искусственным интеллектом ISO/IEC 42001 | iso42001-специалист | `skills/iso42001-specialist/` |
| SOC 2 Готовность I/II типа, критерии доверия | soc2-соответствие требованиям | `skills/soc2-compliance/` |

## Быстрый старт { #quick-start }

```bash
# Example: route a risk-analysis request
cat ra-qm-team/skills/risk-management-specialist/SKILL.md
python3 ra-qm-team/skills/risk-management-specialist/scripts/risk_matrix_calculator.py --help
```

## Правила { #rules }

- Перейдите ровно к одному скиллу, затем следуйте воркфлоу этого скилла. Этот маршрутизатор не поставляет никаких собственных инструментов.
- Все выходные данные являются поддержкой принятия решений: окончательные определения соответствия направляются указанному владельцу (QMR, DPO, консультанту по нормативным вопросам) — никогда не принимаются автоматически.
- Сверьте ссылки на нормативные акты с текущим текстом (например, FDA QMSR, вступивший в силу 2026-02-02, заменил устаревшие подразделы QSR).
