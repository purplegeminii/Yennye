"""app/models/farm.py"""

from pydantic import BaseModel
from typing import Optional

class Farm(BaseModel):
    farm_id: str
    farmer_uid: str
    name: str
    location: str
    description: Optional[str] = None