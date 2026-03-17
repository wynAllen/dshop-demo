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


def test_product_list_empty(client: TestClient):
    r = client.get("/api/v1/products")
    assert r.status_code == 200
    body = r.json()
    assert body["items"] == []
    assert body["total"] == 0
    assert "page" in body


def test_product_list_pagination(client: TestClient, db: Session):
    for i in range(3):
        p = Product(
            id=uuid.uuid4().hex,
            name=f"Product {i}",
            slug=f"product-{i}",
            price=10.0 + i,
            stock=100,
        )
        db.add(p)
    db.commit()
    r = client.get("/api/v1/products?page=1&page_size=2")
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) == 2
    assert body["total"] == 3
    assert body["page"] == 1


def test_product_detail_returns_200(client: TestClient, db: Session):
    product = Product(
        id=uuid.uuid4().hex,
        name="Test Product",
        slug="test-product",
        price=99.99,
        stock=5,
    )
    db.add(product)
    db.commit()
    r = client.get(f"/api/v1/products/{product.id}")
    assert r.status_code == 200
    assert r.json()["name"] == "Test Product"
    assert r.json()["price"] == 99.99


def test_product_detail_not_found_returns_404(client: TestClient):
    r = client.get("/api/v1/products/nonexistent-id")
    assert r.status_code == 404
    assert r.json().get("code") == "NOT_FOUND"
