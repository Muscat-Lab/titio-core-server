from uuid import UUID

from pydantic import BaseModel

from src.enums.like import LikeChoiceType


class LikeChoiceSchema(BaseModel):
    class Genre(BaseModel):
        id: UUID
        name: str

    class Performer(BaseModel):
        id: UUID
        name: str
        profile_image_url: str | None

    type: LikeChoiceType
    genre: Genre | None
    performer: Performer | None
