from fastapi import FastAPI
from another_fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.interface.error_handlers.group.error_handlers import group_install_exception_handlers
from app.interface.error_handlers.permissions.error_handlers import permission_install_exception_handlers
from app.interface.error_handlers.user.error_handlers import user_install_exception_handlers
from app.shared.errors.dto import ErrorResponseDto
from app.shared.errors.enums import ErrorCode


def grouping_install_exception_handlers(app: FastAPI) -> None:
    user_install_exception_handlers(app=app)
    group_install_exception_handlers(app=app)
    permission_install_exception_handlers(app=app)

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