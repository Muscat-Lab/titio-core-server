from fastapi import Depends

from src.models.model import Performance
from src.repositories.performance import PerformanceRepository


class PerformanceService:
    def __init__(self, performance_repository=Depends(PerformanceRepository)):
        self.performance_repository = performance_repository

    async def save_performance(self, performance: Performance) -> Performance:
        return await self.performance_repository.save_performance(performance)

    async def get_performance_list(
        self,
        limit: int,
        cursor: str | None = None,
        pre_booking_enabled: bool | None = None,
    ):
        return await self.performance_repository.get_performance_list(
            limit=limit, cursor=cursor, pre_booking_enabled=pre_booking_enabled
        )

    async def delete_performance(self, performance_id):
        return await self.performance_repository.delete_performance(
            performance_id=performance_id
        )
