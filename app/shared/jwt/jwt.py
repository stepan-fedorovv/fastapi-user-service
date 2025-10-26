import pydantic
from another_fastapi_jwt_auth import AuthJWT

from app.shared.jwt.settings import Settings
from app.core import config

def load_jwt_config() -> Settings:
    @AuthJWT.load_config
    def get_config():
        return Settings()