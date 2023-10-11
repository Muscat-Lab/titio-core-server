from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.models.model import Area


class AreaRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def get_area_list(
        self,
        performance_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> list[Area]:
        query = select(Area).where(Area.performance_id == performance_id)

        if cursor is not None:
            query = query.where(Area.created_at < cursor)

        return list(
            (
                self.session.scalars(
                    query.order_by(Area.latest_cursor.desc()).limit(limit)
                )
            ).all()
        )

    async def find_area_by_id(self, area_id: UUID) -> Area | None:
        return self.session.scalars(select(Area).where(Area.id == area_id)).first()

    async def save_area(self, area: Area) -> Area:
        self.session.add(instance=area)
        self.session.commit()
        self.session.refresh(instance=area)

        return area
