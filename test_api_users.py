import requests

BASE_URL = "https://reqres.in/api"


def test_get_users():
    """Тест на получение списка всех пользователей"""
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


def test_get_user_by_id():
    """Тест на получение пользователя по-конкретному id, например 'id=2'"""
    user_id = 2
    response = requests.get(f"{BASE_URL}/users/{user_id}")

    # Проверка, что статус-код ответа равен 200
    assert response.status_code == 200

    # Получение данных из ответа
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


def test_post_create_user():
    """Тест на создание нового пользователя"""
    payload = {
        "email": "jane.wattson@reqres.in",
        "first_name": "Jane",
        "last_name": "Wattson",
        "avatar": "https://reqres.in/img/faces/13-image.jpg"
    }
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


def test_put_update_user():
    """Тест на обновление данных существующего пользователя"""
    user_id = 2
    payload = {
        "id": 2,
        "email": "janetta.weaver@reqres.in",
        "first_name": "Janetta",
        "last_name": "Weaverton",
        "avatar": "https://reqres.in/img/faces/2-image.jpg"
    }

    # Отправка PUT-запрос к эндпоинту '/users/{user_id}'
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


def test_delete_user():
    """Тест на проверку удаления пользователя"""
    user_id = 2
    response = requests.delete(f"{BASE_URL}/users/{user_id}")

    # Проверка, что статус-код ответа равен 204
    assert response.status_code == 204
