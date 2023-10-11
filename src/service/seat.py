from fastapi import Depends, HTTPException

from src.models.model import Seat
from src.repositories.area import AreaRepository
from src.repositories.seat import SeatRepository


class SeatService:
    def __init__(
        self,
        area_repository=Depends(AreaRepository),
        seat_repository=Depends(SeatRepository),
    ):
        self.area_repository = area_repository
        self.seat_repository = seat_repository

    async def get_seat_list(
        self, area_id, limit: int, cursor: str | None = None
    ) -> list[Seat]:
        area = await self.area_repository.find_area_by_id(area_id)

        if area is None:
            raise HTTPException(status_code=404, detail="Area not found")

        return await self.seat_repository.get_seat_list(
            area_id, limit=limit, cursor=cursor
        )

    async def save_seat(self, seat) -> Seat:
        area = await self.area_repository.find_area_by_id(seat.area_id)

        if area is None:
            raise HTTPException(status_code=404, detail="Area not found")

        return await self.seat_repository.save_seat(seat)
