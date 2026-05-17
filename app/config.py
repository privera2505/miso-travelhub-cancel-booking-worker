from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "postgres"
    database_user: str = "postgres"
    database_password: str = "Postgres1."

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_pms_sync: str = "cancel_booking_queue"
    kafka_consumer_group: str = "cancel-booking-worker-group"
    kafka_enabled: bool = True

    # Notification service
    payments_service_url: str = "https://payments-services-154299161799.us-central1.run.app"

    # Service
    service_name: str = "cancel-booking-worker"
    service_port: int = 8000

    # Retry
    max_retries: int = 3
    retry_backoff_base: int = 2

    # Circuit Breaker
    cb_failure_threshold: int = 5
    cb_recovery_timeout: int = 30

    @property
    def database_url(self) -> str:
        # evita cuelgue de SSL handshake en Cloud Run direct VPC.
        return (
            f"postgresql://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}?sslmode=disable"
        )

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()