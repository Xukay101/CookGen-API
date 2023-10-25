import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope='session')
def client() -> TestClient:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope='session')
def token(client: TestClient) -> str:
    response = client.post('/auth/login', data={'username': 'admin', 'password': 'admin'})
    return response.json()['access_token']