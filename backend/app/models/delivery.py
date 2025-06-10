"""app/models/delivery.py"""

from pydantic import BaseModel
from typing import Optional

class Delivery(BaseModel):
    delivery_id: str
    order_id: str
    assigned_agent_uid: str
    status: str  # 'pending', 'in_transit', 'completed'
    tracking_location: Optional[str] = None