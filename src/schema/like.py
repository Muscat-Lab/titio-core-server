from uuid import UUID

from src.api.request import RequestBase
from src.enums.like import LikeChoiceType


class LikeChoiceSchema(RequestBase):
    id: UUID
    type: LikeChoiceType
    name: str
    profile_image_url: str | None


class LikeChoiceCreateSchema(RequestBase):
    id: UUID
    type: LikeChoiceType
