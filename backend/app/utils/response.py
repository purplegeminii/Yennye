"""app/utils/response.py"""

from fastapi.responses import JSONResponse

def success_response(data, status_code=200, message="Success"):
    return JSONResponse(status_code=status_code, content={"status": "success", "message": message, "data": data})

def error_response(status_code=400, message="An error occurred"):
    return JSONResponse(status_code=status_code, content={"status": "error", "message": message})