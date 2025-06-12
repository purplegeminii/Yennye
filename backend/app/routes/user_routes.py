"""app/routes/user_routes.py"""


from fastapi import APIRouter, HTTPException
from app.models.user import *
from app.config import get_db
from app.services.auth_service import authenticate_user
from app.utils.password_utils import hash_password
from app.utils.response import success_response, error_response

router = APIRouter()
db = get_db()

@router.post("/register", response_model=User)
def register_user(user: UserCreate):
    try:
        user_ref = db.collection("users").document()
        hashed_pwd = hash_password(user.password)

        user_data = user.model_dump()
        user_data["password"] = hashed_pwd
        user_data["uid"] = user_ref.id

        user_ref.set(user_data)
        user_data.pop("password")

        return success_response(data=user_data, message="User registered successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.post("/login", response_model=User)
def login_user(user: UserLogin):
    try:
        user_data = authenticate_user(user.email, user.password, db)
        return success_response(data=user_data, message="Login successful")
    except Exception as e:
        return error_response(message=str(e), status_code=401)

@router.get("/{uid}", response_model=User)
def get_user(uid: str):
    try:
        doc = db.collection("users").document(uid).get()
        if not doc.exists:
            return error_response(message="User not found")
        user = User(**doc.to_dict())
        return success_response(data=user.model_dump(), message="User retrieved successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.put("/{uid}", response_model=User)
def update_user(uid: str, user: UserCreate):
    try:
        user_data = user.model_dump()
        user_data.pop("password")
        user_data["uid"] = uid
        db.collection("users").document(uid).update(user_data)
        user = User(**user_data)
        return success_response(data=user.model_dump(), message="User updated successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.delete("/{uid}", response_model=User)
def delete_user(uid: str):
    try:
        doc = db.collection("farms").document(uid).get()
        if not doc.exists:
            return error_response(message="User not found")
        db.collection("farms").document(uid).delete()
        return success_response(message="User deleted successfully")
    except Exception as e:
        return error_response(message=str(e))
