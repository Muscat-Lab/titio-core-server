from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.hash_password import verify_password
from src.auth.jwt_handler import create_access_token
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
):
    return RedirectResponse(
        url=await kakao_login_service.redirect_url_with_access_token(code),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/kakao/init", response_model=None)
async def kakao_login_handler(
    redirectUri: str,
    kakao_login_service: KakaoLoginService = Depends(),
):
    return RedirectResponse(
        url=kakao_login_service.get_oauth_authorize_url(redirectUri),
        status_code=status.HTTP_303_SEE_OTHER,
    )
