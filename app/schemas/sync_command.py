from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class SyncCommand(BaseModel):
    id: UUID
    codigo: str
    viajeroId: str
    habitacionId: str
    fechaCheckIn: datetime
    fechaCheckOut: datetime
    numHuespedes: int
    estado: str
    subtotal: Decimal
    impuestos: Decimal
    total: Decimal
    moneda: str

    retry_count: int = 0