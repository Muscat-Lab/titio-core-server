from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.api.request import RequestBase, ResponseBase
from src.auth.hash_password import get_password_hash, verify_password
from src.auth.jwt_handler import create_access_token
from src.models.model import User
from src.service.kakao_login import KakaoLoginService
from src.service.user import UserService

router = APIRouter(prefix="/oauth", tags=["oauth"])


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(),
):
    user = await user_service.find_user_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(str(user.id)),
        "token_type": "bearer",
    }


@router.get("/kakao/callback")
async def kakao_login_callback_handler(
    code: str,
    kakao_login_service: KakaoLoginService = Depends(),
) -> RedirectResponse:
    return await kakao_login_service.redirect_with_access_token(code)


@router.get("/kakao/init", response_model=None)
async def kakao_login_handler(
    redirectUri: str,
    kakao_login_service: KakaoLoginService = Depends(),
) -> RedirectResponse:
    return RedirectResponse(
        url=kakao_login_service.get_oauth_authorize_url(redirectUri),
        status_code=status.HTTP_303_SEE_OTHER,
    )


class SigninForDebugRequest(RequestBase):
    username: str
    email: str
    password: str


class SigninForDebugResponse(ResponseBase):
    id: UUID


@router.post("/signin_for_debug")
async def user_signin_for_debug_handler(
    q: SigninForDebugRequest,
    user_service: UserService = Depends(),
) -> SigninForDebugResponse:
    try:
        await user_service.find_user_by_username(q.username)
        await user_service.find_user_by_email(q.email)
    except HTTPException:
        pass
    else:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await user_service.save_user(
        User.create(
            username=q.username,
            email=q.email,
            password=get_password_hash(q.password),
        )
    )

    return SigninForDebugResponse(
        id=user.id,
    )
