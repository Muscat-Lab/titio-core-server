from datetime import date, time
from uuid import UUID

from fastapi import Depends, HTTPException

from src.models.model import Schedule, ScheduleCasting
from src.repositories.performance import PerformanceRepository
from src.repositories.schedule import ScheduleRepository


class ScheduleService:
    def __init__(
        self,
        performance_repository=Depends(PerformanceRepository),
        schedule_repository=Depends(ScheduleRepository),
    ):
        self.performance_repository = performance_repository
        self.schedule_repository = schedule_repository

    async def get_date_list(
        self,
        performance_id: UUID,
        from_date: date | None = None,
        to_date: date | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> list[date]:
        performance = await self.performance_repository.find_performance_by_id(
            performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        return await self.schedule_repository.get_date_list(
            performance_id=performance_id,
            from_date=from_date,
            to_date=to_date,
            cursor=cursor,
            limit=limit,
        )

    async def get_time_list_by_date(
        self,
        performance_id: UUID,
        _date: date,
        from_time: time | None = None,
        to_time: time | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> list[time]:
        performance = await self.performance_repository.find_performance_by_id(
            performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        return await self.schedule_repository.get_time_list_by_date(
            performance_id=performance_id,
            _date=_date,
            from_time=from_time,
            to_time=to_time,
            cursor=cursor,
            limit=limit,
        )

    async def find_schedule_by_date_n_time(
        self,
        performance_id: UUID,
        _date: date,
        _time: time,
    ) -> Schedule:
        performance = await self.performance_repository.find_performance_by_id(
            performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        schedule = await self.schedule_repository.find_schedule_by_date_n_time(
            performance_id=performance_id,
            _date=_date,
            _time=_time,
        )

        if schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")

        return schedule

    async def save_schedule_list(
        self,
        schedule_list: list[Schedule],
    ) -> list[Schedule]:
        return await self.schedule_repository.save_schedule_list(schedule_list)

    async def save_schedule_casting(
        self,
        schedule_casting: ScheduleCasting,
    ) -> Schedule:
        return await self.schedule_repository.save_schedule_casting(schedule_casting)
