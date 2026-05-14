import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Crea un cliente de prueba"""
    return TestClient(app)   

def test_heath(client):
    """test unique"""
    assert True == True
