import enum


class PreBookingStatus(str, enum.Enum):
    InProgress = "InProgress"
    Confirmed = "Confirmed"
    Rejected = "Rejected"
