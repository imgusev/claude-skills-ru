---
description: "Запустите полный аудит оператора Kubernetes (CRD + согласование + возможность) в текущем репозитории"
---

# /оператор-аудит { #operator-audit }

Запустите полный аудит в репозитории оператора Kubernetes:

1. Проверьте каждый CRD YAML на соответствие рекомендациям по шаблонам операторов
2. Используйте функцию согласования каждого контроллера Go для устранения шаблонов
3. Оцените оператора по уровням возможностей OperatorHub (1-5)
4. Выведите отчет Markdown с указанием пройденных/неудачных проверок и конкретными следующими шагами

## Использование { #usage }

```
/operator-audit
/operator-audit --operator-dir ./my-operator
/operator-audit --crd-dir ./config/crd --controller-dir ./controllers
```

## Реализация { #implementation }

```bash
SKILL=engineering/kubernetes-operator/skills/kubernetes-operator
DIR="${OPERATOR_DIR:-.}"

echo "## CRD validation"
python "$SKILL/scripts/crd_validator.py" --crd "$DIR/config/crd" || true

echo ""
echo "## Reconcile lint"
python "$SKILL/scripts/reconcile_lint.py" --controller "$DIR/controllers" || python "$SKILL/scripts/reconcile_lint.py" --controller "$DIR/internal/controller" || true

echo ""
echo "## Capability audit"
python "$SKILL/scripts/operator_capability_audit.py" --operator-dir "$DIR"
```

## Выход { #output }

Отчет о Markdown с:

- ** Результаты CRD** для каждого файла: СБОЙ / ПРЕДУПРЕЖДЕНИЕ / ПРОПУСК для каждой проверки
- ** Согласование результатов**: антишаблоны с номерами строк
- **Текущий уровень возможностей** + конкретные шаги по продвижению

## Предварительные условия { #pre-conditions }

- Запуск из репозитория операторов Kubernetes
- Контроллеры Go ожидаются на `controllers/` или `internal/controller/`
- Кредиты, ожидаемые на `config/crd/` (макет kubebuilder)
- `kubernetes-operator` установлен скилл

## Постусловия { #post-conditions }

- Отчет Markdown, переданный потоковой передачей на терминал
- Код выхода 0, если все ПРОЙДЕНО; 1, если какой-либо из них завершился неудачей
