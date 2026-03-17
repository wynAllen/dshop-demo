import pytest
from fastapi.testclient import TestClient

from retail_api.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_register_returns_201_and_user(client: TestClient):
    r = client.post(
        "/api/v1/users/register",
        json={"email": "u@example.com", "password": "secret123"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "u@example.com"
    assert "id" in body
    assert "password" not in str(body)


def test_register_duplicate_email_returns_409(client: TestClient):
    client.post(
        "/api/v1/users/register",
        json={"email": "u@example.com", "password": "secret123"},
    )
    r = client.post(
        "/api/v1/users/register",
        json={"email": "u@example.com", "password": "other"},
    )
    assert r.status_code == 409
    assert r.json().get("code") == "CONFLICT"


def test_login_returns_token(client: TestClient):
    client.post(
        "/api/v1/users/register",
        json={"email": "u@example.com", "password": "secret123"},
    )
    r = client.post(
        "/api/v1/users/login",
        json={"email": "u@example.com", "password": "secret123"},
    )
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert body.get("token_type") == "bearer"


def test_login_invalid_returns_401(client: TestClient):
    r = client.post(
        "/api/v1/users/login",
        json={"email": "u@example.com", "password": "wrong"},
    )
    assert r.status_code == 401


def test_me_without_token_returns_401(client: TestClient):
    r = client.get("/api/v1/users/me")
    assert r.status_code == 401


def test_me_with_valid_token_returns_user(client: TestClient):
    client.post(
        "/api/v1/users/register",
        json={"email": "u@example.com", "password": "secret123"},
    )
    login = client.post(
        "/api/v1/users/login",
        json={"email": "u@example.com", "password": "secret123"},
    )
    token = login.json()["access_token"]
    r = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["email"] == "u@example.com"
