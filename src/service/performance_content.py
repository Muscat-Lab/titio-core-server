from uuid import UUID

from fastapi import Depends, HTTPException

from src.models.model import PerformanceContent
from src.repositories.performance import PerformanceRepository
from src.repositories.performance_content import PerformanceContentRepository


class PerformanceContentService:
    def __init__(
        self,
        performance_repository: PerformanceRepository = Depends(PerformanceRepository),
        performance_content_repository: PerformanceContentRepository = Depends(
            PerformanceContentRepository
        ),
    ):
        self.performance_repository = performance_repository
        self.performance_content_repository = performance_content_repository

    async def save_performance_content(
        self, performance_content: PerformanceContent
    ) -> PerformanceContent:
        performance = await self.performance_repository.find_performance_by_id(
            performance_content.performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        return await self.performance_content_repository.save_performance_content(
            performance_content
        )

    async def get_performance_content(
        self,
        performance_id: UUID,
    ) -> PerformanceContent:
        return await self.performance_content_repository.get_performance_content(
            performance_id,
        )
