from fastapi.testclient import TestClient

from core.config import settings


def test_app(client: TestClient):
    response = client.get(f"{settings.API_STR}/graphql")

    assert response.status_code == 200
