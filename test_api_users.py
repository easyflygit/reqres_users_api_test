import requests
import pytest

BASE_URL = "https://reqres.in/api"

# Позитивные тесты


def test_get_users():
    """Позитивный тест на получение списка всех пользователей"""
    # Отправка GET-запроса к эндпоинту '/users'
    response = requests.get(f"{BASE_URL}/users")

    # Проверка, что статус-код ответа равен 200
    assert response.status_code == 200

    # Получение данных из ответа
    data = response.json()

    # Проверяем, что в словаре data присутствует ключ 'data'
    assert "data" in data

    # Проверяем, что значение по ключу 'data' является списком
    assert isinstance(data["data"], list)

    # Проверяем, что список пользователей не пустой
    if len(data["data"]) > 0:
        assert "id" in data["data"][0]
        assert "email" in data["data"][0]
        assert "first_name" in data["data"][0]
        assert "last_name" in data["data"][0]
        assert "avatar" in data["data"][0]


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_by_id(user_id):
    """Позитивный тест на получение пользователя по ID"""
    # Отправка GET-запроса к эндпоинту '/users/{user_id}'
    response = requests.get(f"{BASE_URL}/users/{user_id}")

    # Проверка, что статус-код ответа равен 200
    assert response.status_code == 200

    # Получение данных из ответа
    data = response.json()
    assert "data" in data
    user_data = data["data"]

    # Проверка структуры ответа
    assert isinstance(user_data["id"], int)
    assert isinstance(user_data["email"], str)
    assert isinstance(user_data["first_name"], str)
    assert isinstance(user_data["last_name"], str)
    assert isinstance(user_data["avatar"], str)


def test_post_create_user():
    """Позитивный тест на создание нового пользователя"""
    payload = {
        "email": "jane.wattson@reqres.in",
        "first_name": "Jane",
        "last_name": "Wattson",
        "avatar": "https://reqres.in/img/faces/13-image.jpg"
    }

    # Отправка POST-запроса к эндпоинту '/users'
    response = requests.post(f"{BASE_URL}/users", json=payload)

    # Проверка, что статус-код ответа равен 201
    assert response.status_code == 201

    # Получение данных из ответа
    data = response.json()

    # Проверка наличия полей в ответе
    assert "email" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "avatar" in data

    # Проверка, что значения полей в ответе совпадают с отправленными данными
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["avatar"] == payload["avatar"]

    # Дополнительно можно проверить, что возвращаемый объект содержит уникальный идентификатор и дату создания
    assert "id" in data
    assert "createdAt" in data


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_put_update_user(user_id):
    """Позитивный тест на обновление данных существующего пользователя"""
    payload = {
        "id": 2,
        "email": "janetta.weaver@reqres.in",
        "first_name": "Janetta",
        "last_name": "Weaverton",
        "avatar": "https://reqres.in/img/faces/2-image.jpg"
    }

    # Отправка PUT-запроса к эндпоинту '/users/{user_id}'
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)

    # Проверка, что статус-код ответа равен 200
    assert response.status_code == 200

    # Получение данных из ответа
    data = response.json()

    # Проверка наличия полей в ответе
    assert "id" in data
    assert "email" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "avatar" in data

    # Проверка, что значения полей в ответе совпадают с отправленными данными
    assert data["id"] == payload["id"]
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["avatar"] == payload["avatar"]


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_delete_user(user_id):
    """Позитивный тест на проверку удаления пользователя"""
    # Отправка DELETE-запроса к эндпоинту '/users/{user_id}'
    response = requests.delete(f"{BASE_URL}/users/{user_id}")

    # Проверка, что статус-код ответа равен 204
    assert response.status_code == 204

# Негативные тесты


@pytest.mark.parametrize("user_id", [9999, 10999, 336688])
def test_get_user_not_found(user_id):
    """Негативный тест на запрос несуществующего пользователя"""
    # Отправка GET-запроса к эндпоинту '/users/{user_id}'
    response = requests.get(f"{BASE_URL}/users/{user_id}")

    # Проверка, что статус-код ответа равен 404
    assert response.status_code == 404


def test_post_create_user_invalid_data():
    """Негативный тест на создание пользователя с некорректными данными.
    Внимание: API reqres.in не выполняет строгую валидацию данных и возвращает статус 201
    даже при некорректных данных. Этот тест предназначен для проверки фактического поведения
    API, а не для проверки валидации данных.
    """
    payload = {
            "email": 555,  # согласно документации поле ожидает string
            "first_name": 111,  # согласно документации поле ожидает string
            "last_name": 368,  # согласно документации поле ожидает string
            "avatar": [1, '2', 3]  # согласно документации поле ожидает string
        }

    # Отправка POST-запроса к эндпоинту '/users'
    response = requests.post(f"{BASE_URL}/users", json=payload)

    # Проверяем, что статус-код ответа равен 201
    assert response.status_code == 201  # API не валидирует данные, возвращает 201

    # Дополнительные проверки
    data = response.json()
    assert "id" in data
    assert "createdAt" in data


@pytest.mark.parametrize("user_id", [9999, 10000, 12345])
def test_put_updated_user_not_found(user_id):
    """Негативный тест на обновление данных несуществующего пользователя."""
    payload = {
        "email": "nonexistent@reqres.in",
        "first_name": "Ghost",
        "last_name": "User",
        "avatar": "https://reqres.in/img/faces/nonexistent-image.jpg"
    }
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)

    # Проверяем, что статус-код ответа равен 200
    assert response.status_code == 200  # API может возвращать 200, даже если пользователь не существует

    data = response.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["avatar"] == payload["avatar"]


@pytest.mark.parametrize("user_id", [9999, 10999, 336688])
def test_delete_user_not_found(user_id):
    """Негативный тест на проверку удаления несуществующего пользователя.
    Важно: API reqres.in возвращает статус 204, даже если пользователь не существует.
    """
    response = requests.delete(f"{BASE_URL}/users/{user_id}")

    # Проверяем, что статус-код ответа равен 204 (No Content)
    assert response.status_code == 204  # API возвращает 204, даже если пользователь не существует