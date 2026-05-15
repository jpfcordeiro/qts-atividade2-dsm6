from app.services import user_services


def setup_function():
    user_services.users.clear()
    user_services.current_id = 1


def test_should_not_allow_duplicate_users():
    user_services.create_user({"name": "Joao", "email": "joao1@gmail.com"})
    user = user_services.create_user({"name": "Joao", "email": "joao2@gmail.com"})
    assert user is None


def test_create_user_with_email_success():
    user = user_services.create_user({"name": "Maria", "email": "maria@gmail.com"})
    assert user is not None
    assert user.get("email") == "maria@gmail.com"


def test_create_user_without_email_fails():
    user = user_services.create_user({"name": "Jose"})
    assert user is None


def test_create_user_invalid_email_fails():
    user = user_services.create_user({"name": "Ana", "email": "ana_no_at.com"})
    assert user is None


def test_create_user_duplicate_email_fails():
    user_services.create_user({"name": "Carlos", "email": "carlos@gmail.com"})
    user = user_services.create_user({"name": "Carlos2", "email": "carlos@gmail.com"})
    assert user is None


def test_get_all_users_empty():
    users = user_services.get_all_users()
    assert len(users) == 0


def test_get_all_users_with_data():
    user_services.create_user({"name": "Paula", "email": "paula@gmail.com"})
    users = user_services.get_all_users()
    assert len(users) == 1


def test_update_user_name_and_email_success():
    user = user_services.create_user({"name": "Bruno", "email": "bruno@gmail.com"})
    updated = user_services.update_user(
        user["id"], {"name": "Bruno Updated", "email": "bruno2@gmail.com"}
    )
    assert updated is not None
    assert updated["name"] == "Bruno Updated"
    assert updated.get("email") == "bruno2@gmail.com"


def test_update_user_with_duplicate_email_fails():
    user_services.create_user({"name": "Luiza", "email": "luiza@gmail.com"})
    user2 = user_services.create_user({"name": "Fernanda", "email": "fernanda@gmail.com"})
    updated = user_services.update_user(
        user2["id"], {"name": "Fernanda", "email": "luiza@gmail.com"}
    )
    assert updated is None


def test_delete_user_success():
    user = user_services.create_user({"name": "Ricardo", "email": "ricardo@gmail.com"})
    user_services.delete_user(user["id"])
    assert len(user_services.get_all_users()) == 0


def test_delete_user_not_found():
    user_services.create_user({"name": "Camila", "email": "camila@gmail.com"})
    user_services.delete_user(999)
    assert len(user_services.get_all_users()) == 1
