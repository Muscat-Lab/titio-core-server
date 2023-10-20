import datetime
from uuid import UUID

from src.api.request import ResponseBase


class BasePerformanceResponse(ResponseBase):
    id: UUID
    title: str
    running_time: str
    grade: str
    begin: datetime.date
    end: datetime.date
    pre_booking_enabled: bool
    pre_booking_closed_at: datetime.datetime | None = None
    poster_image_url: str | None = None
    like: bool = False
    schedule_text: str = ""
    location_text: str = ""
