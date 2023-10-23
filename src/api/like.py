import json

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase
from src.schema.like import LikeChoiceSchema
from src.service.like import LikeService

router = APIRouter(
    prefix="/likes",
    tags=["like"],
)


class LikeChoiceListRequest(ListRequestBase):
    pass


class LikeChoiceListResponse(ListResponseBase):
    choices: list[LikeChoiceSchema]


@router.get("/choices")
async def like_choices_handler(
    q: LikeChoiceListRequest = Depends(),
    like_service: LikeService = Depends(),
) -> LikeChoiceListResponse:
    return LikeChoiceListResponse(
        choices=[
            LikeChoiceSchema.model_validate(
                json.loads(performer),
                from_attributes=True,
            )
            for performer in await like_service.get_like_choice_list(
                limit=q.limit,
                cursor=q.cursor,
            )
        ],
        next_cursor=str(int(q.cursor) + 1 if q.cursor is not None else 1),
    )
