import os
from dotenv import load_dotenv
import uvicorn
import pyrebase
from fastapi import FastAPI

load_dotenv()

app = FastAPI(
    description="FastAPI backend for devpost hackathon, Yennye",
    title="Yennye Backend",
    docs_url="/"
)


import firebase_admin
from firebase_admin import credentials


if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)


firebaseConfig = os.getenv()

firebase = pyrebase.initialize_app()


@app.post('/signup')
async def create_an_account():
    pass

@app.post('/login')
async def create_access_token():
    pass

@app.post('/ping')
async def validate_token():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)