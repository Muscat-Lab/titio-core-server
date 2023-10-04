from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class RequestBase(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

class ResponseBase(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
