import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_db
from app.services.user_services import get_current_user
from app.services import customer_services
from app.services import film_services

@pytest.fixture(scope="function")
def client():
    def override_get_db():
        yield None

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_client(client):
    def override_get_current_user():
        return {
            "user_id":1
        }

    app.dependency_overrides[get_current_user] = override_get_current_user

    yield client

    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
def mock_customer_service(monkeypatch):
    async def fake_get_customer(customer_id: int, conn):
        return {
            "customer_id": customer_id,
            "customer_first_name": "Mary",
            "customer_last_name": "Smith",
            "customer_email": "mary.smith@example.com",
        }

    monkeypatch.setattr(customer_services, "get_customer", fake_get_customer)

@pytest.fixture
def mock_film_service(monkeypatch):
    async def fake_get_film(film_id:int, conn):
        return {
            "film_id":1,
            "title":"The Terminator",
            "release_year":1984,
            "length":107,
            "rating":"R"
        }
    
    monkeypatch.setattr(film_services,"get_film",fake_get_film)