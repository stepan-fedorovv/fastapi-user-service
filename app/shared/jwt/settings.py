import pydantic

from app.shared.dto import BaseDto
from app.core import config


class Settings(BaseDto):
    authjwt_secret_key: str = pydantic.Field(default=config.APP_SECRET)