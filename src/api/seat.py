from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, ResponseBase

router = APIRouter(prefix="/seats", tags=["seat"])


class SeatListRequest(ListRequestBase):
    area_id: UUID


class SeatListResponse(ListResponseBase):
    class Seat(ResponseBase):
        class Grade(ResponseBase):
            id: UUID
            name: str
            price: int

        id: UUID
        x: float
        y: float
        row: int
        col: int
        name: str
        grade: Grade

    seats: list[Seat]


@router.get("")
async def seat_list_handler(
    q: SeatListRequest = Depends(),
) -> SeatListResponse:
    return SeatListResponse(
        seats=[
            SeatListResponse.Seat(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                x=10.0,
                y=10.0,
                row=1,
                col=1,
                name="seat1",
                grade=SeatListResponse.Seat.Grade(
                    id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                    name="grade1",
                    price=1000,
                ),
            ),
            SeatListResponse.Seat(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1b"),
                x=10.0,
                y=20.0,
                row=2,
                col=2,
                name="seat2",
                grade=SeatListResponse.Seat.Grade(
                    id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1b"),
                    name="grade2",
                    price=2000,
                ),
            ),
        ],
        next_cursor=None,
    )
