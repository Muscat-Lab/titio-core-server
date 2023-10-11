from uuid import UUID

from fastapi import Depends, HTTPException

from src.models.model import Role
from src.repositories.performance import PerformanceRepository
from src.repositories.role import RoleRepository


class RoleService:
    def __init__(
        self,
        performance_repository=Depends(PerformanceRepository),
        role_repository=Depends(RoleRepository),
    ):
        self.performance_repository = performance_repository
        self.role_repository = role_repository

    async def get_role_list(
        self,
        performance_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> list[Role]:
        performance = await self.performance_repository.find_performance_by_id(
            performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        return await self.role_repository.get_role_list(
            performance_id, limit=limit, cursor=cursor
        )

    async def save_role(self, role: Role) -> Role:
        performance = await self.performance_repository.find_performance_by_id(
            role.performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        return await self.role_repository.save_role(role)
