"""app/models/user.py"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str  # 'customer', 'farmer', 'admin', 'delivery_agent'

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "fullname",
                "email": "sample@email.com",
                "role": "customer"
            }
        }

class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "fullname",
                "email": "sample@email.com",
                "role": "customer",
                "password": "password"
            }
        }

class User(UserBase):
    uid: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "fullname",
                "email": "sample@email.com",
                "role": "customer",
                "uid": "uid"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "sample@email.com",
                "password": "password"
            }
        }
