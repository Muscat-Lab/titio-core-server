from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.database.connection import get_db
from src.models.model import Casting


class CastingRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def get_casting_list(
        self,
        performance_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> list[Casting]:
        query = (
            select(Casting)
            .options(
                joinedload(Casting.performer),
                joinedload(Casting.role),
            )
            .where(Casting.performance_id == performance_id)
        )

        if cursor is not None:
            query = query.where(Casting.created_at < cursor)

        query = query.order_by(Casting.created_at.desc()).limit(limit)

        return list((await self.session.execute(query)).scalars().all())

    async def save_casting(self, casting: Casting) -> Casting:
        self.session.add(casting)
        await self.session.commit()
        await self.session.refresh(casting)

        return casting
