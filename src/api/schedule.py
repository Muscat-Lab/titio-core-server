import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import Field

from src.api.request import RequestBase

router = APIRouter(prefix="/schedules", tags=["schedule"])

class ScheduleDateListRequest(RequestBase):
    performance_id: UUID
    limit: int = Field(20, ge=1, le=20)


class ScheduleDateListResponse(RequestBase):
    dates: list[str]
    next_cursor: str | None = None


@router.get("/dates")
async def schedule_date_list_handler(
    q: ScheduleDateListRequest = Depends(),
) -> ScheduleDateListResponse:
    return ScheduleDateListResponse(
        dates=["2021-01-01", "2021-01-02"],
        next_cursor=None,
    )

class ScheduleTimeListRequest(RequestBase):
    performance_id: UUID
    date: datetime.date
    limit: int = Field(20, ge=1, le=20)


class ScheduleTimeListResponse(RequestBase):
    times: list[datetime.time]
    next_cursor: str | None = None


@router.get("/times")
async def schedule_time_list_handler(
    q: ScheduleTimeListRequest = Depends(),
) -> ScheduleTimeListResponse:
    return ScheduleTimeListResponse(
        times=[
            datetime.time(hour=12, minute=0),
            datetime.time(hour=13, minute=0),
        ],
        next_cursor=None,
    )

class ScheduleByDatetimeRequest(RequestBase):
    performance_id: UUID
    date: str
    time: str


class ScheduleByDatetimeResponse(RequestBase):
    class Performer(RequestBase):
        id: UUID
        name: str

    id: UUID
    date: datetime.date
    time: datetime.time
    performers: list[Performer]


@router.get("/by_datetime")
async def schedule_by_datetime_handler(
    q: ScheduleByDatetimeRequest = Depends(),
) -> ScheduleByDatetimeResponse:
    return ScheduleByDatetimeResponse(
        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b11"),
        performance_id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0111"),
        date="2021-01-01",
        time="12:00",
        performers=[
            ScheduleByDatetimeResponse.Performer(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b111111"),
                name="performer_name1",
            ),
            ScheduleByDatetimeResponse.Performer(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a01111111"),
                name="performer_name2",
            ),
        ],
    )