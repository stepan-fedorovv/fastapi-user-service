from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from starlette import status

from app.api.dependency.user import get_user_service
from app.api.routes.v1.schemas.user import UserCreateSchema, UserBaseSchema, AuthResponseSchema
from app.db.uow import UnitOfWork, get_uow
from app.logic.user.service import UserService

router = APIRouter()


@router.post(
    path='/',
    response_model=AuthResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Create a new user',
)
async def create(
        payload: UserCreateSchema,
        authorize: AuthJWT = Depends(),
        service: UserService = Depends(get_user_service),
):
    access_token = authorize.create_access_token(subject=payload.email)
    refresh_token = authorize.create_refresh_token(
        subject=payload.email,
        expires_time=timedelta(hours=2)
    )
    await service.create(payload)
    return AuthResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    ).model_dump()


@router.get(
    path='/me/',
    response_model=UserBaseSchema,
    status_code=status.HTTP_200_OK,
    summary='Get user information',
)
async def me(
        authorize: AuthJWT = Depends(),
        service: UserService = Depends(get_user_service),
):
    authorize.jwt_required()
    return await service.me(
        email=authorize.get_jwt_subject()
    )

@router.post('/refresh/')
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    subject = authorize.get_jwt_subject()
    access_token = authorize.create_access_token(subject=subject)
    refresh_token = authorize.create_refresh_token(subject=subject)
    return AuthResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    ).model_dump()
