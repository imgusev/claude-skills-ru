---
name: "tdd-guide"
description: "Скиллы разработки на основе тестирования для написания модульных тестов, создания тестовых приспособлений и макетов, анализа пробелов в покрытии и руководства воркфлоу с красно-зеленым рефакторингом в Jest, Pytest, JUnit, Vitest и Mocha. Используйте, когда пользователь просит написать тесты, улучшить тестовое покрытие, попрактиковаться в TDD, сгенерировать макеты или заглушки или упоминает тестовые фреймворки, такие как Jest, pytest или JUnit."
---

# Руководство по TDD { #tdd-guide }

Скилл разработки на основе тестирования для создания тестов, анализа покрытия и управления воркфлоу с красно-зеленым рефакторингом в Jest, Pytest, JUnit и Vitest.

---

## Воркфлоу { #workflows }

### Генерируйте тесты из кода { #generate-tests-from-code }

1. Предоставьте исходный код (TypeScript, JavaScript, Python, Java).
2. Укажите целевой фреймворк (Jest, Pytest, JUnit, Vitest)
3. Бежать `test_generator.py` с требованиями
4. Ревью сгенерированные тестовые заглушки
5. ** Проверка:** Тесты компилируются и охватывают счастливый путь, случаи ошибок, крайние случаи

### Анализ пробелов в охвате { #analyze-coverage-gaps }

1. Сгенерировать отчет о покрытии с помощью test runner (`npm test -- --coverage`)
2. Бежать `coverage_analyzer.py` в отчете LCOV/JSON/XML
3. Ревью приоритетных пробелов (P0/P1/P2)
4. Генерировать пропущенные тесты для непокрытых путей
5. ** Проверка:** Охват соответствует целевому порогу (обычно 80%+)

### Новая функция TDD { #tdd-new-feature }

1. Сначала запишите неудачный тест (КРАСНЫЙ)
2. Бежать `tdd_workflow.py --phase red` для проверки
3. Реализовать минимальный код для передачи (ЗЕЛЕНЫЙ)
4. Бежать `tdd_workflow.py --phase green` для проверки
5. Рефакторинг при сохранении зеленого цвета тестов (РЕФАКТОРИНГ)
6. ** Проверка:** Все тесты проходят после каждого цикла

---

## Примеры { #examples }

### Генерация теста — Ввод → вывод (Pytest) { #test-generation--input--output-pytest }

**Функция источника входного сигнала (`math_utils.py`):**
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Команда:**
```bash
python scripts/test_generator.py --input math_utils.py --framework pytest
```

**Сгенерированный тестовый результат (`test_math_utils.py`):**
```python
import pytest
from math_utils import divide

class TestDivide:
    def test_divide_positive_numbers(self):
        assert divide(10, 2) == 5.0

    def test_divide_negative_numerator(self):
        assert divide(-10, 2) == -5.0

    def test_divide_float_result(self):
        assert divide(1, 3) == pytest.approx(0.333, rel=1e-3)

    def test_divide_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_zero_numerator(self):
        assert divide(0, 5) == 0.0
```

---

### Анализ покрытия — Выборка выходных данных P0/P1/P2 { #coverage-analysis--sample-p0p1p2-output }

**Команда:**
```bash
python scripts/coverage_analyzer.py --report lcov.info --threshold 80
```

**Выборочный вывод:**
```
Coverage Report — Overall: 63% (threshold: 80%)

P0 — Critical gaps (uncovered error paths):
  auth/login.py:42-58   handle_expired_token()       0% covered
  payments/process.py:91-110  handle_payment_failure()   0% covered

P1 — High-value gaps (core logic branches):
  users/service.py:77   update_profile() — else branch  0% covered
  orders/cart.py:134    apply_discount() — zero-qty guard  0% covered

P2 — Low-risk gaps (utility / helper functions):
  utils/formatting.py:12  format_currency()            0% covered

Recommended: Generate tests for P0 items first to reach 80% threshold.
```

---

## Ключевые инструменты { #key-tools }

