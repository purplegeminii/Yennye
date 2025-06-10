from fastapi import FastAPI
import uvicorn
from app.routes import (
    user_routes, farm_routes, product_routes, order_routes, delivery_routes
)
from app.config import init_firebase

app = FastAPI(
    description="FastAPI backend for devpost hackathon, Yennye",
    title="Yennye Backend",
    docs_url="/"
)

# Firebase setup
init_firebase()

# Route includes
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(farm_routes.router, prefix="/farms", tags=["Farms"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(delivery_routes.router, prefix="/deliveries", tags=["Deliveries"])


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)