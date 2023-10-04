import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, RequestBase, ListResponseBase
from src.auth.jwt_handler import get_current_user
from src.enums.booking import BookingStatus

router = APIRouter(prefix="/bookings", tags=["booking"])


class BookingListRequest(ListRequestBase):
    pass


class BookingListResponse(ListResponseBase):
    class Booking(RequestBase):
        class Seat(RequestBase):
            id: UUID
            name: str
            booking_code: str

        class Performance(RequestBase):
            id: UUID
            title: str
            thumbnail_url: str

        id: UUID
        performance: Performance
        status: BookingStatus
        seats: list[Seat]
        scheduled_at: datetime.datetime

    bookings: list[Booking]


@router.get("")
async def booking_list_handler(
    q: BookingListRequest = Depends(),
    auth: UUID = Depends(get_current_user),
) -> BookingListResponse:
    return BookingListResponse(
        bookings=[
            BookingListResponse.Booking(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                performance=BookingListResponse.Booking.Performance(
                    id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b2a"),
                    title="하트시그널",
                    thumbnail_url="https://www.edureka.co/blog/golang-tutorial/#var",
                ),
                status=BookingStatus.PaymentCompleted,
                seats=[
                    BookingListResponse.Booking.Seat(
                        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1a"),
                        name="A구역 G11",
                        booking_code="AG1220230024",
                    ),
                    BookingListResponse.Booking.Seat(
                        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1b"),
                        name="A구역 G12",
                        booking_code="AG1120230024",
                    ),
                ],
                scheduled_at=datetime.datetime.fromisoformat("2023-07-26T18:00:00"),
            ),
            BookingListResponse.Booking(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1a"),
                performance=BookingListResponse.Booking.Performance(
                    id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b2a"),
                    title="레베카",
                    thumbnail_url="https://www.edureka.co/blog/golang-tutorial/#var",
                ),
                status=BookingStatus.PaymentCompleted,
                seats=[
                    BookingListResponse.Booking.Seat(
                        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0c2a0b1a"),
                        name="A구역 A7",
                        booking_code="AA1220233932",
                    )
                ],
                scheduled_at=datetime.datetime.fromisoformat("2023-07-26T18:00:00"),
            ),
        ],
        next_cursor=None,
    )


class BookingGetResponse(RequestBase):
    class Seat(RequestBase):
        id: UUID
        row: int
        col: int
        name: str
        price: int
        booking_code: str

    class Schedule(RequestBase):
        id: UUID
        date: datetime.date
        time: datetime.time

    class Performance(RequestBase):
        id: UUID
        title: str

    id: UUID
    performance: Performance
    user_id: UUID
    status: BookingStatus
    seats: list[Seat]
    schedule: Schedule
    original_price: int
    payment_price: int
    discount_price: int
    refund_price: int
    paid_at: datetime.datetime | None = None


@router.get("/{bookingId}")
async def booking_get_handler(
    bookingId: UUID,
    auth: UUID = Depends(get_current_user),
) -> BookingGetResponse:
    return BookingGetResponse(
        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0c2a0b1a"),
        performance=BookingGetResponse.Performance(
            id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0c2a0b1a"),
            title="하트시그널",
        ),
        user_id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0c2a0b1a"),
        status=BookingStatus.PaymentCompleted,
        seats=[
            BookingGetResponse.Seat(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0c2a0b1a"),
                row=1,
                col=1,
                name="A구역 A1",
                price=1000,
                booking_code="AA1220233932",
            ),
            BookingGetResponse.Seat(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0c2a0b1b"),
                row=1,
                col=2,
                name="A구역 A2",
                price=1000,
                booking_code="AA1220233932",
            ),
        ],
        schedule=BookingGetResponse.Schedule(
            id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0c2a0b1a"),
            date=datetime.date(year=2021, month=1, day=1),
            time=datetime.time(hour=12, minute=0),
        ),
        original_price=2000,
        payment_price=2000,
        discount_price=0,
        refund_price=0,
        paid_at=datetime.datetime.fromisoformat("2023-07-26T18:00:00"),
    )
