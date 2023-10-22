from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from src.database.connection import get_db
from src.models.model import HotPerformance, Performance, UserPerformanceLike


class PerformanceRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def save_performance(self, performance: Performance) -> Performance:
        self.session.add(instance=performance)
        await self.session.commit()
        await self.session.refresh(instance=performance)

        return performance

    async def get_performance_list(
        self,
        limit: int,
        cursor: str | None = None,
        pre_booking_enabled: bool | None = None,
        genre_ident: str | None = None,
    ) -> list[Performance]:
        query = select(Performance).options(joinedload(Performance.poster_image))

        if pre_booking_enabled is not None:
            query = query.where(Performance.pre_booking_enabled == pre_booking_enabled)

        if genre_ident is not None:
            query = query.where(Performance.genre_idents.contains([genre_ident]))

        if cursor is not None:
            query = query.where(Performance.snowflake_id < int(cursor))

        performances = await self.session.execute(
            query.order_by(Performance.created_at.desc()).limit(limit)
        )

        return performances.scalars().all()

    async def get_performance_list_by_ids(
        self,
        performance_ids: list[UUID],
    ) -> list[Performance]:
        query = (
            select(Performance)
            .options(joinedload(Performance.poster_image))
            .where(Performance.id.in_(performance_ids))
        )

        return list(
            (
                await self.session.scalars(
                    query.order_by(Performance.created_at.desc())
                )
            ).all()
        )

    async def get_like_list_by_user_id(
        self,
        user_id: UUID,
        performance_ids: list[UUID] | None,
    ) -> list[UserPerformanceLike]:
        query = select(UserPerformanceLike).where(
            UserPerformanceLike.user_id == user_id
        )

        if performance_ids is not None:
            query = query.where(UserPerformanceLike.performance_id.in_(performance_ids))

        likes = await self.session.execute(query)

        return likes.scalars().all()

    async def get_hot_performance_list(self) -> list[HotPerformance]:
        query = select(HotPerformance)

        return list(
            (
                await self.session.scalars(
                    query.order_by(HotPerformance.created_at.desc())
                )
            ).all()
        )

    async def delete_performance(self, performance_id: UUID):
        query = delete(Performance).where(Performance.id == performance_id)
        await self.session.execute(query)
        await self.session.commit()

    async def find_performance_by_id(self, performance_id: UUID) -> Performance | None:
        query = (
            select(Performance)
            .options(joinedload(Performance.like_users))
            .where(Performance.id == performance_id)
        )

        return (await self.session.execute(query)).scalars().first()

    async def create_hot_performance(self, performance_id: UUID):
        self.session.add(instance=HotPerformance(performance_id=performance_id))
        await self.session.commit()

    async def delete_hot_performance(self, performance_id: UUID):
        query = delete(HotPerformance).where(
            HotPerformance.performance_id == performance_id
        )
        await self.session.execute(query)
        await self.session.commit()
