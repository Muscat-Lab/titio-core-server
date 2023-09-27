from typing import List

from sqlalchemy import Uuid, String, Date, Boolean, DateTime, Float, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from .base import Base

metadata = Base.metadata


class Area(Base):
    __tablename__ = "areas"

    id = mapped_column(Uuid, primary_key=True, index=True)
    performance_id = mapped_column(Uuid, nullable=False)
    title = mapped_column(String(256), nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="areas")


class Performance(Base):
    __tablename__ = "performances"

    id = mapped_column(Uuid, primary_key=True, index=True)
    title = mapped_column(String(50), nullable=False)
    running_time = mapped_column(String(30), nullable=False)
    grade = mapped_column(String(30), nullable=False)
    begin = mapped_column(Date, nullable=False)
    end = mapped_column(Date, nullable=False)
    pre_booking_enabled = mapped_column(Boolean, nullable=False)
    pre_booking_closed_at = mapped_column(DateTime(timezone=True), nullable=True)

    areas: Mapped[List["Area"]] = relationship(back_populates="performance")


class Seat(Base):
    __tablename__ = "seats"

    id = mapped_column(Uuid, primary_key=True, index=True)
    area_id = mapped_column(Uuid, nullable=False)
    seat_grade_id = mapped_column(Uuid, nullable=False)
    x = mapped_column(Float, nullable=False)
    y = mapped_column(Float, nullable=False)
    row = mapped_column(Integer, nullable=False)
    col = mapped_column(Integer, nullable=False)

    area: Mapped["Area"] = relationship(back_populates="seats")


class SeatGrade(Base):
    __tablename__ = "seat_grades"

    id = mapped_column(Uuid, primary_key=True, index=True)
    performance_id = mapped_column(Uuid, nullable=False)
    discount_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(String(30), nullable=False)
    price = mapped_column(Integer, nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="seat_grades")


class Discount(Base):
    __tablename__ = "discounts"

    id = mapped_column(Uuid, primary_key=True, index=True)
    performance_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(String(30), nullable=False)
    discount_rate = mapped_column(Float, nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="discounts")


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
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

    @classmethod
    def create(cls, email: str, password: str, username: str = None) -> "User":
        if username is None:
            username = email.split("@")[0]

        return cls(
            email=email,
            password=password,
            username=username,
        )


__all__ = ["User", "Area", "Performance", "Seat", "SeatGrade", "Discount"]
