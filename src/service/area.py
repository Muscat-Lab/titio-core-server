from fastapi import Depends, HTTPException

from src.models.model import Area
from src.repositories.area import AreaRepository
from src.repositories.performance import PerformanceRepository


class AreaService:
    def __init__(
        self,
        area_repository=Depends(AreaRepository),
        performance_repository=Depends(PerformanceRepository),
    ):
        self.area_repository = area_repository
        self.performance_repository = performance_repository

    async def get_area_list(
        self, performance_id, limit: int, cursor: str | None = None
    ) -> list[Area]:
        performance = await self.performance_repository.find_performance_by_id(
            performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        return await self.area_repository.get_area_list(
            performance_id, limit=limit, cursor=cursor
        )

    async def save_area(self, area) -> Area:
        performance = await self.performance_repository.find_performance_by_id(
            area.performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        return await self.area_repository.save_area(area)
