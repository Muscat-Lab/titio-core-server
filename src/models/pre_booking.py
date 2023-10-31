from __future__ import annotations

import typing
import uuid
from typing import List

from snowflake import SnowflakeGenerator
from sqlalchemy import BigInteger, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

from .association_tables import PreBookingSeatAssociation

if typing.TYPE_CHECKING:
    from .model import Performance, Schedule, Seat, User

gen = SnowflakeGenerator(42)


class PreBooking(Base):
    __tablename__ = "pre_bookings"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    schedule_id = mapped_column(ForeignKey("schedules.id"), nullable=False)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)

    snowflake_id = mapped_column(
        BigInteger,
        index=True,
        nullable=False,
        default=lambda: next(gen),
    )

    user: Mapped["User"] = relationship(
        back_populates="pre_bookings",
    )

    schedule: Mapped["Schedule"] = relationship(
        back_populates="pre_bookings",
    )

    performance: Mapped["Performance"] = relationship(
        back_populates="pre_bookings",
    )

    seats: Mapped[List["Seat"]] = relationship(
        secondary=PreBookingSeatAssociation.__tablename__,
        back_populates="pre_bookings",
    )

    @classmethod
    def create(
        cls,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        performance_id: uuid.UUID,
    ) -> PreBooking:
        return cls(
            user_id=user_id,
            schedule_id=schedule_id,
            performance_id=performance_id,
        )

    @property
    def original_price(self) -> int:
        return sum([seat.seat_grade.price for seat in self.seats])
