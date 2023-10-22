from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.models.model import SeatGrade
from src.service.seat_grade import SeatGradeService

router = APIRouter(prefix="/seatGrades", tags=["seatGrade"])


class SeatGradeListRequest(ListRequestBase):
    performance_id: UUID


class SeatGradeListResponse(ListResponseBase):
    class SeatGrade(ResponseBase):
        id: UUID
        name: str
        price: int

    seat_grades: list[SeatGrade]


@router.get("")
async def seat_grade_list_handler(
    q: SeatGradeListRequest = Depends(),
    seat_grade_service: SeatGradeService = Depends(),
) -> SeatGradeListResponse:
    seat_grades = await seat_grade_service.get_seat_grade_list(
        performance_id=q.performance_id,
        limit=q.limit,
        cursor=q.cursor,
    )
    return SeatGradeListResponse(
        seat_grades=[
            SeatGradeListResponse.SeatGrade.model_validate(
                seat_grade, from_attributes=True
            )
            for seat_grade in seat_grades
        ],
        next_cursor=(
            str(seat_grades[-1].snowflake_id) if len(seat_grades) >= q.limit else None
        ),
    )


class SeatGradeSaveRequest(RequestBase):
    performance_id: UUID
    name: str
    price: int

    @property
    def model(self) -> SeatGrade:
        return SeatGrade.create(
            performance_id=self.performance_id,
            name=self.name,
            price=self.price,
        )


class SeatGradeSaveResponse(ResponseBase):
    id: UUID
    performance_id: UUID
    name: str
    price: int


@router.post("")
async def seat_grade_save_handler(
    q: SeatGradeSaveRequest = Depends(),
    seat_grade_service: SeatGradeService = Depends(),
) -> SeatGradeSaveResponse:
    seat_grade = await seat_grade_service.save_seat_grade(seat_grade=q.model)
    return SeatGradeSaveResponse.model_validate(seat_grade, from_attributes=True)
