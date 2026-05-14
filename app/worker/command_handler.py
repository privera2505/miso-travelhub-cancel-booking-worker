import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.schemas.sync_command import SyncCommand

from app.resilience.retry_handler import NonRetryableError
from app.services.cancel_service import ReservaService


logger = logging.getLogger(__name__)

class CommandHandler:
    def __init__(self, db: Session):
        self.db = db
        self.reserva_service = ReservaService(db)

    def process(self, command: SyncCommand) -> None:
        self.reserva_service.marcar_reembolsada(command)