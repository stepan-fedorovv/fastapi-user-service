from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


from app.domain.errors.permission_error_classes import PermissionAlreadyExists


def permission_install_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(PermissionAlreadyExists)
    async def _permission_exists(request: Request, exc: PermissionAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=exc.errors_dto.model_dump(),
        )
