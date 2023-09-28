import logging

import jwt

from urllib.parse import urlencode, urlunparse, urlparse
from fastapi import Depends
from pydantic.v1 import BaseModel

from src.auth.jwt_handler import create_access_token
from src.config import get_config, ConfigTemplate
from src.exceptions.exception import ServiceException, ErrCode
from src.models.model import User
from src.repositories.user import UserRepository
from src.service.http import KakaoOauthTokenRequest, HttpService
from src.utils.auth import jwk_to_pem, JWK

import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KakaoOauthAuthorizeRequest(BaseModel):
    client_id: str
    redirect_uri: str
    response_type: str = "code"
    nonce: str


class KakaoOauthOidcUserInfoResponse(BaseModel):
    sub: str
    name: str | None
    nickname: str | None
    picture: str | None
    email: str | None
    email_verified: bool | None
    gender: str | None
    birthdate: str | None
    phone_number: str | None
    phone_number_verified: bool | None


class KakaoIdTokenClaims(BaseModel):
    iss: str
    aud: str
    sub: str  # 카카오 회원번호
    iat: int
    exp: int
    auth_time: int
    nonce: str | None
    nickname: str | None
    picture: str | None
    email: str | None

    @property
    def user_id(self) -> str:
        return self.sub

    @property
    def redirect_uri(self) -> str | None:
        return self.nonce


class KakaoLoginService:
    def __init__(
        self,
        http_service: HttpService = Depends(HttpService),
        config: ConfigTemplate = Depends(get_config),
        user_repository: UserRepository = Depends(UserRepository),
    ):
        self.kakao_api_host = "kauth.kakao.com"
        self.http_service = http_service
        self.config = config
        self.user_repository = user_repository

    def get_oauth_authorize_url(self, redirect_uri: str) -> str:
        return urlunparse(
            (
                "https",
                self.kakao_api_host,
                "/oauth/authorize",
                "",
                urlencode(
                    KakaoOauthAuthorizeRequest(
                        client_id=self.config.KAKAO_CLIENT_ID,
                        redirect_uri=f"{self.config.SERVER_HOST}/oauth/kakao/callback",
                        nonce=redirect_uri,
                    ).dict()
                ),
                "",
            )
        )

    async def redirect_url_with_access_token(
        self,
        code: str,
    ) -> str:
        try:  # 1. 인가코드를 사용해서 토큰 발급
            response = await self.http_service.get_kakao_oauth_token(
                data=KakaoOauthTokenRequest(
                    client_id=self.config.KAKAO_CLIENT_ID,
                    redirect_uri=f"{self.config.SERVER_HOST}/oauth/kakao/callback",
                    code=code,
                ),
            )
        except Exception as e:
            logger.error(e, exc_info=True)

            raise ServiceException(
                error_code=ErrCode.KakaoUnknownError,
                status_code=500,
            )

        if not response.id_token:  # 2. id_token이 없으면 에러
            raise ServiceException(
                error_code=ErrCode.KakaoTokenVerifyFailed,
                status_code=400,
            )

        claims = await self._verify_kakao_token(response.id_token)  # 3. 토큰 검증

        if not claims.redirect_uri:  # 4. 리다이렉트 URI가 없으면 에러
            raise ServiceException(
                error_code=ErrCode.KakaoTokenVerifyFailed,
                status_code=400,
            )

        user = self.user_repository.get_user_by_kakao_id(claims.user_id)

        if not user:
            user = self.user_repository.save_user(
                user=User(
                    kakao_id=claims.user_id,
                    email=claims.email,
                    username=claims.nickname,
                    password="<kakao-login>",
                )
            )

        redirect_url = urlparse(claims.redirect_uri)

        return urlunparse(
            (
                redirect_url.scheme,
                redirect_url.netloc,
                redirect_url.path,
                "",
                urlencode({"access_token": create_access_token(str(user.id))}),
                "",
            )
        )

    async def _verify_kakao_token(self, id_token: str) -> KakaoIdTokenClaims:
        keys = await self.http_service.get_kakao_jwks()

        try:
            header = jwt.get_unverified_header(id_token)

            matching_keys = [key for key in keys if key.kid == header["kid"]]

            if not matching_keys:
                raise ServiceException(
                    error_code=ErrCode.KakaoUnknownError,
                    status_code=500,
                )

            pem_key = jwk_to_pem(jwk=JWK.parse_obj(matching_keys[0]))

            claims = jwt.decode(
                id_token,
                pem_key,
                algorithms=["RS256"],
                audience=self.config.KAKAO_CLIENT_ID,
                issuer=f"https://{self.kakao_api_host}",
            )

        except jwt.ExpiredSignatureError:
            raise ServiceException(
                error_code=ErrCode.KakaoTokenExpired,
                status_code=401,
            )
        except jwt.PyJWTError as e:
            logger.error(e, exc_info=True)

            raise ServiceException(
                error_code=ErrCode.KakaoTokenVerifyError,
                status_code=401,
            )
        except Exception as e:
            logger.error(e, exc_info=True)

            raise ServiceException(
                error_code=ErrCode.KakaoUnknownError,
                status_code=500,
            )

        return KakaoIdTokenClaims.parse_obj(claims)
