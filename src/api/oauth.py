from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from src.service.kakao_login import KakaoLoginService

router = APIRouter(prefix="/oauth", tags=["oauth"])


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
    redirect_uri: str,
    kakao_login_service: KakaoLoginService = Depends(),
):
    return RedirectResponse(
        url=kakao_login_service.get_oauth_authorize_url(redirect_uri),
        status_code=status.HTTP_303_SEE_OTHER,
    )
