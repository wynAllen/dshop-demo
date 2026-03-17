from sqlalchemy.orm import Session

from retail_api.common.exceptions import AppException
from retail_api.product.models import Product


def ReserveStock(db: Session, product_id: str, quantity: int) -> float:
    product = db.query(Product).filter(Product.id == product_id).with_for_update().first()
    if not product:
        raise AppException(
            message="Product not found",
            code="NOT_FOUND",
            status_code=404,
            details={"product_id": product_id},
        )
    if product.stock < quantity:
        raise AppException(
            message="Insufficient stock",
            code="CONFLICT",
            status_code=409,
            details={"product_id": product_id, "available": product.stock},
        )
    product.stock -= quantity
    return float(product.price)


def ReleaseStock(db: Session, product_id: str, quantity: int) -> None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is not None:
        product.stock += quantity
