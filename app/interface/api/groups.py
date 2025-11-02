from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from another_fastapi_jwt_auth import AuthJWT
from fastapi_pagination import Params, Page
from fastapi_pagination.async_paginator import apaginate
from starlette import status

from app.domain.contracts.group_contracts import IGroupService
from app.interface.schemas.group import GroupBaseSchema, GroupCreateSchema, GroupSetPermissionSchema

router = APIRouter()

#TODO: Add retrieve method, partial_update and remove_group method

@router.get(
    path="/",
    response_model=Page[GroupBaseSchema],
    status_code=status.HTTP_200_OK,
    summary='List of Groups'
)
@inject
async def groups_list(
        authorize: AuthJWT = Depends(),
        service: FromDishka[IGroupService] = None,
        params: Params = Depends(),
):
    authorize.jwt_required()
    groups = await service.groups_list()
    return await apaginate(sequence=groups, params=params)

@router.post(
    path='/',
    response_model=GroupBaseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Create a new validators',
)
@inject
async def create(
        payload: GroupCreateSchema,
        authorize: AuthJWT = Depends(),
        service: FromDishka[IGroupService] = None,
):
    authorize.jwt_required()
    group = await service.create(
       name=payload.name,
    )
    return group

@router.post(
    path='/{group_id}/set_permission/',
    response_model=GroupBaseSchema,
)
@inject
async def set_permission(
        group_id: int,
        payload: GroupSetPermissionSchema,
        authorize: AuthJWT = Depends(),
        service: FromDishka[IGroupService] = None,
):
    authorize.jwt_required()
    response_dto = await service.set_permissions(
        group_id=group_id,
        code_name=payload.code_name
    )
    return response_dto