| Инструмент | Цель | Использование |
|------|---------|-------|
| `test_generator.py` | Генерируйте тестовые примеры из кода/requirements | `python scripts/test_generator.py --input source.py --framework pytest` |
| `coverage_analyzer.py` | Разбирать и анализировать отчеты о покрытии | `python scripts/coverage_analyzer.py --report lcov.info --threshold 80` |
| `tdd_workflow.py` | Направляйте красно-зеленые циклы рефакторинга | `python scripts/tdd_workflow.py --phase red --test test_auth.py` |
| `fixture_generator.py` | Генерируйте тестовые данные и издевайтесь | `python scripts/fixture_generator.py --entity User --count 5` |

Дополнительные скрипты: `framework_adapter.py` (преобразование между фреймворками), `metrics_calculator.py` (показатели качества), `format_detector.py` (определение языка/framework), `output_formatter.py` (CLI/desktop/Вывод CI).

---

## Входные требования { #input-requirements }

**Для генерации тестов:**
- Исходный код (путь к файлу или вставленное содержимое)
- Целевой фреймворк (Jest, Pytest, JUnit, Vitest)
- Область охвата (модуль, интеграция, пограничные случаи)

**Для анализа охвата:**
- Файл отчета о покрытии (формат LCOV, JSON или XML)
- Необязательно: Исходный код для контекста
- Необязательно: Целевой пороговый процент

**Для воркфлоу TDD:**
- Требования к функциям или история пользователя
- Текущая фаза (КРАСНЫЙ, ЗЕЛЕНЫЙ, РЕФАКТОРИНГ)
- Тестовый код и статус реализации

---

## Спецификация-Первый воркфлоу { #spec-first-workflow }

TDD наиболее эффективен, когда руководствуется письменной спецификацией. Поток:

1. **Написать или получить спецификацию** — хранится в `specs/<feature>.md`
2. **Извлеките критерии приемлемости** — каждый критерий становится одним или несколькими тестовыми примерами
3. **Запишите неудачные тесты (красный цвет)** — по одному тесту на каждый критерий приемлемости
4. **Реализовать минимальный код (зеленый)** — выполнить каждый тест по порядку
5. **Рефакторинг** — очистка, пока все тесты остаются зелеными

### Соглашение о каталоге спецификаций { #spec-directory-convention }

```
project/
├── specs/
│   ├── user-auth.md          # Feature spec with acceptance criteria
│   ├── payment-processing.md
│   └── notification-system.md
├── tests/
│   ├── test_user_auth.py     # Tests derived from specs/user-auth.md
│   ├── test_payments.py
│   └── test_notifications.py
└── src/
```

### Извлечение тестов из спецификаций { #extracting-tests-from-specs }

Каждый критерий приемлемости в спецификации соответствует по крайней мере одному тесту:

| Специальный критерий | Тестовый пример |
|---------------|-----------|
| "Пользователь может войти в систему с действительными учетными данными" | `test_login_valid_credentials_returns_token` |
| "Неверный пароль возвращает 401" | `test_login_invalid_password_returns_401` |
| "Учетная запись заблокирована после 5 неудачных попыток" | `test_login_locks_after_five_failures` |

** Совет: ** Укажите свои критерии приемлемости в спецификации. Ссылайтесь на номер в тестовой строке документации для обеспечения прослеживаемости (`# AC-3: Account locks after 5 failed attempts`).

> **Перекрестная ссылка:** Смотрите `engineering/spec-driven-workflow` ознакомьтесь с полной методологией спецификации, включая шаблоны спецификации и чек-листы для ревью.

---

## Красный-Зеленый-Примеры рефакторинга для каждого языка { #red-green-refactor-examples-per-language }

### Машинописный текст / Шутка { #typescript--jest }

