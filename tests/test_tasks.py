import pytest


@pytest.fixture
def auth_headers(client):
    user = {
        "username": "taskuser",
        "email": "taskuser@example.com",
        "password": "12345678",
        "role": "user"
    }
    client.post("/users", json=user)

    login_res = client.post(
        "/auth/login",
        data={"username": user["email"], "password": user["password"]}
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def category_id(client, auth_headers):
    response = client.post(
        "/categories",
        json={"name": "Тестовая категория"},
        headers=auth_headers
    )
    if response.status_code in (200, 201):
        return response.json()["id"]
    return 1


def test_create_task(client, auth_headers, category_id):
    response = client.post(
        "/tasks",
        json={
            "title": "Тестовая задача",
            "description": "Описание задачи",
            "category_id": category_id,
            "status": "open",
            "priority": "low"
        },
        headers=auth_headers
    )
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data or "message" in data or "title" in data


def test_get_tasks_list(client, auth_headers, category_id):
    client.post(
        "/tasks",
        json={
            "title": "Задача для списка",
            "description": "Desc",
            "category_id": category_id,
            "status": "open",
            "priority": "low"
        },
        headers=auth_headers
    )

    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_create_task_unauthorized(client):
    response = client.post(
        "/tasks",
        json={"title": "Анонимная задача", "description": "Desc"}
    )
    assert response.status_code == 401


def test_get_nonexistent_task(client, auth_headers):
    response = client.get("/tasks/999999", headers=auth_headers)
    assert response.status_code == 404