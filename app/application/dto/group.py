from pydantic import BaseModel


class GroupDto(BaseModel):
    id: int | None = None
    name: str | None = None
    permissions_code_names: list[str] | None = None