```typescript
// test/cart.test.ts
describe("Cart", () => {
  describe("addItem", () => {
    it("should add a new item to an empty cart", () => {
      const cart = new Cart();
      cart.addItem({ id: "sku-1", name: "Widget", price: 9.99, qty: 1 });

      expect(cart.items).toHaveLength(1);
      expect(cart.items[0].id).toBe("sku-1");
    });

    it("should increment quantity when adding an existing item", () => {
      const cart = new Cart();
      cart.addItem({ id: "sku-1", name: "Widget", price: 9.99, qty: 1 });
      cart.addItem({ id: "sku-1", name: "Widget", price: 9.99, qty: 2 });

      expect(cart.items).toHaveLength(1);
      expect(cart.items[0].qty).toBe(3);
    });

    it("should throw when quantity is zero or negative", () => {
      const cart = new Cart();
      expect(() =>
        cart.addItem({ id: "sku-1", name: "Widget", price: 9.99, qty: 0 })
      ).toThrow("Quantity must be positive");
    });
  });
});
```

### Python / Pytest (расширенные шаблоны) { #python--pytest-advanced-patterns }

```python
# tests/conftest.py — shared fixtures
import pytest
from app.db import create_engine, Session

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    session = Session(bind=db_engine)
    yield session
    session.rollback()
    session.close()

# tests/test_pricing.py — parametrize for multiple cases
import pytest
from app.pricing import calculate_discount

@pytest.mark.parametrize("subtotal, expected_discount", [
    (50.0, 0.0),       # Below threshold — no discount
    (100.0, 5.0),      # 5% tier
    (250.0, 25.0),     # 10% tier
    (500.0, 75.0),     # 15% tier
])
def test_calculate_discount(subtotal, expected_discount):
    assert calculate_discount(subtotal) == pytest.approx(expected_discount)
```

### Тесты, управляемые таблицами Go { #go--table-driven-tests }

```go
// cart_test.go
package cart

import "testing"

func TestApplyDiscount(t *testing.T) {
    tests := []struct {
        name     string
        subtotal float64
        want     float64
    }{
        {"no discount below threshold", 50.0, 0.0},
        {"5 percent tier", 100.0, 5.0},
        {"10 percent tier", 250.0, 25.0},
        {"15 percent tier", 500.0, 75.0},
        {"zero subtotal", 0.0, 0.0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := ApplyDiscount(tt.subtotal)
            if got != tt.want {
                t.Errorf("ApplyDiscount(%v) = %v, want %v", tt.subtotal, got, tt.want)
            }
        })
    }
}
```

---

## Правила ограниченной автономии { #bounded-autonomy-rules }

При автономном создании тестов следуйте этим правилам, чтобы решить, когда остановиться, и спросить пользователя:

### Остановитесь и спросите, когда { #stop-and-ask-when }

- **Неоднозначные требования** — спецификация или пользовательская история содержат противоречивые или неясные критерии приемлемости
- **Пропущенные граничные случаи ** — вы не можете определить граничные значения без знания предметной области (например, максимально допустимая сумма транзакции).
- ** Количество тестов превышает 50** — перед выполнением больших наборов тестов требуется ревью от человека; представьте резюме и спросите, в каких областях следует расставить приоритеты
- ** Внешние зависимости неясны ** — функция основана на сторонних API или сервисах с недокументированным поведением
- ** Логика, чувствительная к безопасности** - аутентификация, авторизация, шифрование или потоки платежей требуют участия человека в тестовых сценариях

### Продолжайте автономно, когда { #continue-autonomously-when }

- ** Четкая спецификация с пронумерованными критериями приемлемости** — каждый критерий напрямую связан с тестами
- ** Простые операции CRUD** — создание, чтение, обновление, удаление с помощью четко определенных моделей
- ** Четко определенные контракты API** - доступны спецификации OpenAPI или типизированные интерфейсы
- **Чистые функции** — детерминированный ввод/output без каких-либо побочных эффектов
- ** Существующие шаблоны тестирования** — в базе кода уже есть аналогичные тесты, которым нужно следовать

---

## Тестирование на основе свойств { #property-based-testing }

Тестирование, основанное на свойствах, генерирует случайные входные данные для проверки инвариантов вместо того, чтобы полагаться на подобранные вручную примеры. Используйте его, когда пространство ввода велико и ожидаемое поведение может быть описано как свойство.

### Питон — гипотеза { #python--hypothesis }

