"""app/routes/product_routes.py"""

from fastapi import APIRouter
from app.models.product import Product
from app.config import get_db

router = APIRouter()
db = get_db()

@router.post("/add", response_model=Product)
def add_product(product: Product):
    ref = db.collection("products").document(product.product_id)
    ref.set(product.model_dump())
    return product
