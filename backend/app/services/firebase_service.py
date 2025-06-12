"""app/services/firebase_service.py"""

from app.config import get_db
from google.cloud.firestore import DocumentReference
from typing import Optional, Dict, List

db = get_db()

def create_document(collection_name: str, data: Dict, doc_id: Optional[str] = None) -> str:
    try:
        if doc_id:
            doc_ref = db.collection(collection_name).document(doc_id)
        else:
            doc_ref = db.collection(collection_name).document()
            data['id'] = doc_ref.id  # Attach auto-generated ID to the data

        doc_ref.set(data)
        return doc_ref.id
    except Exception as e:
        raise Exception(f"Failed to create document in {collection_name}: {str(e)}")


def get_document(collection_name: str, doc_id: str) -> Optional[Dict]:
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        raise Exception(f"Failed to retrieve document from {collection_name}: {str(e)}")


def update_document(collection_name: str, doc_id: str, updates: Dict) -> bool:
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.update(updates)
        return True
    except Exception as e:
        raise Exception(f"Failed to update document in {collection_name}: {str(e)}")


def delete_document(collection_name: str, doc_id: str) -> bool:
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.delete()
        return True
    except Exception as e:
        raise Exception(f"Failed to delete document from {collection_name}: {str(e)}")


def list_documents(collection_name: str) -> List[Dict]:
    try:
        docs = db.collection(collection_name).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        raise Exception(f"Failed to list documents from {collection_name}: {str(e)}")
