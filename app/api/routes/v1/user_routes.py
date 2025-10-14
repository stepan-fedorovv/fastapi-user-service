from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependency.user import get_user_service
from app.api.routes.v1.schemas.user import UserCreateSchema, UserResponseSchema
from app.db.uow import UnitOfWork, get_uow
from app.logic.user.service import UserService

router = APIRouter()


@router.post(
    path='/',
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Create a new user',
)
async def create(
        payload: UserCreateSchema,
        service: UserService = Depends(get_user_service)
):
    return await service.create(payload)