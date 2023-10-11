from datetime import date, time
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.database.connection import get_db
from src.models.model import Casting, Schedule, ScheduleCasting


class ScheduleRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def find_schedule_by_date_n_time(
        self,
        performance_id: UUID,
        _date: date,
        _time: time,
    ) -> Schedule | None:
        query = (
            select(Schedule)
            .options(
                joinedload(Schedule.castings)
                .joinedload(ScheduleCasting.casting)
                .joinedload(Casting.performer),
            )
            .where(Schedule.performance_id == performance_id)
            .where(Schedule.date == _date)
            .where(Schedule.time == _time)
        )

        return self.session.execute(query).unique().scalar_one_or_none()

    async def get_date_list(
        self,
        performance_id: UUID,
        from_date: date | None = None,
        to_date: date | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> list[date]:
        query = (
            select(Schedule.date)
            .where(Schedule.performance_id == performance_id)
            .distinct()
        )

        if from_date is not None:
            query = query.where(Schedule.date >= from_date)

        if to_date is not None:
            query = query.where(Schedule.date <= to_date)

        if cursor is not None:
            query = query.where(Schedule.date > cursor)

        query = query.order_by(Schedule.date.asc()).limit(limit)

        return [_date for _date in self.session.execute(query).scalars().all()]

    async def get_time_list_by_date(
        self,
        performance_id: UUID,
        _date: date,
        from_time: time | None = None,
        to_time: time | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> list[time]:
        query = (
            select(Schedule.time)
            .where(Schedule.performance_id == performance_id)
            .where(Schedule.date == _date)
            .distinct()
        )

        if from_time is not None:
            query = query.where(Schedule.time >= from_time)

        if to_time is not None:
            query = query.where(Schedule.time <= to_time)

        if cursor is not None:
            query = query.where(Schedule.time > cursor)

        query = query.order_by(Schedule.time.asc()).limit(limit)

        return [_time for _time in self.session.execute(query).scalars().all()]

    async def save_schedule_list(
        self,
        schedule_list: list[Schedule],
    ) -> list[Schedule]:
        self.session.add_all(schedule_list)
        self.session.commit()

        list(map(lambda obj: self.session.refresh(obj), schedule_list))

        return schedule_list

    async def save_schedule_casting(
        self, schedule_casting: ScheduleCasting
    ) -> ScheduleCasting:
        self.session.add(schedule_casting)
        self.session.commit()
        self.session.refresh(schedule_casting)

        return schedule_casting
