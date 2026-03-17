from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from retail_api.db.session import get_db
from retail_api.product.schemas import ProductListOut, ProductOut
from retail_api.product.service import GetProductById, ListProducts

router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.get("", response_model=ProductListOut)
def ProductList(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    items, total = ListProducts(db, page=page, page_size=page_size)
    return ProductListOut(
        items=[ProductOut.model_validate(p) for p in items],
        total=total,
        page=page,
    )


@router.get("/{product_id}", response_model=ProductOut)
def ProductDetail(
    product_id: str,
    db: Session = Depends(get_db),
):
    product = GetProductById(db, product_id)
    return ProductOut.model_validate(product)
