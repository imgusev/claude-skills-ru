---
title: "Маркетинговые скиллы — Каталог + Маршрутизатор { #marketing-skills--directory--router } — Агентский скилл для маркетинга"
description: "Каталог и маршрутизатор для библиотеки скилл-маркетинга. Используйте, когда вам нужно найти подходящий маркетинговый скилл для выполнения задачи. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Маркетинговые скиллы — Каталог + Маршрутизатор { #marketing-skills--directory--router }

<div class="page-meta" markdown>
<span class="meta-badge">:material-bullhorn-outline: Маркетинг</span>
<span class="meta-badge">:material-identifier: `marketing-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/marketing-skill/skills/marketing-skills/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install marketing-skills</code>
</div>


Это индекс скилла для маркетингового плагина. Он выполняет одну задачу: направляет вас к нужному специалисту по скиллу, а затем убирается с дороги. Для логики маршрутизации по запросу, [../маркетинговые операции/СКИЛЛ.md](https://github.com/imgusev/claude-skills-ru/tree/main/marketing-skill/skills/marketing-ops/SKILL.md) является каноническим маршрутизатором — этот файл является картой.

** Подсчитано (честно):** 44 специальных скилла в `skills/` (плюс этот индекс и устаревший `content-creator` перенаправление), 1 видео-скилл в `video-content-strategist/`, 59 инструментов Python только для stdlib. Установка pip не требуется.

## Начните здесь { #start-here }

1. ** Первый запуск когда-либо? ** Используйте `skills/marketing-context/` чтобы создать `.claude/product-marketing-context.md` Любой другой скилл учитывает это в отношении голоса бренда, персоналий и конкурентной среды.
2. ** Знаете свою задачу? ** Найдите ее в таблице маршрутов ниже и загрузите только этот скилл. `SKILL.md`.
3. **Неоднозначный запрос?** Загрузить `skills/marketing-ops/` — его матрица маршрутизации сопоставляет фразы с скиллами.

## Таблица маршрутов { #route-table }

Все пути относятся к `marketing-skill/`.

### Фонд + Операции { #foundation--ops }
| Задача | Скилл |
|---|---|
| Захват контекста бренда/продукта (запуск в первую очередь) | `skills/marketing-context/` |
| Направляйте запрос, планируйте кампании, выбирайте каналы | `skills/marketing-ops/` |
| Программы формирования спроса, воронка + CRM-операции | `skills/marketing-demand-acquisition/` |
| Позиционирование, ICP, маркетинговая стратегия продукта | `skills/marketing-strategy-pmm/` |
| Аудит голосовой/визуальной согласованности бренда | `skills/brand-guidelines/` |

### Содержание { #content }
| Задача | Скилл |
|---|---|
| Пишите посты в блогах, статьи, руководства | `skills/content-production/` |
| Планируйте, какой контент создавать | `skills/content-strategy/` |
| Редактировать копию (семь просмотров) | `skills/copy-editing/` |
| Исправлен контент, похожий на искусственный интеллект | `skills/content-humanizer/` |
| Копия целевой страницы/страницы продаж | `skills/copywriting/` |
| Заголовки, зацепки, генерация идей | `skills/marketing-ideas/` |
| Фреймворки убеждения, ментальные модели | `skills/marketing-psychology/` |

### SEO + AEO { #seo--aeo }
| Задача | Скилл |
|---|---|
| Традиционный SEO-аудит | `skills/seo-audit/` |
| Ссылки на поиск с помощью искусственного интеллекта (чат, недоумение, обзоры с помощью искусственного интеллекта) | `skills/aeo/` |
| Масштабируемое программное SEO | `skills/programmatic-seo/` |
| Структурированные данные / schema.org | `skills/schema-markup/` |
| Структура сайта, внутренние ссылки | `skills/site-architecture/` |

### CRO (конверсия) { #cro-conversion }
| Задача | Скилл |
|---|---|
| Конверсия целевой/маркетинговой страницы | `skills/page-cro/` |
| Формы | `skills/form-cro/` |
| Поток регистрации | `skills/signup-flow-cro/` |
| Онбординг/активация | `skills/onboarding-cro/` |
| Всплывающие окна/модалы | `skills/popup-cro/` |
| Платный доступ/экраны обновления | `skills/paywall-upgrade-cro/` |
| Дизайн A/B теста + размер выборки | `skills/ab-test-setup/` |

### Каналы { #channels }
| Задача | Скилл |
|---|---|
| Последовательности сообщений электронной почты/капли | `skills/email-sequence/` |
| Холодная исходящая электронная почта | `skills/cold-email/` |
| Платная реклама (Google/Meta/LinkedIn) | `skills/paid-ads/` |
| Рекламный креатив + копия | `skills/ad-creative/` |
| Социальный календарь + управление | `skills/social-media-manager/` |
| Платформа - собственные посты в социальных сетях | `skills/social-content/` |
| X/Рост Twitter | `skills/x-twitter-growth/` |
| YouTube (данные + стратегия) | `skills/youtube-full/` |
| Стратегия создания видеоконтента | `video-content-strategist/` (родственная папка, собственный плагин) |
| Вебинары (математика воронки) | `skills/webinar-marketing/` |
| App Store / Play Store (ASO) | `skills/app-store-optimization/` |

### Рост { #growth }
| Задача | Скилл |
|---|---|
| Запуски (PH, HN и т.д.) | `skills/launch-strategy/` |
| Цена + упаковка | `skills/pricing-strategy/` |
| Реферальные программы | `skills/referral-program/` |
| Бесплатные инструменты как приобретение | `skills/free-tool-strategy/` |
| Предотвращение оттока | `skills/churn-prevention/` |

### Интеллект + стимулирование продаж { #intelligence--sales-enablement }
| Задача | Скилл |
|---|---|
| Эффективность кампании, атрибуция | `skills/campaign-analytics/` |
| Планы отслеживания, UTM, ключевые события GA4 | `skills/analytics-tracking/` |
| Анализ социальных аккаунтов | `skills/social-media-analyzer/` |
| Страницы конкурентов/альтернатив | `skills/competitor-alternatives/` |
| Шаблоны промптов LLM + управление для маркетинговых команд | `skills/prompt-engineer-toolkit/` |

## Инструменты Python { #python-tools }

Каждый скилл документирует свои собственные инструменты в своей SKILL.md (раздел "Инструменты" или "воркфлоу" с точными строками CLI). Вызывается из папки скилла:

```bash
python3 skills/<skill>/scripts/<tool>.py --help
```

Все 59 скриптов доступны только для stdlib; большинство из них запускают демо-версию без аргументов.

## Правила { #rules }

- Загружайте по ОДНОМУ скиллу специалиста для каждой задачи — никогда не загружайте их массово.
- Если `.claude/product-marketing-context.md` существует, прочтите его перед выполнением любой маркетинговой задачи.
- `content-creator` является устаревшим — используйте `skills/content-production/`.
- Не устанавливайте ничего в pip-режиме для этих инструментов.
