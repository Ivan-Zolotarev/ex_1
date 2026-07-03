"""Интеграционные тесты модулей «Пользователи» и «Заявки»."""

import pytest

from app.exceptions.app_exceptions import NotFoundError, ValidationError
from app.models.ticket_status import TicketStatus
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.services.application_service import ApplicationService
from app.services.ticket_service import TicketService
from app.services.user_service import UserService


def _create_integrated_services() -> tuple[UserService, TicketService]:
    user_repository = UserRepository()
    user_service = UserService(user_repository)
    ticket_service = TicketService(TicketRepository(), user_service)
    return user_service, ticket_service


def test_integration_create_ticket_for_existing_user():
    """Успешное создание заявки существующим пользователем."""
    user_service, ticket_service = _create_integrated_services()
    user = user_service.create_user("Анна Смирнова", "anna@example.com")

    ticket = ticket_service.create_ticket(
        title="Не работает принтер",
        description="Принтер в офисе не печатает документы.",
        created_by_user_id=user.id,
    )

    assert ticket.created_by_user_id == user.id
    assert ticket.status == TicketStatus.OPEN


def test_integration_reject_ticket_for_nonexistent_user():
    """Запрет создания заявки для несуществующего пользователя."""
    _, ticket_service = _create_integrated_services()

    with pytest.raises(NotFoundError, match="Пользователь с ID 404 не найден"):
        ticket_service.create_ticket(
            title="Ошибка системы",
            description="Описание заявки.",
            created_by_user_id=404,
        )


def test_integration_list_user_tickets_returns_only_user_tickets():
    """Получение заявок конкретного пользователя."""
    user_service, ticket_service = _create_integrated_services()
    user_a = user_service.create_user("Пользователь A", "user_a@example.com")
    user_b = user_service.create_user("Пользователь B", "user_b@example.com")

    ticket_service.create_ticket("Заявка A1", "Описание A1", created_by_user_id=user_a.id)
    ticket_service.create_ticket("Заявка A2", "Описание A2", created_by_user_id=user_a.id)
    ticket_service.create_ticket("Заявка B1", "Описание B1", created_by_user_id=user_b.id)

    user_a_tickets = ticket_service.list_user_tickets(user_a.id)

    assert len(user_a_tickets) == 2
    assert all(ticket.created_by_user_id == user_a.id for ticket in user_a_tickets)


def test_integration_change_ticket_status_for_existing_user_ticket():
    """Изменение статуса заявки существующего пользователя."""
    user_service, ticket_service = _create_integrated_services()
    user = user_service.create_user("Сергей Иванов", "sergey@example.com")
    ticket = ticket_service.create_ticket(
        title="Сбой авторизации",
        description="Не удается войти в систему.",
        created_by_user_id=user.id,
    )

    updated_ticket = ticket_service.change_status(ticket.id, TicketStatus.IN_PROGRESS)

    assert updated_ticket.status == TicketStatus.IN_PROGRESS
    assert ticket_service.get_ticket(ticket.id).status == TicketStatus.IN_PROGRESS


def test_integration_create_ticket_with_empty_description_raises_error():
    """Ошибочный сценарий: пустое описание заявки при существующем пользователе."""
    user_service, ticket_service = _create_integrated_services()
    user = user_service.create_user("Мария Кузнецова", "maria@example.com")

    with pytest.raises(ValidationError, match="Описание заявки не может быть пустым"):
        ticket_service.create_ticket(
            title="Заявка без описания",
            description="   ",
            created_by_user_id=user.id,
        )

def test_integration_change_status_for_unknown_ticket_raises_error():
    """Ошибочный сценарий: смена статуса несуществующей заявки."""
    user_service, ticket_service = _create_integrated_services()
    user_service.create_user("Test User", "test@example.com")

    with pytest.raises(NotFoundError, match="Заявка с ID 999 не найдена"):
        ticket_service.change_status(999, TicketStatus.CLOSED)
