from uuid import UUID

from fastapi import Depends

from src.models.model import Casting
from src.repositories.casting import CastingRepository
from src.repositories.performance import PerformanceRepository


class CastingService:
    def __init__(
        self,
        performance_repository=Depends(PerformanceRepository),
        casting_repository=Depends(CastingRepository),
    ):
        self.performance_repository = performance_repository
        self.casting_repository = casting_repository

    async def get_casting_list(
        self,
        performance_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> list[Casting]:
        return await self.casting_repository.get_casting_list(
            performance_id=performance_id, limit=limit, cursor=cursor
        )

    async def save_casting(self, casting: Casting) -> Casting:
        return await self.casting_repository.save_casting(casting)
