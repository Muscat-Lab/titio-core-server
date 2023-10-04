from uuid import UUID

from fastapi import APIRouter

from src.api.request import ListResponseBase, ResponseBase, ListRequestBase

router = APIRouter(prefix="/areas", tags=["area"])


class AreaListRequest(ListRequestBase):
    performance_id: UUID


class AreaListResponse(ListResponseBase):
    class Area(ResponseBase):
        id: UUID
        title: str

    areas: list[Area]


@router.get("")
async def area_list_handler() -> AreaListResponse:
    return AreaListResponse(
        areas=[
            AreaListResponse.Area(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                title="area1",
            ),
            AreaListResponse.Area(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1b"),
                title="area2",
            ),
        ],
        next_cursor=None,
    )
