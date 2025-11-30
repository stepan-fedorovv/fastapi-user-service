import uuid

from app.shared.jwt.classes import AuthJWTWithPermission as AuthJWT
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from fastapi_pagination import Params, Page
from fastapi_pagination.async_paginator import apaginate
from starlette import status

from app.core import config
from app.domain.contracts.user_contracts import IUserService
from app.interface.schemas.user import (
    UserBaseSchema,
    AuthResponseSchema,
    UserCreateSchema,
    LoginRequestSchema,
    UserUpdateSchema,
)

router = APIRouter()


@router.post(
    path="/",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
@inject
async def register(
    payload: UserCreateSchema,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IUserService] = None,
):
    user = await service.create(
        email=payload.email,
        password=payload.password,
        group_id=payload.group_id,
    )
    access_token = authorize.create_access_token(
        subject=str(user.id),
        user_claims={
            "iss": config.JWT_ISS,
            "aud": config.JWT_AUD,
            "group": user.group.name,
            "permissions": [
                permission.code_name for permission in user.group.permissions
            ],
            "jti": str(uuid.uuid4()),
            "kid": config.JWT_KID,
        },
        algorithm=config.JWT_ALGORITHM,
    )
    refresh_token = authorize.create_refresh_token(
        subject=str(user.id),
        user_claims={
            "iss": config.JWT_ISS,
            "jti": str(uuid.uuid4()),
            "kid": config.JWT_KID,
            "typ": "refresh",
        },
        algorithm=config.JWT_ALGORITHM,
    )
    return AuthResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    path="/login/",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_200_OK,
)
@inject
async def login(
    payload: LoginRequestSchema,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IUserService] = None,
):
    user = await service.login(
        email=payload.email,
        password=payload.password,
    )
    access_token = authorize.create_access_token(
        subject=str(user.id),
        user_claims={
            "iss": config.JWT_ISS,
            "aud": config.JWT_AUD,
            "group": user.group.name,
            "permissions": [
                permission.code_name for permission in user.group.permissions
            ],
            "jti": str(uuid.uuid4()),
            "kid": config.JWT_KID,
        },
        algorithm=config.JWT_ALGORITHM,
    )
    refresh_token = authorize.create_refresh_token(
        subject=str(user.id),
        user_claims={
            "iss": config.JWT_ISS,
            "aud": config.JWT_AUD,
            "jti": str(uuid.uuid4()),
            "kid": config.JWT_KID,
            "typ": "refresh",
        },
        algorithm=config.JWT_ALGORITHM,
    )
    return AuthResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    path="/me/",
    response_model=UserBaseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get user info",
)
@inject
async def me(
    authorize: AuthJWT = Depends(),
    service: FromDishka[IUserService] = None,
):
    authorize.jwt_required()
    return await service.me(user_id=int(authorize.get_jwt_subject()))


@router.get(
    path="/",
    response_model=Page[UserBaseSchema],
    status_code=status.HTTP_200_OK,
    summary="Get user list",
)
@inject
async def users_list(
    service: FromDishka[IUserService] = None,
    params: Params = Depends(),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    users = await service.users_list()
    return await apaginate(sequence=users, params=params)


@router.patch(
    path="/{user_id}/",
    response_model=UserBaseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update user",
)
@inject
async def partial_update(
    user_id: int,
    payload: UserUpdateSchema,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IUserService] = None,
):
    authorize.jwt_required()
    return await service.partial_update(
        user_id=user_id,
        payload=payload.model_dump(exclude_unset=True),
    )


@router.post(
    path="/refresh/",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Refresh token",
)
@inject
async def refresh(
    service: FromDishka[IUserService] = None, authorize: AuthJWT = Depends()
):
    authorize.jwt_refresh_token_required()
    subject = authorize.get_jwt_subject()
    user = await service.find_by_id(
        user_id=int(subject),
    )
    access_token = authorize.create_access_token(
        subject=subject,
        user_claims={
            "iss": config.JWT_ISS,
            "aud": config.JWT_AUD,
            "group": user.group.name,
            "permissions": [
                permission.code_name for permission in user.group.permissions
            ],
            "jti": str(uuid.uuid4()),
            "kid": config.JWT_KID,
        },
        algorithm=config.JWT_ALGORITHM,
    )
    refresh_token = authorize.create_refresh_token(
        subject=str(user.id),
        user_claims={
            "iss": config.JWT_ISS,
            "aud": config.JWT_AUD,
            "jti": str(uuid.uuid4()),
            "kid": config.JWT_KID,
        },
    )
    return AuthResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    path="/{user_id}/",
    response_model=UserBaseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get concrete user info",
)
@inject
async def retrieve(
    user_id: int,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IUserService] = None,
):
    authorize.jwt_required()
    return await service.find_by_id(
        user_id=user_id,
    )
