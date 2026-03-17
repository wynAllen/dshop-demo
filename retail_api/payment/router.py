from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from retail_api.db.session import get_db
from retail_api.payment.service import GetOrderForPayment, MarkOrderPaid

router = APIRouter(prefix="/api/v1", tags=["payment"])


@router.post("/orders/{order_id}/pay")
def OrderPay(
    order_id: str,
    db: Session = Depends(get_db),
):
    order = GetOrderForPayment(db, order_id)
    return {
        "order_id": order.id,
        "status": "pending",
        "pay_url": f"/stub/pay/{order.id}",
    }


@router.post("/payment/callback/stub")
def PaymentCallbackStub(
    order_id: str,
    success: bool = True,
    db: Session = Depends(get_db),
):
    if success:
        MarkOrderPaid(db, order_id)
    return {"received": True}
