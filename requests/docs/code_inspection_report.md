## 1. Краткое описание архитектуры проекта

Приложение построено по **слоистой архитектуре** (layered architecture) и предназначено для учёта пользователей и их заявок в консольном режиме.

```text
main.py
   └── ApplicationService          ← composition root (сборка зависимостей)
           ├── UserRepository
           ├── TicketRepository
           ├── UserService
           └── TicketService ──→ UserService   ← интеграция модулей
   └── ConsoleInterface            ← ввод/вывод, без бизнес-логики
```

| Слой | Назначение | Ключевые компоненты |
|------|------------|---------------------|
| **models** | Доменные сущности | `User`, `Ticket`, `TicketStatus` |
| **repositories** | Хранение данных в памяти | `UserRepository`, `TicketRepository` |
| **services** | Бизнес-логика | `UserService`, `TicketService`, `ApplicationService` |
| **interface** | Представление | `ConsoleInterface` |
| **exceptions** | Обработка ошибок | `AppError`, `ValidationError`, `NotFoundError`, `DuplicateError` |
| **utils** | Вспомогательные функции | `validators` |

**Поток данных при создании заявки:**

1. `ConsoleInterface` вызывает `TicketService.create_ticket()`.
2. `TicketService` проверяет заголовок и описание (`validators.is_not_empty`).
3. `TicketService` вызывает `UserService.get_user()` — проверка существования пользователя.
4. При успехе `TicketRepository.add()` сохраняет заявку.
5. При ошибке выбрасывается типизированное исключение (`ValidationError` / `NotFoundError`), перехватываемое в `ConsoleInterface`.

---

## 2. UML-диаграмма

Актуальная диаграмма классов находится в файле [`docs/uml.puml`](uml.puml).

Для просмотра используйте PlantUML для `.puml` файлов.

**Основные связи на диаграмме:**

- `ApplicationService` создаёт репозитории и сервисы.
- `TicketService` использует `UserService` для проверки пользователя при создании заявки.
- `ConsoleInterface` обращается к сервисам и обрабатывает `AppError`.
- `Ticket` связан с `User` через поле `created_by_user_id`.

---

## 3. Результаты инспектирования

### 3.1. Понятность имён классов, методов и переменных

- Имена классов отражают роль: `UserService`, `TicketRepository`, `ConsoleInterface`.
- Методы названы по действию: `create_user`, `create_ticket`, `list_active_users`, `change_status`.
- Поля моделей понятны: `full_name`, `created_by_user_id`, `is_active`.
- Приватные атрибуты сервисов помечены `_` (`_user_repository`, `_ticket_service`).

---

### 3.2. Разделение ответственности 

| Компонент | Ответственность | Соблюдение |
|-----------|-----------------|------------|
| `UserRepository` / `TicketRepository` | Только CRUD в памяти | ✓ |
| `UserService` / `TicketService` | Бизнес-правила и валидация | ✓ |
| `ApplicationService` | Сборка зависимостей (DI) | ✓ |
| `ConsoleInterface` | Ввод/вывод, демо-сценарий | ✓ |
| `validators` | Переиспользуемые проверки | ✓ |

### 3.3. Отсутствие дублирования логики
- Валидация email и пустых строк вынесена в `validators.py`.
- Проверка «объект не найден» следует единому шаблону во всех сервисах.

### 3.4. Читаемость и сопровождаемость
- Плоская структура каталогов, легко найти нужный слой.
- `ApplicationService` централизует создание зависимостей — изменение связей в одном месте.
- 16 автотестов покрывают модульные и интеграционные сценарии.
- UML-диаграмма актуализирована после интеграции.

## 4. Описание внесённых исправлений (все этапы)

### Этап 1. Интеграция модулей

| Файл | Исправление |
|------|-------------|
| `ticket_service.py` | Добавлена зависимость от `UserService`; вызов `get_user()` перед созданием заявки |
| `application_service.py` | Передача `user_service` в конструктор `TicketService` |
| `ticket_repository.py` | Исправлена фильтрация `list_by_user_id`; исправлен `update_status` |
| `user_service.py` | Исправлен `list_active_users` — фильтрация по `is_active` |
| `validators.py` | Добавлена проверка пустой локальной части email |

### Этап 2. Тестовые сценарии

| Файл | Исправление |
|------|-------------|
| `tests/test_integration.py` | Добавлено 7 интеграционных тестов |
| `tests/test_ticket_service_expected_behavior.py` | Обновлена инициализация `TicketService` с `UserService` |
| `tests/test_additional_expected_behavior.py` | Обновлена инициализация для интеграции |

## 5. Проверка после инспектирования

```bash
cd requests
python -m pytest -v               # 16 passed
cd src
python -m app.main      # демо работает
```

| Проверка | Результат |
|----------|-----------|
| Автотесты | ✓ 16/16 |
| Консольное приложение | ✓ Работает |

---

## 6. Заключение

Все работает)
