from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class RequestBase(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ListRequestBase(RequestBase):
    limit: int = Field(20, ge=1, le=20)
    cursor: str | None = Field(None, max_length=100)


class ResponseBase(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ListResponseBase(ResponseBase):
    next_cursor: str | None = None
