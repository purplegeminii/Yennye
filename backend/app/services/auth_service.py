"""app/services/auth_service.py"""

from fastapi import HTTPException
import firebase_admin
from firebase_admin import auth
from app.utils.password_utils import verify_password
from app.utils.response import success_response, error_response


def verify_token(id_token: str):
    return auth.verify_id_token(id_token)  #jwt


def authenticate_user(email: str, password: str, db) -> dict:
    users = db.collection("users").where("email", "==", email).limit(1).stream()
    user = next(users, None)

    if not user or not user.exists:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user_data = user.to_dict()
    if not verify_password(password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Firebase Admin SDK doesn't support password login, so normally you'd use Firebase client SDK for this.
    # But if using token-based login elsewhere, return user info here
    user_data.pop("password")  # Remove password before returning
    return user_data