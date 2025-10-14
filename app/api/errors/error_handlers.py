# error_handlers.py

from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse
from starlette_problem.handler import add_exception_handler

from app.common.errors import UserAlreadyExists


def install_exception_handlers(app: FastAPI) -> None:
    add_exception_handler(app)

    @app.exception_handler(UserAlreadyExists)
    async def _user_exists(request: Request, exc: UserAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=exc.errors_dto.model_dump(),
        )