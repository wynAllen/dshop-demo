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
        json={"email": "orderuser@example.com", "password": "secret123"},
    )
    r = client.post(
        "/api/v1/users/login",
        json={"email": "orderuser@example.com", "password": "secret123"},
    )
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_order_create_success(client: TestClient, db: Session, auth_headers: dict):
    product = Product(
        id=uuid.uuid4().hex,
        name="P",
        slug="p",
        price=10.0,
        stock=5,
    )
    db.add(product)
    db.commit()
    r = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": product.id, "quantity": 2}]},
        headers=auth_headers,
    )
    assert r.status_code == 201
    body = r.json()
    assert body["total_amount"] == 20.0
    assert body["status"] == "pending"
    assert len(body["items"]) == 1
    assert body["items"][0]["quantity"] == 2


def test_order_create_insufficient_stock_returns_409(
    client: TestClient, db: Session, auth_headers: dict
):
    product = Product(
        id=uuid.uuid4().hex,
        name="P2",
        slug="p2",
        price=5.0,
        stock=1,
    )
    db.add(product)
    db.commit()
    r = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": product.id, "quantity": 10}]},
        headers=auth_headers,
    )
    assert r.status_code == 409
    assert r.json().get("code") == "CONFLICT"


def test_order_get_returns_200(client: TestClient, db: Session, auth_headers: dict):
    product = Product(
        id=uuid.uuid4().hex,
        name="P3",
        slug="p3",
        price=1.0,
        stock=3,
    )
    db.add(product)
    db.commit()
    create_r = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": product.id, "quantity": 1}]},
        headers=auth_headers,
    )
    order_id = create_r.json()["id"]
    r = client.get(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["id"] == order_id


def test_order_get_not_found_returns_404(client: TestClient, auth_headers: dict):
    r = client.get(
        "/api/v1/orders/nonexistent-order-id",
        headers=auth_headers,
    )
    assert r.status_code == 404
