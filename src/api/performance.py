import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import ConfigDict, BaseModel, Field
from pydantic.alias_generators import to_camel

from src.models.model import Performance
from src.service.performance import PerformanceService

router = APIRouter(prefix="/performances", tags=["performance"])


class PerformanceResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

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
    performance_service: PerformanceService = Depends(),
) -> list[PerformanceResponse]:
    return [
        PerformanceResponse.model_validate(performance, from_attributes=True)
        for performance in await performance_service.get_performance_list()
    ]


class PerformanceSaveRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    title: str = Field(max_length=50)
    running_time: str = Field(max_length=30)
    grade: str = Field(max_length=30)
    begin: datetime.date
    end: datetime.date
    pre_booking_enabled: bool
    pre_booking_closed_at: datetime.datetime | None = None

@router.post("")
async def performance_save_handler(
    q: PerformanceSaveRequest,
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