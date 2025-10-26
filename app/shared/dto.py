from pydantic import BaseModel, ConfigDict


class BaseDto(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        from_attributes=True
    )