from uuid import UUID

from fastapi import Depends, HTTPException

from src.models.model import SeatGrade
from src.repositories.performance import PerformanceRepository
from src.repositories.seat_grade import SeatGradeRepository


class SeatGradeService:
    def __init__(
        self,
        performance_repository=Depends(PerformanceRepository),
        seat_grade_repository=Depends(SeatGradeRepository),
    ):
        self.performance_repository = performance_repository
        self.seat_grade_repository = seat_grade_repository

    async def get_seat_grade_list(
        self, performance_id: UUID, limit: int, cursor: str | None = None
    ) -> list[SeatGrade]:
        performance = await self.performance_repository.find_performance_by_id(
            performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        return await self.seat_grade_repository.get_seat_grade_list(
            performance_id=performance_id, limit=limit, cursor=cursor
        )

    async def save_seat_grade(self, seat_grade) -> SeatGrade:
        return await self.seat_grade_repository.save_seat_grade(seat_grade)
