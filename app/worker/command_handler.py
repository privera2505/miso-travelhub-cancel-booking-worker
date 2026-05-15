import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.schemas.sync_command import SyncCommand

from app.resilience.retry_handler import NonRetryableError
from app.services.cancel_service import ReservaService
from app.services.payments_service import PaymentClient


logger = logging.getLogger(__name__)

class CommandHandler:
    def __init__(self, db: Session):
        self.db = db
        self.reserva_service = ReservaService(db)
        self.payment_client = PaymentClient()

    def process(self, command: SyncCommand) -> None:
        self.reserva_service.marcar_reembolsada(command)
        self.payment_client.send_refund_webhook(
            str(command.id)
        )
