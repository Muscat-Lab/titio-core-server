from fastapi import Depends

from src.models.model import Performer
from src.repositories.performance import PerformanceRepository
from src.repositories.performer import PerformerRepository


class PerformerService:
    def __init__(
        self,
        performance_repository=Depends(PerformanceRepository),
        performer_repository=Depends(PerformerRepository),
    ):
        self.performance_repository = performance_repository
        self.performer_repository = performer_repository

    async def get_performer_list(
        self,
        limit: int,
        cursor: str | None = None,
    ) -> list[Performer]:
        return await self.performer_repository.get_performer_list(
            limit=limit, cursor=cursor
        )

    async def save_performer(self, performer: Performer) -> Performer:
        return await self.performer_repository.save_performer(performer)
