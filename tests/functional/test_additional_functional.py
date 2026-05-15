import pytest
from app import create_app
from app.services import user_services


@pytest.fixture
def client():
    app = create_app()
    user_services.users.clear()
    user_services.current_id = 1
    return app.test_client()


def test_flow_create_update_verify_age(client):
    client.post("/users", json={"name": "Flow User", "email": "flow@test.com", "age": 30})
    client.put("/users/1", json={"age": 35})
    response = client.get("/users/1")
    assert response.get_json()["age"] == 35


def test_flow_create_multiple_and_filter(client):
    client.post("/users", json={"name": "Marcos", "email": "marcos@test.com"})
    client.post("/users", json={"name": "Maria", "email": "maria@test.com"})
    client.post("/users", json={"name": "Joao", "email": "joao@test.com"})
    response = client.get("/users?name=Ma")
    assert len(response.get_json()) == 2


def test_flow_invalid_age_not_added(client):
    client.post("/users", json={"name": "Ghost", "email": "ghost@test.com", "age": -1})
    response = client.get("/users")
    assert len(response.get_json()) == 0
