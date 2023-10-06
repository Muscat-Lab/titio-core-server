import datetime
import uuid
from typing import List

from sqlalchemy import (
    Boolean,
    Computed,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
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
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="performance")
    contents: Mapped[List["PerformanceContent"]] = relationship(
        back_populates="performance"
    )

    latest_cursor = mapped_column(
        String(256),
        Computed(
            "CONCAT(created_at, ':', id)",
        ),
        index=True,
        nullable=False,
    )

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


class PerformanceContent(Base):
    __tablename__ = "performance_contents"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    sequence = mapped_column(Integer, nullable=False)
    heading = mapped_column(String(256), nullable=False)
    content = mapped_column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "performance_id",
            "sequence",
        ),
    )

    performance: Mapped["Performance"] = relationship(back_populates="contents")


class Location(Base):
    __tablename__ = "locations"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    title = mapped_column(String(150), nullable=False)
    x = mapped_column(Float, nullable=False)
    y = mapped_column(Float, nullable=False)
    address_name = mapped_column(String(150), nullable=False)
    place_name = mapped_column(String(150), nullable=False)
    kakao_place_name = mapped_column(String(150), nullable=False)
    kakao_place_url = mapped_column(String(150), nullable=False)


class Performer(Base):
    __tablename__ = "performers"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = mapped_column(String(20), nullable=False)
    description = mapped_column(Text, nullable=False)

    castings: Mapped[List["Casting"]] = relationship(back_populates="performer")


class Role(Base):
    __tablename__ = "roles"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = mapped_column(String(20), nullable=False)

    castings: Mapped[List["Casting"]] = relationship(back_populates="role")


class Casting(Base):
    __tablename__ = "castings"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performer_id = mapped_column(ForeignKey("performers.id"), nullable=False)
    role_id = mapped_column(ForeignKey("roles.id"), nullable=False)

    performer: Mapped["Performer"] = relationship(back_populates="castings")
    role: Mapped["Role"] = relationship(back_populates="castings")
    schedules: Mapped[List["ScheduleCasting"]] = relationship(back_populates="casting")


class Schedule(Base):
    __tablename__ = "schedules"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    date = mapped_column(Date, nullable=False)
    time = mapped_column(Time, nullable=False)

    castings: Mapped[List["ScheduleCasting"]] = relationship(back_populates="schedule")
    performance: Mapped["Performance"] = relationship(back_populates="schedules")


class ScheduleCasting(Base):
    __tablename__ = "schedule_casts"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    schedule_id = mapped_column(ForeignKey("schedules.id"), nullable=False)
    casting_id = mapped_column(ForeignKey("castings.id"), nullable=False)

    schedule: Mapped["Schedule"] = relationship(back_populates="castings")
    casting: Mapped["Casting"] = relationship(back_populates="schedules")


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

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
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

    avatar_image_id = mapped_column(ForeignKey("images.id"), nullable=True)

    avatar_image: Mapped["Image"] = relationship(
        "Image",
        foreign_keys=[avatar_image_id],
        backref="users",
    )

    @classmethod
    def create(cls, email: str, password: str, username: str | None = None) -> "User":
        if username is None:
            username = email.split("@")[0]

        return cls(
            email=email,
            password=password,
            username=username,
        )


class Image(Base):
    __tablename__ = "images"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    path = mapped_column(String(256), nullable=False)
    extension = mapped_column(String(8), nullable=False)


__all__ = ["User", "Area", "Performance", "Seat", "SeatGrade", "Discount", "Image"]
