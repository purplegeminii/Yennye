"""app/routes/delivery_routes.py"""

from fastapi import APIRouter
from app.models.delivery import Delivery
from app.config import get_db
from app.utils.response import success_response, error_response


router = APIRouter()
db = get_db()


@router.post("/assign", response_model=Delivery)
def assign_delivery(delivery: Delivery):
    try:
        ref = db.collection("deliveries").document(delivery.delivery_id)
        ref.set(delivery.model_dump())
        return success_response(data=delivery.model_dump(), message="Delivery assigned successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.get("/{delivery_id}", response_model=Delivery)
def get_delivery(delivery_id: str):
    try:
        doc = db.collection("deliveries").document(delivery_id).get()
        if not doc.exists:
            return error_response(message="Delivery not found")
        delivery = Delivery(**doc.to_dict())
        return success_response(data=delivery.model_dump(), message="Delivery retrieved successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.put("/{delivery_id}", response_model=Delivery)
def update_delivery(delivery_id: str, delivery: Delivery):
    try:
        ref = db.collection("deliveries").document(delivery_id)
        ref.set(delivery.model_dump())
        return success_response(data=delivery.model_dump(), message="Delivery updated successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.delete("/{delivery_id}")
def delete_delivery(delivery_id: str):
    try:
        db.collection("deliveries").document(delivery_id).delete()
        return success_response(data=None, message="Delivery deleted successfully")
    except Exception as e:
        return error_response(message=str(e))