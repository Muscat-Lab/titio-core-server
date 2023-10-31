import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.auth.jwt_handler import get_current_user
from src.enums.pre_booking import PreBookingStatus
from src.models.model import PreBooking
from src.service.pre_booking import PreBookingService

router = APIRouter(prefix="/preBookings", tags=["preBooking"])


class PreBookingListRequest(ListRequestBase):
    performance_id: UUID


class PreBookingListResponse(ListResponseBase):
    class PreBooking(ResponseBase):
        class Performance(ResponseBase):
            id: UUID
            title: str
            poster_image_url: str | None

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
        status: PreBookingStatus = PreBookingStatus.InProgress
        schedule: Schedule
        seats: list[Seat]
        original_price: int

    pre_bookings: list[PreBooking]


@router.get("")
async def pre_booking_list_handler(
    q: PreBookingListRequest = Depends(),
    auth: UUID = Depends(get_current_user),
    pre_booking_service: PreBookingService = Depends(),
) -> PreBookingListResponse:
    pre_bookings = await pre_booking_service.get_pre_booking_list(
        user_id=auth,
        limit=q.limit,
        cursor=q.cursor,
    )

    return PreBookingListResponse(
        pre_bookings=[
            PreBookingListResponse.PreBooking.model_validate(
                pre_booking, from_attributes=True
            )
            for pre_booking in pre_bookings
        ],
        next_cursor=(
            str(pre_bookings[-1].snowflake_id) if len(pre_bookings) >= q.limit else None
        ),
    )


class PreBookingGetResponse(PreBookingListResponse.PreBooking):
    pass


@router.get("/{preBookingId}")
async def pre_booking_get_handler(
    preBookingId: UUID,
    user_id: UUID = Depends(get_current_user),
    pre_booking_service: PreBookingService = Depends(),
) -> PreBookingGetResponse:
    pre_booking = await pre_booking_service.find_pre_booking_by_id(
        user_id=user_id,
        pre_booking_id=preBookingId,
    )

    return PreBookingGetResponse.model_validate(pre_booking, from_attributes=True)


class PreBookingCreateRequest(RequestBase):
    performance_id: UUID
    schedule_id: UUID
    seat_ids: list[UUID]

    @classmethod
    def model(cls, user_id: UUID) -> PreBooking:
        return PreBooking.create(
            performance_id=cls.performance_id,
            schedule_id=cls.schedule_id,
            user_id=user_id,
        )


class PreBookingCreateResponse(ResponseBase):
    id: UUID


@router.post("")
async def pre_booking_create_handler(
    q: PreBookingCreateRequest,
    user_id: UUID = Depends(get_current_user),
    pre_booking_service: PreBookingService = Depends(),
) -> PreBookingCreateResponse:
    return PreBookingCreateResponse(
        id=(
            await pre_booking_service.create(
                user_id=user_id,
                performance_id=q.performance_id,
                schedule_id=q.schedule_id,
                seat_ids=q.seat_ids,
            )
        ).id
    )
