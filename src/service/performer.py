from uuid import UUID

from fastapi import Depends

from src.models.model import Performer
from src.repositories.performance import PerformanceRepository
from src.repositories.performer import PerformerRepository
from src.repositories.user import UserRepository


class PerformerService:
    def __init__(
        self,
        performance_repository: PerformanceRepository = Depends(PerformanceRepository),
        performer_repository: PerformerRepository = Depends(PerformerRepository),
        user_repository: UserRepository = Depends(UserRepository),
    ):
        self.performance_repository = performance_repository
        self.performer_repository = performer_repository
        self.user_repository = user_repository

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

    async def like_performer(self, performer_id: UUID, user_id: UUID):
        await self.user_repository.like_performers(
            performer_ids=[performer_id],
            user_id=user_id,
        )

    async def unlike_performer(self, performer_id: UUID, user_id: UUID):
        await self.user_repository.unlike_performer(
            performer_id=performer_id,
            user_id=user_id,
        )
