import asyncio
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


async def run_worker():
    if not settings.kafka_enabled:
        logger.warning("KAFKA_ENABLED=false")
        return

    logger.info("Starting Kafka consumer worker...")

    loop = asyncio.get_event_loop()

    from app.worker.kafka_consumer import KafkaConsumerLoop
    consumer_loop = KafkaConsumerLoop()

    try:
        await loop.run_in_executor(None, consumer_loop.start)
    except asyncio.CancelledError:
        logger.info("Worker task cancelled, shutting down consumer...")
        consumer_loop.stop()
    except Exception as e:
        logger.error(f"Worker crashed: {e}", exc_info=True)
        consumer_loop.stop()
        raise