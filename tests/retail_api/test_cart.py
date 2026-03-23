import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from retail_api.main import create_app
from retail_api.db.session import SessionLocal
from retail_api.product.models import Product


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def auth_headers(client: TestClient):
    client.post(
        "/api/v1/users/register",
        json={"email": "cartuser@example.com", "password": "secret123"},
    )
    r = client.post(
        "/api/v1/users/login",
        json={"email": "cartuser@example.com", "password": "secret123"},
    )
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_cart_get_without_auth_returns_401(client: TestClient):
    r = client.get("/api/v1/cart")
    assert r.status_code == 401


def test_cart_add_without_auth_returns_401(client: TestClient, db: Session):
    product = Product(
        id=uuid.uuid4().hex,
        name="P1",
        slug="p1",
        price=10.0,
        stock=5,
    )
    db.add(product)
    db.commit()
    r = client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 2},
    )
    assert r.status_code == 401


def test_cart_get_empty(client: TestClient, auth_headers: dict):
    r = client.get("/api/v1/cart", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["items"] == []


def test_cart_add_item(client: TestClient, db: Session, auth_headers: dict):
    product = Product(
        id=uuid.uuid4().hex,
        name="P1",
        slug="p1",
        price=10.0,
        stock=5,
    )
    db.add(product)
    db.commit()
    r = client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 2},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["product_id"] == product.id
    assert r.json()["quantity"] == 2


def test_cart_get_returns_items(client: TestClient, db: Session, auth_headers: dict):
    product = Product(
        id=uuid.uuid4().hex,
        name="P2",
        slug="p2",
        price=5.0,
        stock=10,
    )
    db.add(product)
    db.commit()
    client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 1},
        headers=auth_headers,
    )
    r = client.get("/api/v1/cart", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()["items"]) == 1
    assert r.json()["items"][0]["quantity"] == 1


def test_cart_delete_item(client: TestClient, db: Session, auth_headers: dict):
    product = Product(
        id=uuid.uuid4().hex,
        name="P3",
        slug="p3",
        price=1.0,
        stock=1,
    )
    db.add(product)
    db.commit()
    add_r = client.post(
        "/api/v1/cart/items",
        json={"product_id": product.id, "quantity": 1},
        headers=auth_headers,
    )
    item_id = add_r.json()["id"]
    r = client.delete(
        f"/api/v1/cart/items/{item_id}",
        headers=auth_headers,
    )
    assert r.status_code == 200
    get_r = client.get("/api/v1/cart", headers=auth_headers)
    assert get_r.json()["items"] == []
