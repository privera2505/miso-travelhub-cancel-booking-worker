import uuid

from app.services.cancel_service import ReservaService
from app.schemas.sync_command import SyncCommand


def make_command(reserva):
    return SyncCommand(
        event_id=str(uuid.uuid4()),
        event_type="refund_reserva",
        retry_count=0,

        id=reserva.id,
        codigo=reserva.codigo,
        viajeroId=reserva.viajeroId,
        habitacionId=reserva.habitacionId,
        fechaCheckIn=reserva.fechaCheckIn,
        fechaCheckOut=reserva.fechaCheckOut,
        numHuespedes=reserva.numHuespedes,
        estado=reserva.estado,
        subtotal=reserva.subtotal,
        impuestos=reserva.impuestos,
        total=reserva.total,
        moneda=reserva.moneda,
    )


def test_marcar_reembolsada_updates_estado(db, reserva):
    service = ReservaService(db)

    command = make_command(reserva)

    updated = service.marcar_reembolsada(command)

    db.refresh(reserva)

    assert updated is not None
    assert reserva.estado == "REEMBOLSADA"


def test_marcar_reembolsada_returns_same_when_already_refunded(
    db,
    reserva,
):
    reserva.estado = "REEMBOLSADA"
    db.commit()

    service = ReservaService(db)

    command = make_command(reserva)

    updated = service.marcar_reembolsada(command)

    assert updated is not None
    assert updated.estado == "REEMBOLSADA"


def test_marcar_reembolsada_returns_none_when_reserva_not_found(db):
    service = ReservaService(db)

    command = SyncCommand(
        event_id=str(uuid.uuid4()),
        event_type="refund_reserva",
        retry_count=0,

        id=str(uuid.uuid4()),
        codigo="NOT-FOUND",
        viajeroId=str(uuid.uuid4()),
        habitacionId=str(uuid.uuid4()),
        fechaCheckIn="2025-01-01T00:00:00Z",
        fechaCheckOut="2025-01-02T00:00:00Z",
        numHuespedes=1,
        estado="CONFIRMADA",
        subtotal=100,
        impuestos=19,
        total=119,
        moneda="EUR",
    )

    result = service.marcar_reembolsada(command)

    assert result is None