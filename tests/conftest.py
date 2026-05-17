import uuid
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock

from datetime import datetime, timezone, timedelta

from app.database import Base
from app.models.reserva import Reserva


TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def engine():
    eng = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)


@pytest.fixture(scope="function")
def db(engine):
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSession()
    yield session
    session.close()


@pytest.fixture
def reserva(db):
    r = Reserva(
        id=str(uuid.uuid4()),
        codigo="RES-001",
        viajeroId=str(uuid.uuid4()),
        habitacionId=str(uuid.uuid4()),
        fechaCheckIn=datetime.now(timezone.utc),
        fechaCheckOut=datetime.now(timezone.utc) + timedelta(days=2),
        numHuespedes=2,
        estado="CONFIRMADA",
        subtotal=100.0,
        impuestos=19.0,
        total=119.0,
        moneda="EUR",
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@pytest.fixture
def mock_notification_client():
    client = MagicMock()
    client.notify_conflict = MagicMock()
    client.notify_error = MagicMock()
    client.notify_sync_complete = MagicMock()
    return client