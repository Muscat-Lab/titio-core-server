from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.auth.jwt_handler import get_current_user
from src.service.user import UserService

router = APIRouter(prefix="/users", tags=["user"])


class UserResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: UUID
    email: str
    username: str


@router.get("")
async def user_list_handler(
    user_service: UserService = Depends(),
) -> list[UserResponse]:
    return [
        UserResponse.model_validate(user, from_attributes=True)
        for user in await user_service.get_user_list()
    ]


class UserMeResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: UUID
    email: str
    username: str


@router.get("/me")
async def user_me_handler(
    user_service: UserService = Depends(), auth: UUID = Depends(get_current_user)
) -> UserMeResponse:
    return UserMeResponse.model_validate(
        await user_service.find_user_by_id(user_id=auth),
        from_attributes=True,
    )
