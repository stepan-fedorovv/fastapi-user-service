# error_handlers.py

from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from app.domain.errors.user_errors_classes import UserAlreadyExists, UserDoesNotExists


def user_install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExists)
    async def _user_exists(request: Request, exc: UserAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=exc.errors_dto.model_dump(),
        )

    @app.exception_handler(UserDoesNotExists)
    async def _user_does_not_exist(request: Request, exc: UserDoesNotExists):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=exc.errors_dto.model_dump(),
        )
