from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from another_fastapi_jwt_auth import AuthJWT
from fastapi_pagination import Params, Page
from fastapi_pagination.async_paginator import apaginate
from starlette import status

from app.application.dto.group import GroupDto
from app.domain.contracts.group_contracts import IGroupService
from app.interface.schemas.group import (
    GroupBaseSchema,
    GroupCreateSchema,
    GroupUpdateSchema,
)

router = APIRouter()


@router.get(
    path="/",
    response_model=Page[GroupBaseSchema],
    status_code=status.HTTP_200_OK,
    summary="List of Groups",
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


@router.get(
    path="/{group_id}/",
    response_model=GroupBaseSchema,
    status_code=status.HTTP_200_OK,
)
@inject
async def retrieve(
    group_id: int,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IGroupService] = None,
):
    authorize.jwt_required()
    group = await service.retrieve(
        group_id=group_id,
    )
    return group


@router.post(
    path="/",
    response_model=GroupBaseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new validators",
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


@router.patch(
    path="/{group_id}/",
    response_model=GroupBaseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update groups",
)
@inject
async def partial_update(
    group_id: int,
    payload: GroupUpdateSchema,
    authorize: AuthJWT = Depends(),
    service: FromDishka[IGroupService] = None,
):
    authorize.jwt_required()
    group = await service.partial_update(
        data=GroupDto(id=group_id, **payload.model_dump(exclude_unset=True)),
    )
    return group
