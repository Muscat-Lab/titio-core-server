from typing import Type
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.models.model import Performance


class PerformanceRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def save_performance(self, performance: Performance) -> Performance:
        self.session.add(instance=performance)
        self.session.commit()
        self.session.refresh(instance=performance)

        return performance

    async def get_performance_list(
        self,
        limit: int,
        cursor: str | None = None,
        pre_booking_enabled: bool | None = None,
    ) -> list[Performance]:
        query = select(Performance)

        if pre_booking_enabled is not None:
            query = query.where(Performance.pre_booking_enabled == pre_booking_enabled)

        if cursor is not None:
            query = query.where(Performance.created_at < cursor)

        return list(
            (
                self.session.scalars(
                    query.order_by(Performance.latest_cursor.desc()).limit(limit)
                )
            ).all()
        )

    async def delete_performance(self, performance_id: UUID):
        self.session.query(Performance).where(Performance.id == performance_id).delete()
        self.session.commit()

    async def find_performance_by_id(self, performance_id: UUID) -> Performance | None:
        return (
            self.session.query(Performance)
            .where(Performance.id == performance_id)
            .first()
        )
