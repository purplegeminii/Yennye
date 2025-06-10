"""app/models/product.py"""

from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    product_id: str
    farm_id: str
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    is_available: bool = True