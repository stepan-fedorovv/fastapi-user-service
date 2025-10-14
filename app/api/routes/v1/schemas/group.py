from app.common.dto import BaseDto


class GroupResponseSchema(BaseDto):
    id: int
    name: str