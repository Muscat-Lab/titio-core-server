from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.models.model import Casting
from src.service.casting import CastingService

router = APIRouter(prefix="/castings", tags=["casting"])


class CastingListRequest(ListRequestBase):
    performance_id: UUID


class CastingListResponse(ListResponseBase):
    class Casting(ResponseBase):
        id: UUID
        performer_name: str
        performer_id: UUID
        role_name: str
        role_id: UUID
        profile_url: str

    castings: list[Casting]


@router.get("")
async def casting_list_handler(
    q: CastingListRequest = Depends(),
    casting_service: CastingService = Depends(),
) -> CastingListResponse:
    castings = await casting_service.get_casting_list(
        performance_id=q.performance_id,
        limit=q.limit,
        cursor=q.cursor,
    )

    return CastingListResponse(
        castings=[
            CastingListResponse.Casting(
                id=casting.id,
                performer_name=casting.performer.name,
                performer_id=casting.performer.id,
                role_name=casting.role.name,
                role_id=casting.role.id,
                profile_url="https://www.edureka.co/blog/golang-tutorial/#var",
            )
            for casting in castings
        ],
        next_cursor=(castings[-1].created_at if len(castings) >= q.limit else None),
    )


class CastingCreateRequest(RequestBase):
    performance_id: UUID
    performer_id: UUID
    role_id: UUID

    @property
    def model(self) -> Casting:
        return Casting.create(
            performance_id=self.performance_id,
            performer_id=self.performer_id,
            role_id=self.role_id,
        )


class CastingCreateResponse(ResponseBase):
    id: UUID


@router.post("")
async def casting_create_handler(
    q: CastingCreateRequest,
    casting_service: CastingService = Depends(),
) -> CastingCreateResponse:
    casting = await casting_service.save_casting(
        q.model,
    )

    return CastingCreateResponse.model_validate(casting, from_attributes=True)
