from uuid import UUID

from fastapi import Depends, HTTPException

from src.models.model import PreBooking
from src.repositories.performance import PerformanceRepository
from src.repositories.pre_booking import PreBookingRepository
from src.repositories.schedule import ScheduleRepository
from src.repositories.seat import SeatRepository
from src.repositories.user import UserRepository


class PreBookingService:
    def __init__(
        self,
        pre_booking_repository: PreBookingRepository = Depends(PreBookingRepository),
        performance_repository: PerformanceRepository = Depends(PerformanceRepository),
        schedule_repository: ScheduleRepository = Depends(ScheduleRepository),
        seat_repository: SeatRepository = Depends(SeatRepository),
        user_repository: UserRepository = Depends(UserRepository),
    ):
        self._pre_booking_repository = pre_booking_repository
        self._performance_repository = performance_repository
        self._schedule_repository = schedule_repository
        self._seat_repository = seat_repository
        self._user_repository = user_repository

    async def create(
        self,
        user_id: UUID,
        performance_id: UUID,
        schedule_id: UUID,
        seat_ids: list[UUID],
    ) -> PreBooking:
        performance = await self._performance_repository.find_performance_by_id(
            performance_id
        )

        if performance is None:
            raise HTTPException(status_code=404, detail="Performance not found")

        schedule = await self._schedule_repository.find_schedule_by_id(schedule_id)

        if schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")

        original_seat_list = await self._seat_repository.get_seat_list_by_seat_ids(
            seat_ids
        )

        if original_seat_list is None or len(seat_ids) != len(original_seat_list):
            raise HTTPException(status_code=404, detail="Seat not found")

        user = await self._user_repository.find_user_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        pre_booking = PreBooking.create(
            user_id=user.id,
            performance_id=performance.id,
            schedule_id=schedule.id,
        )

        pre_booking.seats = original_seat_list

        return await self._pre_booking_repository.save_pre_booking(pre_booking)

    async def find_pre_booking_by_id(
        self,
        user_id: UUID,
        pre_booking_id: UUID,
    ) -> PreBooking | None:
        pre_booking = await self._pre_booking_repository.find_pre_booking_by_id(
            pre_booking_id
        )

        if pre_booking is None:
            raise HTTPException(status_code=404, detail="PreBooking not found")

        if pre_booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        return pre_booking

    async def get_pre_booking_list(
        self,
        user_id: UUID,
        limit: int,
        cursor: str | None = None,
    ):
        return await self._pre_booking_repository.get_pre_booking_list(
            user_id,
            limit,
            cursor,
        )
