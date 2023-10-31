from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

from src.models.base import Base


class PreBookingSeatAssociation(Base):
    __tablename__ = "pre_booking_seat_association"

    pre_booking_id = mapped_column(ForeignKey("pre_bookings.id"), primary_key=True)
    seat_id = mapped_column(ForeignKey("seats.id"), primary_key=True)
