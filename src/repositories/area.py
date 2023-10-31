from uuid import UUID

from fastapi import Depends
from sqlalchemy import select

from src.database.connection import get_db
from src.models.model import Area


class AreaRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def get_area_list(
        self,
        performance_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> list[Area]:
        query = select(Area, Area.accessible_seats_count).where(
            Area.performance_id == performance_id
        )

        if cursor is not None:
            query = query.where(Area.created_at < cursor)

        result = (
            await self.session.execute(
                query.order_by(Area.created_at.desc()).limit(limit)
            )
        ).all()

        for area, accessible_seats_count in result:
            area.accessible_seats_count = accessible_seats_count

        return [area for area, accessible_seats_count in result]

    async def find_area_by_id(self, area_id: UUID) -> Area | None:
        query = select(Area).where(Area.id == area_id)

        return (await self.session.scalars(query)).first()

    async def save_area(self, area: Area) -> Area:
        self.session.add(instance=area)
        await self.session.commit()
        await self.session.refresh(instance=area)

        return area
