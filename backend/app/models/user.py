"""app/models/user.py"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    customer = "customer"
    farmer = "farmer"
    admin = "admin"
    delivery_agent = "delivery_agent"

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: RoleEnum

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "fullname",
                "email": "sample@email.com",
                "role": "customer"
            }
        }

class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "fullname",
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
                "full_name": "fullname",
                "email": "sample@email.com",
                "role": "customer",
                "uid": "uid"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    # id_token: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "sample@email.com",
                "password": "password"
            }
        }

class UserLoginResponse(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    uid: str
    id_token: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: RoleEnum

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "fullname",
                "email": "sample@email.com",
                "role": "customer"
            }
        }
