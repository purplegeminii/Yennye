from fastapi import FastAPI
import uvicorn
from app import config
from app.routes import (
    user_routes, farm_routes, product_routes, order_routes, delivery_routes
)



app = FastAPI(
    description="FastAPI backend for devpost hackathon, Yennye",
    title="Yennye Backend",
    docs_url="/",
    version="0.0.1"
)

# Firebase setup
config.init_firebase()

# Route includes
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(farm_routes.router, prefix="/farms", tags=["Farms"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(delivery_routes.router, prefix="/deliveries", tags=["Deliveries"])
