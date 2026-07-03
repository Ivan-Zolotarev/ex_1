# Отчёт о тестировании
## 1. Анализ существующих автотестов

До расширения в проекте было **10 автотестов** в трёх файлах:

| Файл | Кол-во | Что проверяется |
|------|--------|-----------------|
| `tests/test_user_service.py` | 3 | Создание пользователя, некорректный email, дублирующий email |
| `tests/test_ticket_service_expected_behavior.py` | 4 | Создание заявки, пустой заголовок, несуществующий пользователь, фильтрация заявок по пользователю |
| `tests/test_additional_expected_behavior.py` | 3 | Пустая локальная часть email, список активных пользователей, смена статуса заявки |

**Вывод:** базовые сценарии модулей покрыты, но отдельного набора интеграционных тестов, проверяющих совместную работу сервисов и `ApplicationService`, не было.

## 2. Добавленные тест-кейсы

Добавлен файл `tests/test_integration.py` с **6 новыми интеграционными тестами**:

| № | Тест | Тип | Сценарий |
|---|------|-----|----------|
| 1 | `test_integration_create_ticket_for_existing_user` | Успех | Создание заявки существующим пользователем |
| 2 | `test_integration_reject_ticket_for_nonexistent_user` | Ошибка | Запрет создания заявки несуществующим пользователем |
| 3 | `test_integration_list_user_tickets_returns_only_user_tickets` | Успех | Получение заявок конкретного пользователя |
| 4 | `test_integration_change_ticket_status_for_existing_user_ticket` | Успех | Изменение статуса заявки |
| 5 | `test_integration_create_ticket_with_empty_description_raises_error` | Ошибка | Валидация описания при существующем пользователе |
| 6 | `test_integration_change_status_for_unknown_ticket_raises_error` | Ошибка | Смена статуса несуществующей заявки |

Покрыты примеры из задания:

- создание заявки существующим пользователем — тест №1;
- запрет создания заявки несуществующим пользователем — тест №2;
- получение заявок конкретного пользователя — тест №3;
- изменение статуса заявки — тест №4;
- создание пользователя с некорректным email — `test_create_user_with_invalid_email_should_raise_error`;
- получение списка активных пользователей — `test_list_active_users_should_not_return_deactivated_users`.

## 3. Команда запуска

```bash
cd requests
python -m pytest -v
```
## 4. Заключение

все работает)
