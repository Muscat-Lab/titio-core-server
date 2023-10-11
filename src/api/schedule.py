import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.models.model import Schedule, ScheduleCasting
from src.service.schedule import ScheduleService

router = APIRouter(prefix="/schedules", tags=["schedule"])


class ScheduleDateListRequest(ListRequestBase):
    performance_id: UUID
    from_date: datetime.date | None = None
    to_date: datetime.date | None = None


class ScheduleDateListResponse(ListResponseBase):
    dates: list[datetime.date]
    next_cursor: str | None = None


@router.get("/dates")
async def schedule_date_list_handler(
    q: ScheduleDateListRequest = Depends(),
    schedule_service: ScheduleService = Depends(),
) -> ScheduleDateListResponse:
    dates = await schedule_service.get_date_list(
        performance_id=q.performance_id,
        from_date=q.from_date,
        to_date=q.to_date,
        cursor=q.cursor,
        limit=q.limit,
    )

    return ScheduleDateListResponse(
        dates=dates,
        next_cursor=str(dates[-1]) if len(dates) == q.limit else None,
    )


class ScheduleTimeListRequest(ListRequestBase):
    performance_id: UUID
    date: datetime.date
    from_time: datetime.time | None = None
    to_time: datetime.time | None = None


class ScheduleTimeListResponse(ListResponseBase):
    times: list[datetime.time]


@router.get("/times")
async def schedule_time_list_handler(
    q: ScheduleTimeListRequest = Depends(),
    schedule_service: ScheduleService = Depends(),
) -> ScheduleTimeListResponse:
    times = await schedule_service.get_time_list_by_date(
        performance_id=q.performance_id,
        _date=q.date,
        from_time=q.from_time,
        to_time=q.to_time,
        cursor=q.cursor,
        limit=q.limit,
    )

    return ScheduleTimeListResponse(
        times=times,
        next_cursor=str(times[-1]) if len(times) == q.limit else None,
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


@router.get("/byDatetime")
async def schedule_by_datetime_handler(
    q: ScheduleByDatetimeRequest = Depends(),
    schedule_service: ScheduleService = Depends(),
) -> ScheduleByDatetimeResponse:
    schedule = await schedule_service.find_schedule_by_date_n_time(
        performance_id=q.performance_id,
        _date=datetime.datetime.strptime(q.date, "%Y-%m-%d").date(),
        _time=datetime.datetime.strptime(q.time, "%H:%M:%S").time(),
    )

    return ScheduleByDatetimeResponse(
        id=schedule.id,
        date=schedule.date,
        time=schedule.time,
        performers=[
            ScheduleByDatetimeResponse.Performer(
                id=casting.casting.performer.id,
                name=casting.casting.performer.name,
            )
            for casting in schedule.castings
        ],
    )


class ScheduleBulkByDatetimeRequest(RequestBase):
    performance_id: UUID
    schedules: list[datetime.datetime]


@router.post("/bulk/by_datetime")
async def schedule_bulk_by_datetime_handler(
    q: ScheduleBulkByDatetimeRequest,
    schedule_service: ScheduleService = Depends(),
) -> ResponseBase:
    await schedule_service.save_schedule_list(
        schedule_list=[
            Schedule.create(
                performance_id=q.performance_id,
                date=schedule.date(),
                time=schedule.time().replace(microsecond=0),
            )
            for schedule in q.schedules
        ]
    )

    return ResponseBase()


class ScheduleCastingCreateRequest(RequestBase):
    casting_id: UUID


@router.post("/{scheduleId}/casting")
async def schedule_casting_create_handler(
    scheduleId: UUID,
    q: ScheduleCastingCreateRequest,
    schedule_service: ScheduleService = Depends(),
) -> ResponseBase:
    await schedule_service.save_schedule_casting(
        ScheduleCasting.create(
            schedule_id=scheduleId,
            casting_id=q.casting_id,
        )
    )

    return ResponseBase()
