import uuid
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Reserva(Base):
    __tablename__ = "reserva"
    __mapper_args__ = {"confirm_deleted_rows": False}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    codigo = Column(String, nullable=False, unique=True)
    viajeroId = Column(String, nullable=False)
    habitacionId = Column(String(36), nullable=False)
    fechaCheckIn = Column(DateTime(timezone=True), nullable=False)
    fechaCheckOut = Column(DateTime(timezone=True), nullable=False)
    numHuespedes = Column(Integer, nullable=False)
    estado = Column(String, nullable=False)
    subtotal = Column(Float, nullable=False)
    impuestos = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    moneda = Column(String, nullable=False)