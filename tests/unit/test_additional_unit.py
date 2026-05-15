from app.services import user_services


def setup_function():
    user_services.users.clear()
    user_services.current_id = 1


def test_create_user_with_age_success():
    user = user_services.create_user({"name": "Joao Teste", "email": "joao@gmail.com", "age": 25})
    assert user is not None
    assert user.get("age") == 25


def test_create_user_with_invalid_age_too_low_fails():
    user = user_services.create_user({"name": "Maria Nova", "email": "maria@gmail.com", "age": 0})
    assert user is None


def test_create_user_with_invalid_age_too_high_fails():
    user = user_services.create_user({"name": "Jose Velho", "email": "jose@gmail.com", "age": 121})
    assert user is None


def test_create_user_with_non_int_age_fails():
    user = user_services.create_user(
        {"name": "Ana Texto", "email": "ana@gmail.com", "age": "twenty"}
    )
    assert user is None


def test_update_user_age_success():
    user = user_services.create_user(
        {"name": "Carlos Update", "email": "carlos@gmail.com", "age": 30}
    )
    updated = user_services.update_user(user["id"], {"age": 31})
    assert updated is not None
    assert updated["age"] == 31


def test_update_user_invalid_age_fails():
    user = user_services.create_user({"name": "Paula Erro", "email": "paula@gmail.com", "age": 30})
    updated = user_services.update_user(user["id"], {"age": -5})
    assert updated is None


def test_filter_users_by_name_success():
    user_services.create_user({"name": "Bruno Silva", "email": "bruno@gmail.com", "age": 20})
    user_services.create_user({"name": "Luiza Souza", "email": "luiza@gmail.com", "age": 30})
    results = user_services.filter_users_by_name("Bruno")
    assert len(results) == 1
    assert results[0]["name"] == "Bruno Silva"


def test_filter_users_by_name_case_insensitive():
    user_services.create_user(
        {"name": "Fernanda Oliveira", "email": "fernanda@gmail.com", "age": 22}
    )
    results = user_services.filter_users_by_name("FERNANDA")
    assert len(results) == 1


def test_filter_users_by_name_no_match():
    user_services.create_user({"name": "Ricardo Santos", "email": "ricardo@gmail.com", "age": 40})
    results = user_services.filter_users_by_name("Zorro")
    assert len(results) == 0


def test_get_user_by_id_invalid_type():
    user_services.create_user({"name": "Camila Lima", "email": "camila@gmail.com", "age": 18})
    assert user_services.get_user_by_id(999) is None
