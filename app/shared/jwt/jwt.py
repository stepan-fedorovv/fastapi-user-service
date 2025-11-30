from app.shared.jwt.classes import AuthJWTWithPermission as AuthJWT

from app.shared.jwt.settings import Settings


def load_jwt_config() -> Settings:
    @AuthJWT.load_config
    def get_config():
        return Settings()
