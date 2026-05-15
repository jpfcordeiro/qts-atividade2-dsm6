import pytest
from app import create_app


from app.services import user_services


@pytest.fixture
def client():
    app = create_app()
    user_services.users.clear()
    user_services.current_id = 1
    return app.test_client()


def test_create_user_success(client):
    response = client.post("/users", json={"name": "Joao Silva", "email": "joao.silva@gmail.com"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Joao Silva"


def test_create_user_missing_name(client):
    response = client.post("/users", json={"email": "u1@test.com"})
    assert response.status_code == 400
    assert "Dados inválidos" in response.get_json()["message"]
    response = client.get("/users")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_user(client):
    client.post("/users", json={"name": "Maria Oliveira", "email": "maria@gmail.com"})
    response = client.get("/users/1")
    assert response.status_code == 200


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "Usuário não encontrado" in response.get_json()["message"]


def test_delete_user(client):
    client.post("/users", json={"name": "Jose Santos", "email": "jose@gmail.com"})
    response = client.delete("/users/1")
    assert response.status_code == 204


def test_update_user_success(client):
    response = client.post("/users", json={"name": "Carlos Souza", "email": "carlos@gmail.com"})
    assert response.status_code == 201

    user_id = response.get_json()["id"]

    response = client.put(
        f"/users/{user_id}", json={"name": "Carlos Souza Updated", "email": "carlos2@gmail.com"}
    )
    assert response.status_code == 200
    assert response.get_json()["name"] == "Carlos Souza Updated"
