import datetime
import uuid
from typing import List

from sqlalchemy import Uuid, String, Date, Boolean, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from .base import Base

Base.metadata.naming_convention = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = Base.metadata


class Area(Base):
    __tablename__ = "areas"

    id = mapped_column(Uuid, primary_key=True, index=True)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    title = mapped_column(String(256), nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="areas")
    seats: Mapped[List["Seat"]] = relationship(back_populates="area")


class Performance(Base):
    __tablename__ = "performances"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4())
    title = mapped_column(String(50), nullable=False)
    running_time = mapped_column(String(30), nullable=False)
    grade = mapped_column(String(30), nullable=False)
    begin = mapped_column(Date, nullable=False)
    end = mapped_column(Date, nullable=False)
    pre_booking_enabled = mapped_column(Boolean, nullable=False)
    pre_booking_closed_at = mapped_column(DateTime(timezone=True), nullable=True)

    areas: Mapped[List["Area"]] = relationship(back_populates="performance")
    seat_grades: Mapped[List["SeatGrade"]] = relationship(back_populates="performance")
    discounts: Mapped[List["Discount"]] = relationship(back_populates="performance")

    @classmethod
    def create(
        cls,
        title: str,
        running_time: str,
        grade: str,
        begin: datetime.date,
        end: datetime.date,
        pre_booking_enabled: bool,
        pre_booking_closed_at: datetime.datetime | None,
    ) -> "Performance":
        return cls(

            title=title,
            running_time=running_time,
            grade=grade,
            begin=begin,
            end=end,
            pre_booking_enabled=pre_booking_enabled,
            pre_booking_closed_at=pre_booking_closed_at,
        )


class Seat(Base):
    __tablename__ = "seats"

    id = mapped_column(Uuid, primary_key=True, index=True)
    area_id = mapped_column(ForeignKey("areas.id"), nullable=False)
    seat_grade_id = mapped_column(ForeignKey("seat_grades.id"), nullable=False)
    x = mapped_column(Float, nullable=False)
    y = mapped_column(Float, nullable=False)
    row = mapped_column(Integer, nullable=False)
    col = mapped_column(Integer, nullable=False)

    area: Mapped["Area"] = relationship(back_populates="seats")


class SeatGrade(Base):
    __tablename__ = "seat_grades"

    id = mapped_column(Uuid, primary_key=True, index=True)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    discount_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(String(30), nullable=False)
    price = mapped_column(Integer, nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="seat_grades")


class Discount(Base):
    __tablename__ = "discounts"

    id = mapped_column(Uuid, primary_key=True, index=True)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    name = mapped_column(String(30), nullable=False)
    discount_rate = mapped_column(Float, nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="discounts")


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4())
    email = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
    )
    username = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
    )
    password = mapped_column(String(256), nullable=False)
    kakao_id = mapped_column(String(256), nullable=True, unique=True, index=True)

    @classmethod
    def create(cls, email: str, password: str, username: str | None = None) -> "User":
        if username is None:
            username = email.split("@")[0]

        return cls(
            email=email,
            password=password,
            username=username,
        )


__all__ = ["User", "Area", "Performance", "Seat", "SeatGrade", "Discount"]
