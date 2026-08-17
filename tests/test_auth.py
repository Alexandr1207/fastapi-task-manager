from fastapi.testclient import TestClient

from app.core.enums import UserRole
from app.main import app

client = TestClient(app)

def test_register_user(client):
    response = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "12345678",
            "role": UserRole.user
        }
    )

    assert response.status_code == 201


def test_login(client):
    user = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "12345678",
        "role": "user"
    }

    response = client.post("/users", json=user)
    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        data={
            "username": user["email"],
            "password": user["password"],
        },
    )

    print("ACTUAL JSON RESPONSE:", response.json())

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user_me(client):
    user = {
        "username": "meuser",
        "email": "me@example.com",
        "password": "12345678",
        "role": "user"
    }
    client.post("/users", json=user)

    login_res = client.post(
        "/auth/login",
        data={"username": user["email"], "password": user["password"]}
    )
    token = login_res.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == user["email"]


def test_login_wrong_password(client):
    user = {
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "12345678",
        "role": "user"
    }
    client.post("/users", json=user)

    response = client.post(
        "/auth/login",
        data={"username": user["email"], "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_get_me_unauthorized(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_register_invalid_email(client):
    response = client.post(
        "/users",
        json={
            "username": "baduser",
            "email": "not-an-email",
            "password": "12345678",
            "role": "user"
        }
    )
    assert response.status_code == 422