from app.exceptions.app_exceptions import NotFoundError, ValidationError
from app.models.ticket import Ticket
from app.models.ticket_status import TicketStatus
from app.repositories.ticket_repository import TicketRepository
from app.utils.validators import is_not_empty


class TicketService:
    """Сервис заявок.

    Отвечает за бизнес-логику модуля «Заявки».
    """

    def __init__(self, ticket_repository: TicketRepository) -> None:
        self._ticket_repository = ticket_repository

    def create_ticket(self, title: str, description: str, created_by_user_id: int) -> Ticket:
        title = title.strip()
        description = description.strip()

        if not is_not_empty(title):
            raise ValidationError("Заголовок заявки не может быть пустым.")

        if not is_not_empty(description):
            raise ValidationError("Описание заявки не может быть пустым.")

        return self._ticket_repository.add(
            title=title,
            description=description,
            created_by_user_id=created_by_user_id,
        )

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self._ticket_repository.get_by_id(ticket_id)
        if ticket is None:
            raise NotFoundError(f"Заявка с ID {ticket_id} не найдена.")
        return ticket

    def list_tickets(self) -> list[Ticket]:
        return self._ticket_repository.get_all()

    def list_user_tickets(self, user_id: int) -> list[Ticket]:
        return self._ticket_repository.list_by_user_id(user_id)

    def change_status(self, ticket_id: int, status: TicketStatus) -> Ticket:
        ticket = self._ticket_repository.update_status(ticket_id, status)
        if ticket is None:
            raise NotFoundError(f"Заявка с ID {ticket_id} не найдена.")
        return ticket
