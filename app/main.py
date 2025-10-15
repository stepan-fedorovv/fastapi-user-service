from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.errors.error_handlers import install_exception_handlers
from app.api.router import grouping_router
from app.common.jwt.jwt import load_jwt_config
from app.core import config
from app.db.setup import dispose_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await dispose_engine()


def get_application() -> FastAPI:
    application = FastAPI(
        debug=config.DEBUG,
        title="User Service",
        summary="User service api for interactions with it",
        description="",
        version=config.VERSION,
        redirect_slashes=True,
        lifespan=lifespan
    )
    load_jwt_config()
    install_exception_handlers(application)
    application.include_router(grouping_router)

    return application


app = get_application()