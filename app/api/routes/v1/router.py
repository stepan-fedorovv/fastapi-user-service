from fastapi import APIRouter

from app.api.routes.v1.user_routes import router as user_routes

v1_router = APIRouter()

v1_router.include_router(user_routes, tags=['users'], prefix="/users")