import pytest
from app import create_app
from app.services import user_services


@pytest.fixture
def client():
    app = create_app()
    user_services.users.clear()
    user_services.current_id = 1
    return app.test_client()


def test_api_create_user_with_age_success(client):
    response = client.post(
        "/users", json={"name": "Joao Integracao", "email": "joao@gmail.com", "age": 25}
    )
    assert response.status_code == 201
    assert response.get_json()["age"] == 25


def test_api_create_user_with_invalid_age_fails(client):
    response = client.post(
        "/users", json={"name": "Maria Erro", "email": "maria@gmail.com", "age": 150}
    )
    assert response.status_code == 400


def test_api_filter_users_by_name(client):
    client.post("/users", json={"name": "Alice Maria", "email": "alice@gmail.com"})
    client.post("/users", json={"name": "Bruno Silva", "email": "bruno@gmail.com"})

    response = client.get("/users?name=Alice")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Alice Maria"


def test_api_update_user_age(client):
    resp = client.post("/users", json={"name": "Jose Update", "email": "jose@gmail.com", "age": 20})
    user_id = resp.get_json()["id"]

    update_resp = client.put(f"/users/{user_id}", json={"age": 21})
    assert update_resp.status_code == 200
    assert update_resp.get_json()["age"] == 21


def test_api_get_users_contains_age(client):
    client.post("/users", json={"name": "Ana Idade", "email": "ana@gmail.com", "age": 40})
    response = client.get("/users")
    assert response.status_code == 200
    data = response.get_json()
    assert "age" in data[0]
    assert data[0]["age"] == 40
