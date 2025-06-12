"""app/routes/user_routes.py"""


from fastapi import APIRouter, HTTPException, Header
from app.models.user import *
from app.models.response import ResponseModel
from app.config import get_db, pyrebaseFirebase
from app.services.auth_service import authenticate_user, verify_token
from app.utils.password_utils import hash_password
from app.utils.response import success_response, error_response

router = APIRouter()
db = get_db()


@router.post("/register", response_model=ResponseModel[User])
def register_user(user: UserCreate):
    try:
        # Register with Firebase Authentication
        firebase_user = pyrebaseFirebase.auth().create_user_with_email_and_password(user.email, user.password)
        uid = firebase_user['localId']

        # Prepare user data for Firestore
        hashed_pwd = hash_password(user.password)
        user_data = user.model_dump()
        user_data["password"] = hashed_pwd
        user_data["uid"] = uid

        # Save to Firestore
        db.collection("users").document(uid).set(user_data)
        user_data.pop("password")

        return success_response(status_code=201, data=user_data, message="User registered successfully")
    except Exception as e:
        return error_response(message=str(e))


@router.post("/login", response_model=ResponseModel[UserLoginResponse])
def login_user(user: UserLogin):
    try:
        user_data = authenticate_user(user.email, user.password, db)

        firebase_user = pyrebaseFirebase.auth().sign_in_with_email_and_password(user.email, user.password)
        
        user_data["id_token"] = firebase_user['idToken']

        return success_response(data=user_data, message="Login successful")
    except Exception as e:
        return error_response(message=str(e))

@router.get("/{uid}", response_model=ResponseModel[User])
def get_user(uid: str):
    try:
        doc = db.collection("users").document(uid).get()
        if not doc.exists:
            return error_response(status_code=404, message="User not found")
        user = User(**doc.to_dict())
        return success_response(data=user.model_dump(), message="User retrieved successfully")
    except Exception as e:
        return error_response(message=str(e))


@router.put("/{uid}", response_model=User)
def update_user(uid: str, user: UserUpdate, authorization: str = Header(...)):
    try:
        if not authorization.startswith("Bearer "):
            return error_response(status_code=401, message="Invalid authorization header format")

        token = authorization.split(" ")[1]  # Extract token after 'Bearer'
        decoded = verify_token(token)
        
        if decoded['uid'] != uid:
            return error_response(status_code=403, message="Unauthorized to update this user")

        user_ref = db.collection("users").document(uid)
        if not user_ref.get().exists:
            return error_response(status_code=404, message="User not found")

        user_data = user.model_dump(exclude_unset=True)
        user_data["uid"] = uid
        user_ref.update(user_data)

        updated_user = User(**user_data)
        return success_response(data=updated_user.model_dump(), message="User updated successfully")
    except Exception as e:
        return error_response(message=str(e))


@router.delete("/{uid}")
def delete_user(uid: str):
    try:
        doc = db.collection("farms").document(uid).get()
        if not doc.exists:
            return error_response(status_code=404, message="User not found")
        db.collection("farms").document(uid).delete()
        return success_response(message="User deleted successfully")
    except Exception as e:
        return error_response(message=str(e))
