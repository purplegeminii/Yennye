"""app/routes/user_routes.py"""


from fastapi import APIRouter, HTTPException
from app.models.user import *
from app.config import get_db
# from app.utils.id_generator import generate_id
from app.services.auth_service import authenticate_user
from app.utils.password_utils import hash_password, verify_password
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

@router.post("/login")
def login_user(user: UserLogin):  # Reusing UserCreate for email & password
    try:
        user_data = authenticate_user(user.email, user.password, db)
        return success_response(data=user_data, message="Login successful")
    except Exception as e:
        return error_response(message=str(e), status_code=401)

@router.get("/{uid}", response_model=User)
def get_user(uid: str):
    doc = db.collection("users").document(uid).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**doc.to_dict()).model_dump()

@router.put("/{uid}", response_model=User)
def update_user(uid: str, user: UserCreate):
    user_data = user.model_dump()
    user_data.pop("password")
    user_data["uid"] = uid
    db.collection("users").document(uid).update(user_data)
    return User(**user_data).model_dump()

@router.delete("/{uid}")
def delete_user(uid: str):
    db.collection("users").document(uid).delete()
    return {"status": "success", "message": "User deleted"}
