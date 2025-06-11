"""app/routes/delivery_routes.py"""

from fastapi import APIRouter
from app.models.delivery import Delivery
from app.config import get_db

router = APIRouter()
db = get_db()

@router.post("/assign", response_model=Delivery)
def assign_delivery(delivery: Delivery):
    ref = db.collection("deliveries").document(delivery.delivery_id)
    ref.set(delivery.model_dump())
    return delivery
