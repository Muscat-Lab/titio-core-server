from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database.connection import get_db
from src.models.model import Seat


class SeatRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def find_seat_by_id(self, seat_id: UUID) -> Seat | None:
        query = select(Seat).where(Seat.id == seat_id)

        return (await self.session.execute(query)).unique().scalar_one_or_none()

    async def get_seat_list_by_seat_ids(self, seat_ids: list[UUID]) -> list[Seat]:
        query = select(Seat).where(Seat.id.in_(seat_ids))

        return list((await self.session.execute(query)).scalars().all())

    async def get_seat_list(
        self,
        area_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> list[Seat]:
        query = (
            select(Seat)
            .options(joinedload(Seat.seat_grade))
            .where(Seat.area_id == area_id)
        )

        if cursor is not None:
            query = query.where(Seat.row_col_cursor > int(cursor))

        query = query.order_by(Seat.row_col_cursor.asc()).limit(limit)

        seats = await self.session.execute(query)

        return list(seats.scalars().all())

    async def save_seat(self, seat: Seat) -> Seat:
        self.session.add(instance=seat)
        await self.session.commit()
        await self.session.refresh(instance=seat)

        return seat
