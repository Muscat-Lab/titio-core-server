from uuid import UUID

from pydantic import BaseModel

from src.enums.like import LikeChoiceType


class LikeChoiceSchema(BaseModel):
    id: UUID
    type: LikeChoiceType
    name: str
    profile_image_url: str | None
