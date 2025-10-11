from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import grouping_router
from app.core import config
from app.db.setup import dispose_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: можно прогреть коннекты/кэш
    yield
    # shutdown: корректно закрываем пул коннектов
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

    application.include_router(grouping_router)

    return application


app = get_application()