from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_db
from src.models.model import SeatGrade


class SeatGradeRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_seat_grade_list(
        self,
        performance_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> list[SeatGrade]:
        query = select(
            SeatGrade,
        ).where(
            SeatGrade.performance_id == performance_id,
        )

        if cursor is not None:
            query = query.where(SeatGrade.created_at < cursor)

        return list(
            (
                await self.session.scalars(
                    query.order_by(SeatGrade.snowflake_id.desc()).limit(limit)
                )
            ).all()
        )

    async def save_seat_grade(self, seat_grade: SeatGrade) -> SeatGrade:
        self.session.add(instance=seat_grade)
        await self.session.commit()
        await self.session.refresh(instance=seat_grade)

        return seat_grade
