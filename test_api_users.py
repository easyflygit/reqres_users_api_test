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
