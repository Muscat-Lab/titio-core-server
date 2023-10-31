from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database.connection import get_db
from src.models.model import PreBooking
from src.models.seat import Seat


class PreBookingRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def save_pre_booking(self, pre_booking: PreBooking) -> PreBooking:
        self.session.add(instance=pre_booking)
        await self.session.commit()
        await self.session.refresh(instance=pre_booking)

        return pre_booking

    async def find_pre_booking_by_id(
        self,
        pre_booking_id: UUID,
    ) -> PreBooking | None:
        query = (
            select(PreBooking)
            .options(
                joinedload(PreBooking.seats),
                joinedload(PreBooking.user),
                joinedload(PreBooking.performance),
                joinedload(PreBooking.schedule),
            )
            .where(PreBooking.id == pre_booking_id)
        )

        return (await self.session.execute(query)).unique().scalar_one_or_none()

    async def get_pre_booking_list(
        self,
        user_id: UUID,
        limit: int,
        cursor: str | None = None,
    ):
        query = (
            select(PreBooking)
            .options(
                joinedload(PreBooking.seats).joinedload(Seat.seat_grade),
                joinedload(PreBooking.user),
                joinedload(PreBooking.performance),
                joinedload(PreBooking.schedule),
            )
            .where(PreBooking.user_id == user_id)
        )

        if cursor is not None:
            query = query.where(PreBooking.snowflake_id < int(cursor))

        query = query.order_by(PreBooking.snowflake_id.desc()).limit(limit)

        return list((await self.session.execute(query)).scalars().unique().all())
