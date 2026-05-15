import logging
import uuid
from datetime import datetime, timezone

import httpx

from app.config import get_settings
from app.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenError,
)

logger = logging.getLogger(__name__)

settings = get_settings()


class PaymentClient:
    def __init__(self):
        self.base_url = settings.payments_service_url
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=settings.cb_failure_threshold,
            recovery_timeout=settings.cb_recovery_timeout,
            name="payment-service",
        )

    def send_refund_webhook(
        self,
        invoice_id: str
    ):
        payload = {
            "status": "REFUNDED",
            "message": "Devolución",
            "invoiceId": invoice_id,
            "amount": 0,
            "currency": "EUR",
            "cardHolder": "*",
            "maskedCard": "*",
            "transactionId": str(uuid.uuid4()),
            "processedAt": datetime.now(timezone.utc).isoformat(),
        }

        self._send(payload)

    def _send(self, payload: dict):
        def _do_request():
            with httpx.Client(timeout=5.0) as client:
                response = client.post(
                    f"{self.base_url}/api/v1/payment-webhook",
                    json=payload,
                )
                response.raise_for_status()
                return response

        try:
            self.circuit_breaker.call(_do_request)

            logger.info(
                f"Payment webhook sent successfully: "
                f"invoiceId={payload.get('invoiceId')}, "
                f"transactionId={payload.get('transactionId')}"
            )

        except CircuitBreakerOpenError:
            logger.warning(
                f"Payment service circuit breaker is OPEN. "
                f"Skipping webhook for invoice {payload.get('invoiceId')}"
            )
            raise

        except Exception as e:
            logger.warning(
                f"Failed to send payment webhook "
                f"(invoiceId={payload.get('invoiceId')}): {e}"
            )
            raise