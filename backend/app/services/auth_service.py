"""app/services/auth_service.py"""

import firebase_admin
from firebase_admin import auth

def create_firebase_user(email: str, password: str):
    user_record = auth.create_user(
        email=email,
        password=password
    )
    return user_record.uid


def verify_token(id_token: str):
    decoded_token = auth.verify_id_token(id_token)  #jwt
    return decoded_token