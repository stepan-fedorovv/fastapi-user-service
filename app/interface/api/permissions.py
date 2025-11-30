from another_fastapi_jwt_auth import AuthJWT
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.async_paginator import apaginate
from starlette import status

from app.application.dto.permission import PermissionDto
from app.domain.contracts.permission_contracts import IPermissionService
from app.interface.schemas.permission import (
    PermissionBaseSchema,
    PermissionCreateSchema,
    PermissionUpdateSchema,
)

router = APIRouter()


@router.get(
    path="/", status_code=status.HTTP_200_OK, response_model=Page[PermissionBaseSchema]
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
    summary="Create a new permission",
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


@router.get(
    path="/{permission_id}/",
    status_code=status.HTTP_200_OK,
    response_model=PermissionBaseSchema,
    summary="Get a permission",
)
@inject
async def retrieve(
    permission_id: int,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IPermissionService] = None,
):
    authorize.jwt_required()
    permission = await service.get_permission(
        permission_id=permission_id,
    )
    return permission


@router.delete(
    path="/{permission_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a permission",
)
@inject
async def delete(
    permission_id: int,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IPermissionService] = None,
):
    authorize.jwt_required()
    await service.delete(
        permission_id=permission_id,
    )
    return None


@router.patch(
    path="/{permission_id}/",
    status_code=status.HTTP_200_OK,
    summary="Update a permission",
    response_model=PermissionBaseSchema,
)
@inject
async def partial_update(
    permission_id: int,
    payload: PermissionUpdateSchema,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IPermissionService] = None,
):
    authorize.jwt_required()
    permission = await service.partial_update(
        data=PermissionDto(id=permission_id, **payload.model_dump(exclude_unset=True))
    )
    return permission
