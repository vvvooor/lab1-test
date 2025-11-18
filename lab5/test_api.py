import requests


BASE_URL = "https://jsonplaceholder.typicode.com/users"


def test_get_user():
    response = requests.get(f"{BASE_URL}/1")

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    try:
        json_data = response.json()
    except ValueError:
        assert False, "Ответ не является JSON"

    assert "id" in json_data, "Поле 'id' отсутствует"
    assert json_data["id"] == 1, f"ID пользователя должен быть равен 1, получен {json_data['id']}"
    for field in ["name", "username", "email"]:
        assert field in json_data, f"Поле '{field}' отсутствует"

    assert response.elapsed.total_seconds() * 1000 < 1000, f"Слишком долго откликается сервер: {response.elapsed.total_seconds()*1000:.2f}ms"


def test_create_user():
    payload = {
        "name": "Valiko",
        "username": "viiarr",
        "email": "viaeer@example.com"
    }
    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"

    json_data = response.json()

    assert "id" in json_data, "Сервер не вернул поле 'id'"
    assert isinstance(json_data["id"], int), "Поле 'id' должно быть числом"

    for key in ["name", "username", "email"]:
        assert json_data[key] == payload[key], f"{key} в ответе не совпадает с отправленным"

    assert response.elapsed.total_seconds() * 1000 < 1500, f"Медленный ответ при создании: {response.elapsed.total_seconds()*1000:.2f}ms"


def test_update_user():
    payload = {
        "id": 1,
        "name": "Jane Doe",
        "username": "janed",
        "email": "jane@example.com"
    }
    response = requests.put(f"{BASE_URL}/1", json=payload)

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    json_data = response.json()

    for key in ["id", "name", "username", "email"]:
        assert json_data[key] == payload[key], f"{key} не совпадает с отправленным"

    assert response.elapsed.total_seconds() * 1000 < 1200, f"Медленный ответ при обновлении: {response.elapsed.total_seconds()*1000:.2f}ms"