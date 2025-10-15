import pydantic
from fastapi_jwt_auth import AuthJWT

from app.common.jwt.settings import Settings
from app.core import config

def load_jwt_config() -> Settings:
    @AuthJWT.load_config
    def get_config():
        return Settings()