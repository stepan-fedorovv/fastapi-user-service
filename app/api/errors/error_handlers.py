# error_handlers.py

from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette import status
from starlette.responses import JSONResponse
from starlette_problem.handler import add_exception_handler

from app.api.errors.dto.user_errors import ErrorResponseDto, ErrorCode
from app.common.errors import UserAlreadyExists


def install_exception_handlers(app: FastAPI) -> None:
    add_exception_handler(app)

    @app.exception_handler(UserAlreadyExists)
    async def _user_exists(request: Request, exc: UserAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=exc.errors_dto.model_dump(),
        )

    @app.exception_handler(AuthJWTException)
    def auth_jwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponseDto(
                detail=exc.message,
                status=exc.status_code,
                code=ErrorCode.UNAUTHORIZED.value,
                errors=[]
            ).model_dump()
        )
