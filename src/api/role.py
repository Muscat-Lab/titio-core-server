from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.models.model import Role
from src.service.role import RoleService

router = APIRouter(prefix="/roles", tags=["role"])


class RoleListRequest(ListRequestBase):
    performance_id: UUID


class RoleListResponse(ListResponseBase):
    class Role(ResponseBase):
        id: UUID
        name: str

    roles: list[Role]


@router.get("")
async def role_list_handler(
    q: RoleListRequest = Depends(),
    role_service: RoleService = Depends(),
) -> RoleListResponse:
    roles = await role_service.get_role_list(
        performance_id=q.performance_id,
        limit=q.limit,
        cursor=q.cursor,
    )
    return RoleListResponse(
        roles=[
            RoleListResponse.Role.model_validate(role, from_attributes=True)
            for role in roles
        ],
        next_cursor=(roles[-1].created_at if len(roles) >= q.limit else None),
    )


class RoleCreateRequest(RequestBase):
    performance_id: UUID
    name: str

    @property
    def model(self) -> Role:
        return Role.create(
            performance_id=self.performance_id,
            name=self.name,
        )


class RoleCreateResponse(ResponseBase):
    id: UUID
    name: str


@router.post("")
async def role_create_handler(
    q: RoleCreateRequest,
    role_service: RoleService = Depends(),
) -> RoleCreateResponse:
    role = await role_service.save_role(
        q.model,
    )

    return RoleCreateResponse.model_validate(role, from_attributes=True)
