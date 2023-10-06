import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, ResponseBase
from src.auth.jwt_handler import get_current_user
from src.enums.pre_booking import PreBookingStatus

router = APIRouter(prefix="/preBookings", tags=["preBooking"])


class PreBookingListRequest(ListRequestBase):
    performance_id: UUID


class PreBookingListResponse(ListResponseBase):
    class PreBooking(ResponseBase):
        class Performance(ResponseBase):
            id: UUID
            title: str
            thumbnail_url: str

        class Schedule(ResponseBase):
            id: UUID
            date: datetime.date
            time: datetime.time

        class Seat(ResponseBase):
            id: UUID
            name: str
            row: int
            col: int
            price: int

        id: UUID
        performance: Performance
        status: PreBookingStatus
        schedule: Schedule
        seats: list[Seat]
        original_price: int

    pre_bookings: list[PreBooking]


@router.get("")
async def pre_booking_list_handler(
    q: PreBookingListRequest = Depends(),
    auth: UUID = Depends(get_current_user),
) -> PreBookingListResponse:
    return PreBookingListResponse(
        pre_bookings=[
            PreBookingListResponse.PreBooking(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1a"),
                performance=PreBookingListResponse.PreBooking.Performance(
                    id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1a"),
                    title="하트시그널",
                    thumbnail_url="https://www.edureka.co/blog/golang-tutorial/#var",
                ),
                status=PreBookingStatus.InProgress,
                schedule=PreBookingListResponse.PreBooking.Schedule(
                    id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1a"),
                    date=datetime.date(2021, 1, 1),
                    time=datetime.time(12, 0),
                ),
                seats=[
                    PreBookingListResponse.PreBooking.Seat(
                        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1a"),
                        name="A구역 G11",
                        row=7,
                        col=11,
                        price=1000,
                    ),
                    PreBookingListResponse.PreBooking.Seat(
                        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1b"),
                        name="A구역 G12",
                        row=7,
                        col=12,
                        price=1000,
                    ),
                ],
                original_price=2000,
            ),
            PreBookingListResponse.PreBooking(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1b"),
                performance=PreBookingListResponse.PreBooking.Performance(
                    id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1b"),
                    title="레베카",
                    thumbnail_url="https://www.edureka.co/blog/golang-tutorial/#var",
                ),
                status=PreBookingStatus.InProgress,
                schedule=PreBookingListResponse.PreBooking.Schedule(
                    id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1b"),
                    date=datetime.date(2021, 1, 1),
                    time=datetime.time(12, 0),
                ),
                seats=[
                    PreBookingListResponse.PreBooking.Seat(
                        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1b"),
                        name="A구역 A2",
                        row=1,
                        col=2,
                        price=1000,
                    ),
                    PreBookingListResponse.PreBooking.Seat(
                        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b2a0b1b"),
                        name="A구역 A1",
                        row=1,
                        col=1,
                        price=1000,
                    ),
                ],
                original_price=2000,
            ),
        ],
        next_cursor=None,
    )


class PreBookingGetResponse(PreBookingListResponse.PreBooking):
    pass


@router.get("/{preBookingId}")
async def pre_booking_get_handler(
    preBookingId: UUID, auth: UUID = Depends(get_current_user)
) -> PreBookingGetResponse:
    return PreBookingGetResponse(
        id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a1b2a0b1a"),
        performance=PreBookingGetResponse.Performance(
            id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a1b2a0b1a"),
            title="하트시그널",
            thumbnail_url="https://www.edureka.co/blog/golang-tutorial/#var",
        ),
        status=PreBookingStatus.InProgress,
        schedule=PreBookingGetResponse.Schedule(
            id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a1b2a0b1a"),
            date=datetime.date(2021, 1, 1),
            time=datetime.time(12, 0),
        ),
        seats=[
            PreBookingGetResponse.Seat(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a1b2a0b1a"),
                name="A구역 G11",
                row=7,
                col=11,
                price=1000,
            ),
            PreBookingGetResponse.Seat(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a1b2a0b1b"),
                name="A구역 G12",
                row=7,
                col=12,
                price=1000,
            ),
        ],
        original_price=2000,
    )
