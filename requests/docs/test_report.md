# Отчёт о тестировании

**Проект:** Информационная система учёта заявок пользователей  
**Этап:** Разработка тестовых сценариев (интеграция модулей «Пользователи» и «Заявки»)  
**Дата:** 03.07.2026

## 1. Анализ существующих автотестов

До расширения в проекте было **10 автотестов** в трёх файлах:

| Файл | Кол-во | Что проверяется |
|------|--------|-----------------|
| `tests/test_user_service.py` | 3 | Создание пользователя, некорректный email, дублирующий email |
| `tests/test_ticket_service_expected_behavior.py` | 4 | Создание заявки, пустой заголовок, несуществующий пользователь, фильтрация заявок по пользователю |
| `tests/test_additional_expected_behavior.py` | 3 | Пустая локальная часть email, список активных пользователей, смена статуса заявки |

**Вывод:** базовые сценарии модулей покрыты, но отдельного набора интеграционных тестов, проверяющих совместную работу сервисов и `ApplicationService`, не было.

## 2. Добавленные тест-кейсы

Добавлен файл `tests/test_integration.py` с **7 новыми интеграционными тестами**:

| № | Тест | Тип | Сценарий |
|---|------|-----|----------|
| 1 | `test_integration_create_ticket_for_existing_user` | Успех | Создание заявки существующим пользователем |
| 2 | `test_integration_reject_ticket_for_nonexistent_user` | Ошибка | Запрет создания заявки несуществующим пользователем |
| 3 | `test_integration_list_user_tickets_returns_only_user_tickets` | Успех | Получение заявок конкретного пользователя |
| 4 | `test_integration_change_ticket_status_for_existing_user_ticket` | Успех | Изменение статуса заявки |
| 5 | `test_integration_create_ticket_with_empty_description_raises_error` | Ошибка | Валидация описания при существующем пользователе |
| 6 | `test_integration_application_service_wires_modules_correctly` | Успех | Связка модулей через `ApplicationService` |
| 7 | `test_integration_change_status_for_unknown_ticket_raises_error` | Ошибка | Смена статуса несуществующей заявки |

Покрыты примеры из задания:

- создание заявки существующим пользователем — тест №1;
- запрет создания заявки несуществующим пользователем — тест №2;
- получение заявок конкретного пользователя — тест №3;
- изменение статуса заявки — тест №4;
- создание пользователя с некорректным email — `test_create_user_with_invalid_email_should_raise_error`;
- обработка дублирующего email — `test_create_duplicate_user_should_raise_error`;
- получение списка активных пользователей — `test_list_active_users_should_not_return_deactivated_users`.

## 3. Команда запуска

```bash
cd requests
python -m pytest -v
```

## 4. Результаты тестирования

```
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-8.2.2, pluggy-1.6.0
collected 17 items

tests/test_additional_expected_behavior.py::test_create_user_with_empty_email_local_part_should_raise_error PASSED [  5%]
tests/test_additional_expected_behavior.py::test_list_active_users_should_not_return_deactivated_users PASSED [ 11%]
tests/test_additional_expected_behavior.py::test_change_status_should_store_requested_status PASSED [ 17%]
tests/test_integration.py::test_integration_create_ticket_for_existing_user PASSED [ 23%]
tests/test_integration.py::test_integration_reject_ticket_for_nonexistent_user PASSED [ 29%]
tests/test_integration.py::test_integration_list_user_tickets_returns_only_user_tickets PASSED [ 35%]
tests/test_integration.py::test_integration_change_ticket_status_for_existing_user_ticket PASSED [ 41%]
tests/test_integration.py::test_integration_create_ticket_with_empty_description_raises_error PASSED [ 47%]
tests/test_integration.py::test_integration_application_service_wires_modules_correctly PASSED [ 52%]
tests/test_integration.py::test_integration_change_status_for_unknown_ticket_raises_error PASSED [ 58%]
tests/test_ticket_service_expected_behavior.py::test_create_ticket_success PASSED [ 64%]
tests/test_ticket_service_expected_behavior.py::test_create_ticket_with_empty_title_should_raise_error PASSED [ 70%]
tests/test_ticket_service_expected_behavior.py::test_create_ticket_for_unknown_user_should_raise_error PASSED [ 76%]
tests/test_ticket_service_expected_behavior.py::test_list_user_tickets_should_return_only_selected_user_tickets PASSED [ 82%]
tests/test_user_service.py::test_create_user_success PASSED              [ 88%]
tests/test_user_service.py::test_create_user_with_invalid_email_should_raise_error PASSED [ 94%]
tests/test_user_service.py::test_create_duplicate_user_should_raise_error PASSED [100%]

============================= 17 passed in 0.04s ==============================
```

| Показатель | Значение |
|------------|----------|
| Всего тестов | 17 |
| Успешно | 17 |
| Провалено | 0 |
| Новых интеграционных тестов | 7 |

## 5. Заключение

Интеграция модулей «Пользователи» и «Заявки» подтверждена автотестами. Успешные и ошибочные сценарии обрабатываются корректно: заявки создаются только для существующих пользователей, ошибки интеграции (`NotFoundError`, `ValidationError`) возникают с ожидаемыми сообщениями, а `ApplicationService` корректно связывает оба модуля.
