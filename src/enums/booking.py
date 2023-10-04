import enum


class BookingStatus(str, enum.Enum):
    BookRequested = "BookRequested"
    PaymentRequested = "PaymentRequested"
    PaymentCompleted = "PaymentCompleted"
    CancelRequested = "CancelRequested"
    CancelCompleted = "CancelCompleted"
