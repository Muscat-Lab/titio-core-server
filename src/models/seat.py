from __future__ import annotations

import typing
import uuid
from typing import List

from sqlalchemy import Boolean, Computed, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from .model import Area, PreBooking, SeatGrade


class Seat(Base):
    __tablename__ = "seats"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    area_id = mapped_column(ForeignKey("areas.id"), nullable=False)
    seat_grade_id = mapped_column(ForeignKey("seat_grades.id"), nullable=False)
    x = mapped_column(Float, nullable=False)
    y = mapped_column(Float, nullable=False)
    row = mapped_column(Integer, nullable=False)
    col = mapped_column(Integer, nullable=False)
    name = mapped_column(String(30), nullable=False)

    is_accessible = mapped_column(Boolean, nullable=False, default=True)
    distance_from_stage = mapped_column(Float, nullable=True)

    area: Mapped["Area"] = relationship(
        back_populates="seats",
    )
    seat_grade: Mapped["SeatGrade"] = relationship(back_populates="seats")
    pre_bookings: Mapped[List["PreBooking"]] = relationship(
        secondary="pre_booking_seat_association",
        back_populates="seats",
    )

    row_col_cursor = mapped_column(
        Integer,
        Computed(
            "(row * 10000) + col",
        ),
        index=True,
        nullable=False,
    )

    @property
    def price(self) -> int:
        return self.seat_grade.price

    @classmethod
    def create(
        cls,
        area_id: uuid.UUID,
        x: float,
        y: float,
        row: int,
        col: int,
        name: str,
        seat_grade_id: uuid.UUID,
        is_accessible: bool,
        distance_from_stage: float | None = None,
    ) -> "Seat":
        return cls(
            area_id=area_id,
            x=x,
            y=y,
            row=row,
            col=col,
            name=name,
            seat_grade_id=seat_grade_id,
            is_accessible=is_accessible,
            distance_from_stage=distance_from_stage,
        )


__all__ = [
    "Seat",
]
