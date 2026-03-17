from sqlalchemy.orm import Session

from retail_api.common.exceptions import NotFoundError
from retail_api.product.models import Product


def ListProducts(
    db: Session,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Product], int]:
    offset = (page - 1) * page_size
    query = db.query(Product)
    total = query.count()
    items = query.offset(offset).limit(page_size).all()
    return items, total


def GetProductById(db: Session, product_id: str) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise NotFoundError("Product not found", details={"product_id": product_id})
    return product
