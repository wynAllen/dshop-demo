import uuid

import pytest
from sqlalchemy.orm import Session

from retail_api.db.base import Base
from retail_api.db.session import SessionLocal, engine
from retail_api.product.models import Product
from retail_api.inventory.service import ReserveStock, ReleaseStock


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_reserve_stock_decrements(db: Session):
    product = Product(
        id=uuid.uuid4().hex,
        name="P",
        slug="p",
        price=10.0,
        stock=5,
    )
    db.add(product)
    db.commit()
    price = ReserveStock(db, product.id, 2)
    db.commit()
    assert price == 10.0
    db.refresh(product)
    assert product.stock == 3


def test_reserve_stock_insufficient_raises(db: Session):
    product = Product(
        id=uuid.uuid4().hex,
        name="P2",
        slug="p2",
        price=5.0,
        stock=1,
    )
    db.add(product)
    db.commit()
    from retail_api.common.exceptions import AppException

    with pytest.raises(AppException) as exc_info:
        ReserveStock(db, product.id, 10)
    assert exc_info.value.status_code == 409


def test_release_stock_restores(db: Session):
    product = Product(
        id=uuid.uuid4().hex,
        name="P3",
        slug="p3",
        price=1.0,
        stock=10,
    )
    db.add(product)
    db.commit()
    ReserveStock(db, product.id, 3)
    db.commit()
    ReleaseStock(db, product.id, 3)
    db.commit()
    db.refresh(product)
    assert product.stock == 10
