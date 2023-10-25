import json
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.auth.jwt_handler import get_current_user
from src.schema.like import LikeChoiceSchema, LikeChoiceCreateSchema
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
async def like_choice_list_handler(
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
        next_cursor=str(int(q.cursor) + q.limit if q.cursor is not None else q.limit),
    )


class LikeChoiceBulkCreateRequest(RequestBase):
    choices: list[LikeChoiceCreateSchema]


class LikeChoiceBulkCreateResponse(ResponseBase):
    pass


@router.post("/choices/bulk")
async def like_choice_bulk_create_handler(
    q: LikeChoiceBulkCreateRequest,
    like_service: LikeService = Depends(),
    user_id: UUID = Depends(get_current_user),
) -> LikeChoiceBulkCreateResponse:
    await like_service.bulk_create_like_choice(
        choices=q.choices,
        user_id=user_id,
    )

    return LikeChoiceBulkCreateResponse()


@router.post("/choices/flush")
async def like_choice_flush_handler(
    like_service: LikeService = Depends(),
) -> LikeChoiceBulkCreateResponse:
    await like_service.flush_like_choice()

    return LikeChoiceBulkCreateResponse()