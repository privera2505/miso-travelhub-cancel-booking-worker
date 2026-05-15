import logging
from sqlalchemy.orm import Session

from app.models.reserva import Reserva
from app.schemas.sync_command import SyncCommand

logger = logging.getLogger(__name__)


class ReservaService:
    def __init__(self, db: Session):
        self.db = db

    def _find(self, reserva_id) -> Reserva | None:
        return (
            self.db.query(Reserva)
            .filter(Reserva.id == str(reserva_id))
            .first()
        )

    def marcar_reembolsada(self, command: SyncCommand):
        reserva = self._find(command.id)

        if not reserva:
            logger.warning(f"Reserva {command.id} no encontrada")
            return None

        if reserva.estado == "REEMBOLSADA":
            logger.info(f"Reserva {reserva.id} ya estaba reembolsada")
            return reserva

        reserva.estado = "REEMBOLSADA"

        self.db.commit()
        self.db.refresh(reserva)

        logger.info(f"Reserva {reserva.id} marcada como REEMBOLSADO")

        return reserva