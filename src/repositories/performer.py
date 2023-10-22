from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database.connection import get_db
from src.models.model import Performer


class PerformerRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def get_performer_list(
        self,
        limit: int,
        cursor: str | None = None,
    ) -> list[Performer]:
        query = select(Performer)

        if cursor is not None:
            query = query.where(Performer.created_at < cursor)

        query = query.order_by(Performer.created_at.desc()).limit(limit)

        return list((await self.session.execute(query)).scalars().all())

    async def get_performer_list_with_like_count(
        self,
        limit: int,
        cursor: str | None = None,  # Performer.id
    ) -> list[Performer]:
        query = select(Performer).options(
            joinedload(Performer.users),
        )

        if cursor is not None:
            query = query.where(Performer.id < cursor)

        query = query.order_by(Performer.id.desc()).limit(limit)

        return list((await self.session.execute(query)).unique().scalars().all())

    async def save_performer(self, performer: Performer) -> Performer:
        self.session.add(performer)
        await self.session.commit()
        await self.session.refresh(performer)

        return performer
