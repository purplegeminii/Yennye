"""app/routes/order_routes.py"""

from fastapi import APIRouter
from app.models.order import Order
from app.config import get_db
from app.utils.response import success_response, error_response

router = APIRouter()
db = get_db()


@router.post("/place", response_model=Order)
def place_order(order: Order):
    try:
        ref = db.collection("orders").document(order.order_id)
        ref.set(order.model_dump())
        return success_response(data=order.model_dump(), message="Order placed successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str):
    try:
        doc = db.collection("orders").document(order_id).get()
        if not doc.exists:
            return error_response(message="Order not found")
        order = Order(**doc.to_dict())
        return success_response(data=order.model_dump(), message="Order retrieved successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.put("/{order_id}", response_model=Order)
def update_order(order_id: str, order: Order):
    try:
        ref = db.collection("orders").document(order_id)
        ref.set(order.model_dump())
        return success_response(data=order.model_dump(), message="Order updated successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.delete("/{order_id}")
def delete_order(order_id: str):
    try:
        db.collection("orders").document(order_id).delete()
        return success_response(data=None, message="Order deleted successfully")
    except Exception as e:
        return error_response(message=str(e))
