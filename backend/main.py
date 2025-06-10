import os
from dotenv import load_dotenv
import uvicorn
import pyrebase
from fastapi import FastAPI
from models import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

load_dotenv()

app = FastAPI(
    description="FastAPI backend for devpost hackathon, Yennye",
    title="Yennye Backend",
    docs_url="/"
)


import firebase_admin
from firebase_admin import credentials, auth


if not firebase_admin._apps:
    cred = credentials.Certificate("backend/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)


firebaseConfig = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "projectId": os.getenv("projectId"),
    "storageBucket": os.getenv("storageBucket"),
    "messagingSenderId": os.getenv("messagingSenderId"),
    "appId": os.getenv("appId"),
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)


@app.post('/signup')
async def create_an_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.create_user(
            email = email,
            password = password
        )
        return JSONResponse(
            content = {"message": f"User account created successfully for user {user.uid}"},
            status_code = 201
        )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code = 400,
            detail = f"Account already created for the email {email}"
        )


@app.post('/login')
async def create_access_token(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(email, password)
        
        token = user['idToken']

        return JSONResponse(
            content = {"token": token},
            status_code = 200
        )
    except:
        raise HTTPException(
            status_code = 400,
            detail = "Invalid Credentials"
        )


@app.post('/ping')
async def validate_token(request: Request):
    headers = request.headers
    jwt = headers.get('authorization')

    user = auth.verify_id_token(jwt)

    return user['uid']


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
