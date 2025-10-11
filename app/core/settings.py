from functools import lru_cache, cached_property
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")


class APPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra="ignore",
    )
    PROJECT_NAME: str = config("PROJECT_NAME", cast=str, default="UserService")
    VERSION: str = config("VERSION", cast=str, default="1.0.0")

    DEBUG: bool = config("DEBUG", cast=bool, default=True)
    ENV: str = config("ENV", cast=str, default="TEST")

    POSTGRES_SERVER: str = config("POSTGRES_SERVER", cast=str, default="127.0.0.1")
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int, default=5432)
    POSTGRES_USER: str = config("POSTGRES_USER", cast=str, default="fastapi_template")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str, default="fastapi_template")
    POSTGRES_DB: str = config("POSTGRES_DB", cast=str, default="fastapi_template")

    API_ROUTE: str = config("API_ROUTE", cast=str, default="/api")
    API_ROOT_PATH: str = config("API_ROOT_PATH", default="")

    LOGGING_LEVEL: str = config("LOGGING_LEVEL", cast=str, default="INFO")
    LOGGING_SERIALIZE: bool = config("LOGGING_SERIALIZE", cast=bool, default=False)

    HTTP_CLIENT_MAX_ATTEMPTS: int = config(
        "HTTP_CLIENT_MAX_ATTEMPTS", cast=int, default=3
    )
    HTTP_CLIENT_START_TIMEOUT: float = config(
        "HTTP_CLIENT_START_TIMEOUT", cast=float, default=0.1
    )
    HTTP_CLIENT_MAX_TIMEOUT: float = config(
        "HTTP_CLIENT_MAX_TIMEOUT", cast=float, default=30.0
    )
    HTTP_CLIENT_BACKOFF_FACTOR: float = config(
        "HTTP_CLIENT_BACKOFF_FACTOR", cast=float, default=3.0
    )
    HTTP_CLIENT_DNS_MAX_ATTEMPTS: int = config(
        "HTTP_CLIENT_DNS_MAX_ATTEMPTS", cast=int, default=4
    )
    HTTP_CLIENT_DNS_TIMEOUT: float = config(
        "HTTP_CLIENT_DNS_TIMEOUT", cast=float, default=5.0
    )
    HTTP_CLIENT_RAISE_FOR_STATUS: bool = config(
        "HTTP_CLIENT_RAISE_FOR_STATUS", cast=bool, default=False
    )
    HTTP_CLIENT_RETRY_STATUSES: Optional[CommaSeparatedStrings] = config(
        "HTTP_CLIENT_RETRY_STATUSES", cast=CommaSeparatedStrings, default=None
    )
    MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=1)
    MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)

    @cached_property
    def get_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache()
def get_app_settings() -> APPSettings:
    return APPSettings()
