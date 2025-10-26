from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.core import config
from app.infrastructure.db.setup import engine
from app.infrastructure.di import build_container
from app.interface.error_handlers.grouping_erros import grouping_install_exception_handlers
from app.interface.router import grouping_router
from app.shared.jwt.jwt import load_jwt_config

container = build_container()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()
    await container.close()


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
    grouping_install_exception_handlers(application)
    application.include_router(grouping_router)
    add_pagination(application)
    setup_dishka(container, application)
    return application


app = get_application()