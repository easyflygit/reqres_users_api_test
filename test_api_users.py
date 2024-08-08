import requests

BASE_URL = "https://reqres.in/api"


def test_get_users():
    """Тест на получение списка всех пользователей"""
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    if len(data["data"]) > 0:
        assert "id" in data["data"][0]
        assert "email" in data["data"][0]
        assert "first_name" in data["data"][0]
        assert "last_name" in data["data"][0]
        assert "avatar" in data["data"][0]


def test_get_user_by_id():
    """Тест на получение пользователя с заданным id, например 'id=2'"""
    user_id = 2
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    user_data = data["data"]

    # Проверяем, что id в данных ответа соответствует ожидаемому
    assert "id" in user_data
    assert user_data["id"] == user_id

    # Проверяем наличие остальных полей
    assert "email" in user_data
    assert "first_name" in user_data
    assert "last_name" in user_data
    assert "avatar" in user_data
