---
name: "cross-eval"
description: "/cs: перекрестная оценка <памятка> - Многомодельный консенсус по записке правления или краткой стратегии. Кросс-ревью Claude + Codex + Gemini с плавной деградацией. Используйте, когда памятка с высокими ставками нуждается в независимой проверке на вменяемость перед заседанием совета директоров - например, сводная информация о ставках на компанию или условия сбора средств."
---

# /cs:cross-eval — Консенсус по нескольким моделям { #cscross-eval--multi-model-consensus }

**Команда:** `/cs:cross-eval <memo-or-brief>`

Запускает одну и ту же памятку через нескольких поставщиков моделей и согласовывает расхождения. Используйте для ** принятия необратимых решений с высокими ставками **, когда предвзятость в отношении одной модели обходится слишком дорого: слияния и поглощения, крупные сборы средств, увольнения, стратегические повороты, нормативные обязательства.

Адаптировано из gstack's `/codex` шаблон перекрестного ревью, обобщенный для ** служебных записок** вместо code PR.

## Когда запускать { #when-to-run }

- Прежде чем подписывать контрактный лист
- Прежде чем объявить об увольнении
- Прежде чем перейти на регулируемый рынок
- До принятия любого решения, отмена которого требует более 6 месяцев рабочего времени компании
- Когда голосование в зале заседаний было разделено или имело критическое несогласие

## Используемые модели (плавная деградация) { #models-used-graceful-degradation }

Команда пытается вызвать каждую доступную модель по порядку:

1. **Клод** (основной, всегда доступен) — родной голос зала заседаний
2. **Кодекс / OpenAI** (если `OPENAI_API_KEY` или `codex` Доступен CLI)
3. **Близнецы** (если `GEMINI_API_KEY` или `gemini` Доступен CLI)

Если доступен только Claude, команда запускает **Claude-только в режиме состязательности** — та же модель, разные начальные значения промптов — и четко помечает выходные данные как одномодельные.

## Воркфлоу { #workflow }

1. Прочтите памятку/ краткое изложение
2. Исследуйте среду для доступных ключей CLIs/API модели
3. Для каждой доступной модели:
   - Отправьте памятку с этим префиксом промпта:
     > "Вы независимый рецензент C-suite. Ниже приведена памятка для правления из зала заседаний другой компании. Определите 3 основные проблемы, 3 основные поддержки и свой голос (ОДОБРИТЬ / ОТКЛОНИТЬ / ОТЛОЖИТЬ). Не соглашайтесь почтительно — предполагайте, что рассуждения в записке ошибочны, пока не доказано обратное."
4. Соберите три независимых ревью
5. Согласовать: в чем они сходятся? Где они расходятся?
6. Выявляйте расхождения в виде вопросов к основателю

## Выходной формат { #output-format }

Сохранено в `~/.claude/cross-eval/YYYY-MM-DD-<slug>.md`:

```markdown
# Cross-Eval: <memo title>
**Date:** YYYY-MM-DD
**Memo reviewed:** <link>
**Models invoked:** Claude / Codex / Gemini (or noted fallbacks)

## Vote Tally
| Model | Vote | Confidence |
|---|---|---|
| Claude | APPROVE | High |
| Codex | DEFER | Med |
| Gemini | APPROVE | Low |

## Consensus Concerns (≥2 models flagged)
1. <concern> — flagged by Claude + Codex
2. <concern> — flagged by all 3

## Divergent Concerns (1 model flagged)
- <Codex only:> <concern> — worth a second look
- <Gemini only:> <concern> — likely noise, but check

## Consensus Supports (≥2 models endorsed)
1. <support>
2. <support>

## Recommendation
- 🟢 GO if 2+ models APPROVE and no CRITICAL concerns from any model
- 🟡 PAUSE if any model is DEFER or any concern is CRITICAL
- 🔴 STOP if 2+ models REJECT

## Open Questions for Founder
1. <question raised by divergence>
2. <question raised by divergence>
```

## Почему это так важно { #why-this-matters }

Рекомендации, основанные на одной модели, имеют систематические отклонения. Клод полезен и может недооценивать риск. Кодекс (OpenAI) проявляет большую осторожность в вопросах развивающихся рынков и регулирования. Близнецы более осторожны в заявлениях о техническом масштабе. Несогласие - это сигнал, а не шум.

Это ** система подстраховки перед необратимостью** — не замена внешнему консультанту или реальному совету директоров.

## Изящная деградация { #graceful-degradation }

Если только Клод будет свободен:

```markdown
**Models available:** Claude only
**Mode:** ADVERSARIAL — running 3 independent Claude passes with different system prompts:
  1. Standard reviewer
  2. Devil's advocate (must find 3 critical concerns)
  3. Steelman (must find 3 strongest reasons to approve)

This is weaker than true multi-model. Treat the result as suggestive, not conclusive.
```

## Маршрутизация { #routing }

- `/cs:decide` — если будет достигнут консенсус, ИДИТЕ
- `/cs:freeze` — если консенсус - это ПАУЗА
- `/cs:boardroom` (повторный запуск) — если консенсус ОСТАНОВЛЕН

## Связанный { #related }

- Скиллы: [`board-meeting`](../../../skills/board-meeting/SKILL.md), [`executive-mentor`](../../../executive-mentor/)
- Вдохновение: gstack's `/codex` шаблон перекрестного ревью (адаптирован для служебных записок)

---

**Версия:** 1.0.0
