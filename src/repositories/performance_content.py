from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.models.model import PerformanceContent


class PerformanceContentRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def save_performance_content(
        self, performance_content: PerformanceContent
    ) -> PerformanceContent:
        self.session.add(instance=performance_content)
        self.session.commit()
        self.session.refresh(instance=performance_content)

        return performance_content

    async def get_performance_content_list(
        self,
        performance_id: UUID,
        limit: int = 20,
        cursor: str | None = None,
    ) -> list[PerformanceContent]:
        query = select(PerformanceContent).where(
            PerformanceContent.performance_id == performance_id
        )

        if cursor is not None:
            query = query.where(PerformanceContent.created_at < cursor)

        return list(
            (
                self.session.scalars(
                    query.order_by(PerformanceContent.created_at.desc()).limit(limit)
                )
            ).all()
        )
