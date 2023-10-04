import logging

from fastapi import Depends
from pydantic import BaseModel

from src.config import ConfigTemplate, get_config
from src.exceptions.exception import ServiceException, ErrCode
from src.utils.auth import JWK
from src.utils.http_client import HttpClient, get_http_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KakaoOauthTokenRequest(BaseModel):
    grant_type: str = "authorization_code"
    client_id: str
    redirect_uri: str
    code: str


class KakaoOauthTokenResponse(BaseModel):
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    scope: str | None
    id_token: str | None


class HttpService:
    def __init__(
        self,
        http_client: HttpClient = Depends(get_http_client),
        config: ConfigTemplate = Depends(get_config),
    ):
        self.http_client = http_client
        self.config = config

    async def get_kakao_oauth_token(
        self,
        data: KakaoOauthTokenRequest,
    ) -> KakaoOauthTokenResponse:
        try:
            result = KakaoOauthTokenResponse.model_validate(
                await self.http_client.post(
                    f"https://{self.config.KAKAO_API_HOST}/oauth/token",
                    data=data.model_dump(),
                )
            )

            return result
        except Exception as e:
            logger.error(e, exc_info=True)

            raise ServiceException(
                error_code=ErrCode.HttpClientError,
                status_code=500,
            )

    async def get_kakao_jwks(self) -> list[JWK]:
        try:
            return [
                JWK.model_validate(jwk)
                for jwk in (
                    await self.http_client.get(
                        f"https://{self.config.KAKAO_API_HOST}/.well-known/jwks.json"
                    )
                ).get("keys", [])
            ]
        except Exception as e:
            logger.error(e, exc_info=True)

            raise ServiceException(
                error_code=ErrCode.HttpClientError,
                status_code=500,
            )
