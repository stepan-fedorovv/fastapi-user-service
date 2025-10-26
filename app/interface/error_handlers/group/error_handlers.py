from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.errors.group_error_classes import GroupAlreadyExists
from app.domain.errors.permission_error_classes import PermissionNotFound, PermissionAlreadySetInGroup


def group_install_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(GroupAlreadyExists)
    async def _group_exists(request: Request, exc: GroupAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=exc.errors_dto.model_dump(),
        )

    @app.exception_handler(PermissionNotFound)
    async def _permission_not_found(request: Request, exc: PermissionNotFound):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=exc.errors_dto.model_dump(),
        )

    @app.exception_handler(PermissionAlreadySetInGroup)
    async def _permission_already_set(request: Request, exc: PermissionAlreadySetInGroup):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=exc.errors_dto.model_dump(),
        )
