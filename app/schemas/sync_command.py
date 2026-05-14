from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class SyncCommand(BaseModel):
    id: UUID
    codigo: str
    viajeroId: UUID
    habitacionId: UUID
    fechaCheckIn: datetime
    fechaCheckOut: datetime
    numHuespedes: int
    estado: str
    subtotal: Decimal
    impuestos: Decimal
    total: Decimal
    moneda: str