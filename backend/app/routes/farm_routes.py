"""app/routes/farm_routes.py"""

from fastapi import APIRouter, HTTPException
from app.models.farm import Farm
from app.config import db
from app.utils.response import success_response, error_response

router = APIRouter()

@router.post("/register", response_model=Farm)
def register_farm(farm: Farm):
    try:
        ref = db.collection("farms").document(farm.farm_id)
        ref.set(farm.dict())
        return success_response(data=farm.model_dump(), message="Farm registered successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.get("/{farm_id}", response_model=Farm)
def get_farm(farm_id: str):
    try:
        doc = db.collection("farms").document(farm_id).get()
        if not doc.exists:
            return error_response(message="Farm not found")
        farm = Farm(**doc.to_dict())
        return success_response(data=farm.model_dump(), message="Farm retrieved successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.put("/{farm_id}", response_model=Farm)
def update_farm(farm_id: str, farm: Farm):
    try:
        doc = db.collection("farms").document(farm_id).get()
        if not doc.exists:
            return error_response(message="Farm not found")
        db.collection("farms").document(farm_id).update(farm.dict())
        return success_response(data=farm.model_dump(), message="Farm updated successfully")
    except Exception as e:
        return error_response(message=str(e))

@router.delete("/{farm_id}", response_model=Farm)
def delete_farm(farm_id: str):
    try:
        doc = db.collection("farms").document(farm_id).get()
        if not doc.exists:
            return error_response(message="Farm not found")
        db.collection("farms").document(farm_id).delete()
        return success_response(message="Farm deleted successfully")
    except Exception as e:
        return error_response(message=str(e))
