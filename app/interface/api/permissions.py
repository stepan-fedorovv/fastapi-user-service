from another_fastapi_jwt_auth import AuthJWT
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.async_paginator import apaginate
from starlette import status

from app.domain.contracts.permission_contracts import IPermissionService
from app.interface.schemas.permission import PermissionBaseSchema, PermissionCreateSchema
router = APIRouter()

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=Page[PermissionBaseSchema]
)
@inject
async def permission_list(
        authorize: AuthJWT = Depends(),
        params: Params = Depends(),
        service: FromDishka[IPermissionService] = None,
):
    authorize.jwt_required()
    permissions = await service.permissions_list()
    return await apaginate(sequence=permissions, params=params)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=PermissionBaseSchema,
    summary='Create a new permission',
)
@inject
async def create(
        payload: PermissionCreateSchema,
        authorize: AuthJWT = Depends(),
        service: FromDishka[IPermissionService] = None,
):
    authorize.jwt_required()
    permission = await service.create(
        name=payload.name,
        code_name=payload.code_name,
    )
    return permission