```python
from hypothesis import given, strategies as st
from app.serializers import serialize, deserialize

@given(st.text())
def test_roundtrip_serialization(data):
    """Serialization followed by deserialization returns the original."""
    assert deserialize(serialize(data)) == data

@given(st.integers(), st.integers())
def test_addition_is_commutative(a, b):
    assert a + b == b + a
```

### Машинопись — быстрая проверка { #typescript--fast-check }

```typescript
import fc from "fast-check";
import { encode, decode } from "./codec";

test("encode/decode roundtrip", () => {
  fc.assert(
    fc.property(fc.string(), (input) => {
      expect(decode(encode(input))).toBe(input);
    })
  );
});
```

### Когда использовать на основе свойств, а не на основе примеров { #when-to-use-property-based-over-example-based }

| Использовать на основе свойств | Пример |
|-------------------|---------|
| Преобразования данных | Сериализовать/deserialize поездки туда и обратно |
| Математические свойства | Коммутативность, ассоциативность, идемпотентность |
| Кодирование/decoding | Base64, кодировка URL, сжатие |
| Сортировка и фильтрация | Выходные данные отсортированы, длина сохранена |
| Корректность синтаксического анализатора | Допустимый ввод всегда анализируется без ошибок |

---

## Тестирование на мутации { #mutation-testing }

Тестирование мутаций изменяет ваш производственный код (создает "мутантов") и проверяет, улавливают ли ваши тесты изменения. Если мутант выживает (тесты все еще проходят), в ваших тестах есть пробел, который не может быть выявлен одним только охватом.

### Инструменты { #tools }

| Язык | Инструмент | Команда |
|----------|------|---------|
| Машинопись/JavaScript | **Страйкер** | `npx stryker run` |
| Питон | **мутмут** | `mutmut run --paths-to-mutate=src/` |
| Java | **ЯМА** | `mvn org.pitest:pitest-maven:mutationCoverage` |

### Почему важно тестирование на мутации { #why-mutation-testing-matters }

- ** 100% покрытие строк ! = хорошие тесты ** — покрытие сообщает вам, что код был выполнен, а не что он был проверен
- **Перехватывает слабые утверждения** — тесты, которые запускают код, но не утверждают ничего значимого
- ** Находит пропущенные граничные тесты** — мутанты, которые изменяются `<` к `<=` выставляйте зазоры поодиночке
- **Количественный показатель качества** — оценка мутаций (% убитых мутантов) является более сильным сигналом, чем охват %

** Рекомендация:** Запустите тестирование мутаций на критических путях (авторизация, платежи, обработка данных), даже если общий охват высок. Целевой показатель мутации 85%+ по модулям P0.

---

## Перекрестные ссылки { #cross-references }

| Скилл | Отношения |
|-------|-------------|
| `engineering/spec-driven-workflow` | Спецификация → критерии приемки → пайплайн для тестирования вытяжки |
| `engineering-team/focused-fix` | Фаза 5 (Проверка) использует TDD для подтверждения исправления с помощью регрессионного теста |
| `engineering-team/senior-qa` | Более широкая стратегия контроля качества; TDD - это один из уровней пирамиды тестирования |
| `engineering-team/code-reviewer` | Проведите ревью сгенерированных тестов на предмет качества утверждений и полноты охвата |
| `engineering-team/senior-fullstack` | Строительные леса проекта включают в себя инфраструктуру тестирования, совместимую с воркфлоу TDD |

---

## Ограничения { #limitations }

| Сфера применения | Детали |
|-------|---------|
| Фокус модульного тестирования | Тесты интеграции и E2E требуют разных шаблонов |
| Статический анализ | Не удается выполнить тесты или измерить поведение во время выполнения |
| Языковая поддержка | Лучше всего подходит для TypeScript, JavaScript, Python, Java |
| Форматы отчетов | Только LCOV, JSON, XML; другие форматы требуют преобразования |
| Сгенерированные тесты | Обеспечьте строительные леса; требуйте ревью от человека для сложной логики |

**Когда следует использовать другие инструменты:**
- Тестирование E2E: Драматург, Cypress, Selenium
- Тестирование производительности: k6, JMeter, Locust
- Тестирование безопасности: OWASP ZAP, Burp Suite
