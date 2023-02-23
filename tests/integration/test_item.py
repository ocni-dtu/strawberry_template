from fastapi.testclient import TestClient

from core.config import settings


def test_item_query(client: TestClient, items):
    query = """
        query {
            items {
                id
                name
            }
        }
    """

    response = client.post(
        f"{settings.API_STR}/graphql",
        json={
            "query": query,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert not data.get("errors")
    assert data.get("data", {}).get("items")


def test_item_mutation(client: TestClient):
    query = """
        mutation($name: String!) {
            addItem(name: $name) {
                id
                name
            }
        }
    """

    response = client.post(
        f"{settings.API_STR}/graphql",
        json={"query": query, "variables": {"name": "My Item"}},
    )

    assert response.status_code == 200
    data = response.json()

    assert not data.get("errors")
    assert data.get("data", {}).get("addItem")
    assert data["data"]["addItem"]["name"] == "My Item"
