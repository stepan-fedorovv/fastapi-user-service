from fastapi import APIRouter

from app.core import config
from app.interface.api.users import router as user_routes
from app.interface.api.groups import router as group_routes
from app.interface.api.permissions import router as permission_routes

grouping_router = APIRouter(prefix=config.API_ROUTE, tags=["api"])

grouping_router.include_router(user_routes, tags=["users"], prefix="/users")
grouping_router.include_router(group_routes, tags=["groups"], prefix="/groups")
grouping_router.include_router(
    permission_routes, tags=["permissions"], prefix="/permissions"
)
