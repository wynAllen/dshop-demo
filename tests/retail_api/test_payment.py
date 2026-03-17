import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from retail_api.main import create_app
from retail_api.db.session import SessionLocal
from retail_api.order.models import Order


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


def test_order_pay_returns_pay_url(client: TestClient, db: Session):
    order = Order(
        id=uuid.uuid4().hex,
        user_id="u1",
        total_amount=99.0,
        status="pending",
    )
    db.add(order)
    db.commit()
    r = client.post(f"/api/v1/orders/{order.id}/pay")
    assert r.status_code == 200
    assert "pay_url" in r.json()
    assert order.id in r.json()["pay_url"]


def test_payment_callback_stub_marks_paid(client: TestClient, db: Session):
    order = Order(
        id=uuid.uuid4().hex,
        user_id="u2",
        total_amount=10.0,
        status="pending",
    )
    db.add(order)
    db.commit()
    r = client.post(
        "/api/v1/payment/callback/stub",
        params={"order_id": order.id, "success": True},
    )
    assert r.status_code == 200
    db.refresh(order)
    assert order.status == "paid"
