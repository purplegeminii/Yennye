"""app/models/order.py"""

from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    order_id: str
    customer_uid: str
    items: List[OrderItem]
    total_price: float
    delivery_address: str
    status: str  # 'pending', 'confirmed', 'shipped', 'delivered'