import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import Field

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.models.model import Performance
from src.service.performance import PerformanceService

router = APIRouter(prefix="/performances", tags=["performance"])


class PerformanceListRequest(ListRequestBase):
    pre_booking_enabled: bool | None = Query(None)


class PerformanceListResponse(ListResponseBase):
    class Performance(ResponseBase):
        id: UUID
        title: str
        running_time: str
        grade: str
        begin: datetime.date
        end: datetime.date
        pre_booking_enabled: bool
        pre_booking_closed_at: datetime.datetime | None = None

    performances: list[Performance]


@router.get("")
async def performance_list_handler(
    q: PerformanceListRequest = Depends(),
    performance_service: PerformanceService = Depends(),
) -> PerformanceListResponse:
    performances = await performance_service.get_performance_list(
        limit=q.limit,
        cursor=q.cursor,
        pre_booking_enabled=q.pre_booking_enabled,
    )

    return PerformanceListResponse(
        performances=[
            PerformanceListResponse.Performance.model_validate(
                performance, from_attributes=True
            )
            for performance in performances
        ],
        next_cursor=performances[-1].latest_cursor if performances else None,
    )


class PerformanceCreateRequest(RequestBase):
    title: str = Field(max_length=50)
    running_time: str = Field(max_length=30)
    grade: str = Field(max_length=30)
    begin: datetime.date
    end: datetime.date
    pre_booking_enabled: bool
    pre_booking_closed_at: datetime.datetime | None = None


class PerformanceCreateResponse(ResponseBase):
    id: UUID
    title: str
    running_time: str
    grade: str
    begin: datetime.date
    end: datetime.date
    pre_booking_enabled: bool
    pre_booking_closed_at: datetime.datetime | None = None


@router.post("")
async def performance_create_handler(
    q: PerformanceCreateRequest,
    performance_service: PerformanceService = Depends(),
) -> PerformanceCreateResponse:
    return PerformanceCreateResponse.model_validate(
        await performance_service.save_performance(
            Performance.create(
                title=q.title,
                running_time=q.running_time,
                grade=q.grade,
                begin=q.begin,
                end=q.end,
                pre_booking_enabled=q.pre_booking_enabled,
                pre_booking_closed_at=q.pre_booking_closed_at,
            )
        ),
        from_attributes=True,
    )


class PerformanceUpdateRequest(PerformanceCreateRequest):
    pass


class PerformanceUpdateResponse(PerformanceCreateResponse):
    pass


@router.put("/{performanceId}")
async def performance_update_handler(
    q: PerformanceUpdateRequest,
    performanceId: UUID,
    performance_service: PerformanceService = Depends(),
) -> PerformanceUpdateResponse:
    return PerformanceUpdateResponse.model_validate(
        await performance_service.save_performance(
            Performance(
                id=performanceId,
                title=q.title,
                running_time=q.running_time,
                grade=q.grade,
                begin=q.begin,
                end=q.end,
                pre_booking_enabled=q.pre_booking_enabled,
                pre_booking_closed_at=q.pre_booking_closed_at,
            ),
        )
    )


@router.delete("/{performanceId}")
async def performance_delete_handler(
    performanceId: UUID,
    performance_service: PerformanceService = Depends(),
) -> ResponseBase:
    await performance_service.delete_performance(performanceId)

    return ResponseBase()
