"""app/routes/product_routes.py"""

from fastapi import APIRouter
from app.models.product import *
from app.config import get_db
from app.utils.response import success_response, error_response

router = APIRouter()
db = get_db()


@router.post("/add", response_model=Product)
def add_product(product: Product):
    try:
        ref = db.collection("products").document(product.product_id)
        ref.set(product.model_dump())
        return success_response(data=product.model_dump(), message="Product added successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str):
    try:
        doc = db.collection("products").document(product_id).get()
        if not doc.exists:
            return error_response(message="Product not found")
        product = Product(**doc.to_dict())
        return success_response(data=product.model_dump(), message="Product retrieved successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: str, product: Product):
    try:
        ref = db.collection("products").document(product_id)
        ref.set(product.model_dump())
        return success_response(data=product.model_dump(), message="Product updated successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.delete("/{product_id}")
def delete_product(product_id: str):
    try:
        db.collection("products").document(product_id).delete()
        return success_response(data=None, message="Product deleted successfully")
    except Exception as e:
        return error_response(message=str(e))
