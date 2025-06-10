"""app/routes/product_routes.py"""

from fastapi import APIRouter
from app.models.product import Product
from app.config import db

router = APIRouter()

@router.post("/add", response_model=Product)
def add_product(product: Product):
    ref = db.collection("products").document(product.product_id)
    ref.set(product.model_dump())
    return product
