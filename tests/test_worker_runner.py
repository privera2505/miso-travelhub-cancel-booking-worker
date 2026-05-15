import asyncio
import json
import uuid
from datetime import date, datetime, timezone
from unittest.mock import patch, MagicMock

import pytest

from app.worker import worker_runner

@pytest.mark.asyncio
async def test_run_worker_starts_kafka_consumer_and_handles_cancel():
    consumer_instance = MagicMock()

    def fake_start():
        import time
        time.sleep(0.5)

    consumer_instance.start.side_effect = fake_start

    with patch.object(worker_runner.settings, "kafka_enabled", True), patch(
        "app.worker.kafka_consumer.KafkaConsumerLoop", return_value=consumer_instance
    ):
        task = asyncio.create_task(worker_runner.run_worker())
        await asyncio.sleep(0.05)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    consumer_instance.stop.assert_called()


@pytest.mark.asyncio
async def test_run_worker_propagates_unexpected_exception():
    consumer_instance = MagicMock()
    consumer_instance.start.side_effect = RuntimeError("boom")

    with patch.object(worker_runner.settings, "kafka_enabled", True), patch(
        "app.worker.kafka_consumer.KafkaConsumerLoop", return_value=consumer_instance
    ):
        with pytest.raises(RuntimeError):
            await worker_runner.run_worker()

    consumer_instance.stop.assert_called()