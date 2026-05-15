import uuid
from unittest.mock import patch

from app.schemas.sync_command import SyncCommand
from app.worker.command_handler import CommandHandler
from app.models.reserva import Reserva


def make_command(reserva):
    return SyncCommand(
        event_id=str(uuid.uuid4()),
        event_type="refund_reserva",
        retry_count=0,

        id=str(reserva.id),
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


def test_command_handler_marks_reserva_as_refunded_and_calls_payment(
    db,
    reserva,
):
    command = make_command(reserva)

    with patch(
        "app.worker.command_handler.PaymentClient"
    ) as mock_payment_client_class:

        mock_payment_client = mock_payment_client_class.return_value

        handler = CommandHandler(db)

        handler.process(command)

        db.refresh(reserva)

        assert reserva.estado == "REEMBOLSADA"

        mock_payment_client.send_refund_webhook.assert_called_once_with(
            reserva.id
        )


def test_command_handler_raises_when_payment_fails(
    db,
    reserva,
):
    command = make_command(reserva)

    with patch(
        "app.worker.command_handler.PaymentClient"
    ) as mock_payment_client_class:

        mock_payment_client = mock_payment_client_class.return_value

        mock_payment_client.send_refund_webhook.side_effect = Exception(
            "payment service unavailable"
        )

        handler = CommandHandler(db)

        try:
            handler.process(command)
            assert False, "Expected exception was not raised"

        except Exception as e:
            assert "payment service unavailable" in str(e)