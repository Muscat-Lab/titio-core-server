import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import Field

from src.api.request import ResponseBase, RequestBase
from src.models.model import Performance
from src.service.performance import PerformanceService

router = APIRouter(prefix="/performances", tags=["performance"])


class PerformanceListRequest(RequestBase):
    pre_booking_enabled: bool | None = Query(None)


class PerformanceResponse(ResponseBase):
    id: UUID
    title: str
    running_time: str
    grade: str
    begin: datetime.date
    end: datetime.date
    pre_booking_enabled: bool
    pre_booking_closed_at: datetime.datetime | None = None


@router.get("")
async def performance_list_handler(
    q: PerformanceListRequest = Depends(),
    performance_service: PerformanceService = Depends(),
) -> list[PerformanceResponse]:
    return [
        PerformanceResponse.model_validate(performance, from_attributes=True)
        for performance in await performance_service.get_performance_list(
            pre_booking_enabled=q.pre_booking_enabled
        )
    ]


class PerformanceCreateRequest(RequestBase):
    title: str = Field(max_length=50)
    running_time: str = Field(max_length=30)
    grade: str = Field(max_length=30)
    begin: datetime.date
    end: datetime.date
    pre_booking_enabled: bool
    pre_booking_closed_at: datetime.datetime | None = None


@router.post("")
async def performance_create_handler(
    q: PerformanceCreateRequest,
    performance_service: PerformanceService = Depends(),
) -> PerformanceResponse:
    return PerformanceResponse.model_validate(
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


@router.put("/{performanceId}")
async def performance_update_handler(
    q: PerformanceUpdateRequest,
    performanceId: UUID,
    performance_service: PerformanceService = Depends(),
) -> PerformanceResponse:
    return PerformanceResponse.model_validate(
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
