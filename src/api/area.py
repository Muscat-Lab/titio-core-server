from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.models.model import Area
from src.service.area import AreaService

router = APIRouter(prefix="/areas", tags=["area"])


class AreaListRequest(ListRequestBase):
    performance_id: UUID


class AreaListResponse(ListResponseBase):
    class Area(ResponseBase):
        id: UUID
        title: str

    areas: list[Area]


@router.get("")
async def area_list_handler(
    q: AreaListRequest = Depends(),
    area_service: AreaService = Depends(),
) -> AreaListResponse:
    areas = await area_service.get_area_list(
        performance_id=q.performance_id,
        limit=q.limit,
        cursor=q.cursor,
    )

    return AreaListResponse(
        areas=[
            AreaListResponse.Area.model_validate(area, from_attributes=True)
            for area in areas
        ],
        next_cursor=str(areas[-1].snowflake_id) if len(areas) >= q.limit else None,
    )


class AreaSaveRequest(RequestBase):
    performance_id: UUID
    title: str

    @property
    def model(self) -> Area:
        return Area.create(
            performance_id=self.performance_id,
            title=self.title,
        )


class AreaSaveResponse(ResponseBase):
    performance_id: UUID
    title: str


@router.post("")
async def area_save_handler(
    q: AreaSaveRequest = Depends(),
    area_service: AreaService = Depends(),
) -> AreaSaveResponse:
    area = await area_service.save_area(area=q.model)

    return AreaSaveResponse.model_validate(area, from_attributes=True)
