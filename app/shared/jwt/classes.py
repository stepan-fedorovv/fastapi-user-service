from datetime import timedelta
from typing import Optional, Callable, List

from another_fastapi_jwt_auth import AuthJWT
from another_fastapi_jwt_auth.auth_config import AuthConfig
from another_fastapi_jwt_auth.config import LoadConfig
from pydantic import ValidationError, StrictStr
from starlette.websockets import WebSocket

from app.shared.errors.enums import ErrorCode
from app.shared.errors.error_classes import PermissionDenied


class PermissionLoadConfig(LoadConfig):
    authjwt_permissions_field: Optional[StrictStr] = "permissions"


class PermissionAuthConfig(AuthConfig):
    _permissions_field = None
    _token = None
    _token_location = {"headers"}

    _secret_key = None
    _public_key = None
    _private_key = None
    _algorithm = "HS256"
    _decode_algorithms = None
    _decode_leeway = 0
    _encode_issuer = None
    _decode_issuer = None
    _decode_audience = None
    _denylist_enabled = False
    _denylist_token_checks = {"access", "refresh"}
    _header_name = "Authorization"
    _header_type = "Bearer"
    _token_in_denylist_callback = None
    _access_token_expires = timedelta(minutes=15)
    _refresh_token_expires = timedelta(days=30)

    # option for create cookies
    _access_cookie_key = "access_token_cookie"
    _refresh_cookie_key = "refresh_token_cookie"
    _access_cookie_path = "/"
    _refresh_cookie_path = "/"
    _cookie_max_age = None
    _cookie_domain = None
    _cookie_secure = False
    _cookie_samesite = None

    # option for double submit csrf protection
    _cookie_csrf_protect = True
    _access_csrf_cookie_key = "csrf_access_token"
    _refresh_csrf_cookie_key = "csrf_refresh_token"
    _access_csrf_cookie_path = "/"
    _refresh_csrf_cookie_path = "/"
    _access_csrf_header_name = "X-CSRF-Token"
    _refresh_csrf_header_name = "X-CSRF-Token"
    _csrf_methods = {"POST", "PUT", "PATCH", "DELETE"}

    @property
    def jwt_in_cookies(self) -> bool:
        return "cookies" in self._token_location

    @property
    def jwt_in_headers(self) -> bool:
        return "headers" in self._token_location

    @classmethod
    def load_config(cls, settings: Callable[..., List[tuple]]) -> "AuthConfig":
        try:
            config = PermissionLoadConfig(
                **{key.lower(): value for key, value in settings()}
            )
            cls._permissions_field = config.authjwt_permissions_field
            cls._token_location = config.authjwt_token_location
            cls._secret_key = config.authjwt_secret_key
            cls._public_key = config.authjwt_public_key
            cls._private_key = config.authjwt_private_key
            cls._algorithm = config.authjwt_algorithm
            cls._decode_algorithms = config.authjwt_decode_algorithms
            cls._decode_leeway = config.authjwt_decode_leeway
            cls._encode_issuer = config.authjwt_encode_issuer
            cls._decode_issuer = config.authjwt_decode_issuer
            cls._decode_audience = config.authjwt_decode_audience
            cls._denylist_enabled = config.authjwt_denylist_enabled
            cls._denylist_token_checks = config.authjwt_denylist_token_checks
            cls._header_name = config.authjwt_header_name
            cls._header_type = config.authjwt_header_type
            cls._access_token_expires = config.authjwt_access_token_expires
            cls._refresh_token_expires = config.authjwt_refresh_token_expires
            # option for create cookies
            cls._access_cookie_key = config.authjwt_access_cookie_key
            cls._refresh_cookie_key = config.authjwt_refresh_cookie_key
            cls._access_cookie_path = config.authjwt_access_cookie_path
            cls._refresh_cookie_path = config.authjwt_refresh_cookie_path
            cls._cookie_max_age = config.authjwt_cookie_max_age
            cls._cookie_domain = config.authjwt_cookie_domain
            cls._cookie_secure = config.authjwt_cookie_secure
            cls._cookie_samesite = config.authjwt_cookie_samesite
            # option for double submit csrf protection
            cls._cookie_csrf_protect = config.authjwt_cookie_csrf_protect
            cls._access_csrf_cookie_key = config.authjwt_access_csrf_cookie_key
            cls._refresh_csrf_cookie_key = config.authjwt_refresh_csrf_cookie_key
            cls._access_csrf_cookie_path = config.authjwt_access_csrf_cookie_path
            cls._refresh_csrf_cookie_path = config.authjwt_refresh_csrf_cookie_path
            cls._access_csrf_header_name = config.authjwt_access_csrf_header_name
            cls._refresh_csrf_header_name = config.authjwt_refresh_csrf_header_name
            cls._csrf_methods = config.authjwt_csrf_methods
        except ValidationError:
            raise
        except Exception:
            raise TypeError("Config must be pydantic 'BaseSettings' or list of tuple")

    @classmethod
    def token_in_denylist_loader(cls, callback: Callable[..., bool]) -> "AuthConfig":
        cls._token_in_denylist_callback = callback


class AuthJWTWithPermission(
    AuthJWT,
    PermissionAuthConfig,
):
    @staticmethod
    def has_permission(
        required_permissions: list[str], user_permissions: list[str]
    ) -> bool:
        user_permissions = set(user_permissions)
        required_permissions = set(required_permissions)
        if required_permissions.issubset(user_permissions):
            return True
        return False

    def jwt_required(
        self,
        auth_from: str = "request",
        token: Optional[str] = None,
        websocket: Optional[WebSocket] = None,
        csrf_token: Optional[str] = None,
        required_permissions: set[str] | None = None,
    ) -> None:
        super().jwt_required(
            auth_from=auth_from,
            token=token,
            websocket=websocket,
            csrf_token=csrf_token,
        )
        if required_permissions:
            raw_jwt = self.get_raw_jwt()
            user_permissions = raw_jwt.get(self._permissions_field, None)

            if user_permissions is None:
                raise PermissionDenied(
                    detail="Permission field not found in claims",
                    errors={
                        "field": "permissions",
                        "message": "Permission denied",
                        "code": ErrorCode.PERMISSION_DENIED,
                    },
                )
            if not self.has_permission(
                required_permissions=required_permissions,
                user_permissions=user_permissions,
            ):
                raise PermissionDenied(
                    detail="Permission denied",
                    errors={
                        "field": "permissions",
                        "message": "Permission denied",
                        "code": ErrorCode.PERMISSION_DENIED,
                    },
                )
