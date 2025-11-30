
from app.shared.dto import BaseDto
from app.core import config


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_private_key() -> str:
    path = config.AUTHJWT_PRIVATE_KEY_PATH
    if not path:
        raise RuntimeError("Missing AUTHJWT_PRIVATE_KEY_PATH")
    return _read_text(path)


def load_public_key() -> str:
    path = config.AUTHJWT_PUBLIC_KEY_PATH
    if not path:
        raise RuntimeError("Missing AUTHJWT_PUBLIC_KEY{_PATH}")
    return _read_text(path)


class Settings(BaseDto):
    authjwt_algorithm: str = "RS256"
    authjwt_token_location: set[str] = {"headers"}
    authjwt_decode_algorithms: set[str] = {"RS256"}
    authjwt_header_name: str = "Authorization"
    authjwt_header_type: str = "Bearer"
    authjwt_public_key: str = load_public_key()
    authjwt_private_key: str = load_private_key()
    authjwt_decode_audience: str | list[str] | None = config.JWT_AUD
