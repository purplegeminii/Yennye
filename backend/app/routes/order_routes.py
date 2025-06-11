"""app/routes/order_routes.py"""

from fastapi import APIRouter
from app.models.order import Order
from app.config import get_db

router = APIRouter()
db = get_db()

@router.post("/place", response_model=Order)
def place_order(order: Order):
    ref = db.collection("orders").document(order.order_id)
    ref.set(order.model_dump())
    return order
