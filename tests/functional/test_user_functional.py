import pytest
from app import create_app
from app.services import user_services


@pytest.fixture
def client():
    app = create_app()
    user_services.users.clear()
    user_services.current_id = 1
    return app.test_client()


def test_user_full_flow(client):
    response = client.post("/users", json={"name": "Carlos Flow", "email": "carlos@gmail.com"})
    assert response.status_code == 201
    user_id = response.get_json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

    response = client.put(
        f"/users/{user_id}",
        json={"name": "Carlos Flow Updated", "email": "carlos_up@gmail.com"},
    )
    assert response.status_code == 200
    assert response.get_json()["name"] == "Carlos Flow Updated"
    assert response.get_json()["email"] == "carlos_up@gmail.com"

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_list_users(client):
    client.post("/users", json={"name": "Joao", "email": "joao@gmail.com"})
    client.post("/users", json={"name": "Maria", "email": "maria@gmail.com"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_create_and_list_three_users(client):
    client.post("/users", json={"name": "Joao", "email": "joao@gmail.com"})
    client.post("/users", json={"name": "Maria", "email": "maria@gmail.com"})
    client.post("/users", json={"name": "Jose", "email": "jose@gmail.com"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_should_return_400_when_user_already_exists(client):
    client.post("/users", json={"name": "Joao", "email": "joao@gmail.com"})
    response = client.post("/users", json={"name": "Joao2", "email": "joao@gmail.com"})
    assert response.status_code == 400


def test_functional_register_same_email_fails(client):
    resp1 = client.post("/users", json={"name": "Ana", "email": "ana@gmail.com"})
    assert resp1.status_code == 201
    resp2 = client.post("/users", json={"name": "Ana2", "email": "ana@gmail.com"})
    assert resp2.status_code == 400


def test_functional_update_name_and_email(client):
    resp1 = client.post("/users", json={"name": "Paula Velha", "email": "paula@gmail.com"})
    user_id = resp1.get_json()["id"]

    resp2 = client.put(
        f"/users/{user_id}", json={"name": "Paula Nova", "email": "paula_nova@gmail.com"}
    )
    assert resp2.status_code == 200

    resp3 = client.get(f"/users/{user_id}")
    assert resp3.get_json()["name"] == "Paula Nova"
    assert resp3.get_json()["email"] == "paula_nova@gmail.com"


def test_functional_delete_all_users_sequentially(client):
    client.post("/users", json={"name": "Joao", "email": "joao@gmail.com"})
    client.post("/users", json={"name": "Maria", "email": "maria@gmail.com"})

    users = client.get("/users").get_json()
    assert len(users) == 2

    for u in users:
        client.delete(f"/users/{u['id']}")

    users_after = client.get("/users").get_json()
    assert len(users_after) == 0
