"""app/models/user.py"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str  # 'customer', 'farmer', 'admin', 'delivery_agent'

class UserCreate(UserBase):
    password: str

class User(UserBase):
    uid: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
