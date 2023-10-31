from __future__ import annotations

import typing
import uuid
from decimal import Decimal
from typing import List

from snowflake import SnowflakeGenerator
from sqlalchemy import (
    BigInteger,
    ForeignKey,
    SQLColumnExpression,
    String,
    Uuid,
    func,
    select,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from .model import Performance, Seat


gen = SnowflakeGenerator(42)


class Area(Base):
    __tablename__ = "areas"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    title = mapped_column(String(256), nullable=False)
    accessible_seats_info = mapped_column(String(256), nullable=True)

    performance: Mapped["Performance"] = relationship(
        back_populates="areas",
    )
    seats: Mapped[List["Seat"]] = relationship(
        back_populates="area",
        lazy="selectin",
    )

    snowflake_id = mapped_column(
        BigInteger,
        index=True,
        nullable=False,
        default=lambda: next(gen),
    )

    @hybrid_property
    def accessible_seats_count(self) -> int:
        return len([seat.id for seat in self.seats if seat.is_accessible is True])

    @accessible_seats_count.inplace.setter
    def _accessible_seats_count_setter(self, value: int) -> None:
        assert value is not None

        from src.models.model import Seat

        if len(self.seats) == 0:
            self.seats = [
                Seat(
                    area_id=self.id,
                    is_accessible=True,
                )
                for _ in range(value)
            ]

    @accessible_seats_count.inplace.expression  # type: ignore
    @classmethod
    def _accessible_seats_count_expression(cls) -> SQLColumnExpression[Decimal]:
        from src.models.model import Seat

        return (
            select(func.count(Seat.id))
            .where(Seat.area_id == cls.id)
            .where(Seat.is_accessible.is_(True))
            .label("accessible_seats_count")
        )

    @classmethod
    def create(
        cls,
        performance_id: uuid.UUID,
        title: str,
        accessible_seats_info: str | None,
    ) -> "Area":
        return cls(
            performance_id=performance_id,
            title=title,
            accessible_seats_info=accessible_seats_info,
        )
