import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ResponseBase, ListRequestBase, ListResponseBase

router = APIRouter(prefix="/castings", tags=["casting"])


class CastingListRequest(ListRequestBase):
    performance_id: UUID


class CastingListResponse(ListResponseBase):
    class Casting(ResponseBase):
        id: UUID
        performer_name: str
        performer_id: UUID
        role_name: str
        role_id: UUID
        profile_url: str

    castings: list[Casting]


@router.get("")
async def casting_list_handler(
    q: CastingListRequest = Depends(),
) -> CastingListResponse:
    return CastingListResponse(
        castings=[
            CastingListResponse.Casting(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                performer_name="performer_name1",
                performer_id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                role_name="role_name1",
                role_id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                profile_url="https://www.edureka.co/blog/golang-tutorial/#var",
            ),
            CastingListResponse.Casting(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1b"),
                performer_name="performer_name2",
                performer_id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1b"),
                role_name="role_name2",
                role_id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1b"),
                profile_url="https://www.edureka.co/blog/golang-tutorial/#var",
            ),
        ],
        next_cursor=None,
    )
