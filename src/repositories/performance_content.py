from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.models.model import PerformanceContent


class PerformanceContentRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def save_performance_content(
        self, performance_content: PerformanceContent
    ) -> PerformanceContent:
        self.session.add(instance=performance_content)
        await self.session.commit()
        await self.session.refresh(instance=performance_content)

        return performance_content

    async def get_performance_content(
        self,
        performance_id: UUID,
    ) -> PerformanceContent:
        query = select(PerformanceContent).where(
            PerformanceContent.performance_id == performance_id
        )

        return (await self.session.execute(query)).scalars().first()
