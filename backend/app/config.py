import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

load_dotenv()

_app_initialized = False

def init_firebase():
    global _app_initialized
    if not firebase_admin._apps:

        # Compute path from this file (config.py) to the serviceAccountKey
        current_dir = os.path.dirname(os.path.abspath(__file__))  # .../backend/app
        # key_path = os.path.abspath(os.path.join(current_dir, "..", os.getenv("FIREBASE_CRED_JSON")))
        key_path = os.path.abspath(os.path.join(current_dir, "..", "serviceAccountKey.json"))
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        
    _app_initialized = True

def get_db():
    if not _app_initialized:
        init_firebase()
    return firestore.client()

firebaseConfig = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "projectId": os.getenv("projectId"),
    "storageBucket": os.getenv("storageBucket"),
    "messagingSenderId": os.getenv("messagingSenderId"),
    "appId": os.getenv("appId"),
    "databaseURL": os.getenv("databaseURL")
}

pyrebaseFirebase = pyrebase.initialize_app(firebaseConfig)

