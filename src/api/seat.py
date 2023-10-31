from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import Field

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.models.model import Seat
from src.service.seat import SeatService

router = APIRouter(prefix="/seats", tags=["seat"])


class SeatListRequest(ListRequestBase):
    limit: int = Field(100, ge=1, le=100)
    area_id: UUID


class SeatListResponse(ListResponseBase):
    class Seat(ResponseBase):
        class SeatGrade(ResponseBase):
            id: UUID
            name: str
            price: int

        id: UUID
        x: float
        y: float
        row: int
        col: int
        name: str
        seat_grade: SeatGrade
        is_accessible: bool
        distance_from_stage: float | None = None

    seats: list[Seat]


@router.get("")
async def seat_list_handler(
    q: SeatListRequest = Depends(),
    seat_service: SeatService = Depends(),
) -> SeatListResponse:
    seats = await seat_service.get_seat_list(
        area_id=q.area_id,
        limit=q.limit,
        cursor=q.cursor,
    )
    return SeatListResponse(
        seats=[
            SeatListResponse.Seat.model_validate(seat, from_attributes=True)
            for seat in seats
        ],
        next_cursor=seats[-1].row_col_cursor if len(seats) >= q.limit else None,
    )


class SeatSaveRequest(RequestBase):
    area_id: UUID
    x: float
    y: float
    row: int = Field(ge=1)
    col: int = Field(ge=1)
    name: str = Field(max_length=30)
    seat_grade_id: UUID
    is_accessible: bool = False
    distance_from_stage: float | None = None

    @property
    def model(self) -> Seat:
        return Seat.create(
            area_id=self.area_id,
            x=self.x,
            y=self.y,
            row=self.row,
            col=self.col,
            name=self.name,
            seat_grade_id=self.seat_grade_id,
            is_accessible=self.is_accessible,
            distance_from_stage=self.distance_from_stage,
        )


class SeatSaveResponse(ResponseBase):
    area_id: UUID
    x: float
    y: float
    row: int
    col: int
    name: str
    seat_grade_id: UUID
    is_accessible: bool
    distance_from_stage: float | None = None


@router.post("")
async def seat_save_handler(
    q: SeatSaveRequest = Depends(),
    seat_service: SeatService = Depends(),
) -> SeatSaveResponse:
    seat = await seat_service.save_seat(seat=q.model)

    return SeatSaveResponse.model_validate(seat, from_attributes=True)
