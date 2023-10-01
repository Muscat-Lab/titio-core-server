import uuid
from unittest.mock import Mock
from urllib.parse import urlencode, urlparse

import pytest

from src.config import ConfigTemplate
from src.repositories.user import UserRepository
from src.service.http import KakaoOauthTokenResponse, HttpService
from src.utils.auth import JWK
from src.utils.http_client import AioHttpClient
from src.service.kakao_login import KakaoLoginService

config = ConfigTemplate()


class TestKakaoLoginService:
    @pytest.fixture()
    def mocked_user_repository(self):
        return Mock(spec=UserRepository)

    @pytest.fixture()
    def kakao_login_service(self, mocked_user_repository):
        return KakaoLoginService(
            http_service=HttpService(
                http_client=AioHttpClient(),
                config=config,
            ),
            config=config,
            user_repository=mocked_user_repository,
        )

    @pytest.mark.asyncio
    async def test_get_oauth_authorize_url(self, kakao_login_service):
        callback_url = f"{config.SERVER_HOST}/oauth/kakao/callback"
        redirect_uri = f"https://tito.kr/main"

        oauth_authorize_url = kakao_login_service.get_oauth_authorize_url(redirect_uri)

        parsed_url = urlparse(oauth_authorize_url)

        assert parsed_url.scheme == "https"
        assert parsed_url.netloc == "kauth.kakao.com"
        assert parsed_url.path == "/oauth/authorize"
        assert parsed_url.query == urlencode(
            {
                "client_id": config.KAKAO_CLIENT_ID,
                "redirect_uri": callback_url,
                "response_type": "code",
                "nonce": redirect_uri,
            }
        )

    @pytest.mark.asyncio
    async def test_redirect_url_with_access_token(
        self,
        mocker,
        kakao_login_service: KakaoLoginService,
        mocked_user_repository: Mock,
    ):
        mocker.patch(
            "src.service.http.HttpService.get_kakao_oauth_token",
            return_value=KakaoOauthTokenResponse(
                token_type="bearer",
                access_token="test_access_token",
                expires_in=21599,
                refresh_token="test_refresh_token",
                refresh_token_expires_in=5183999,
                scope=None,
                id_token="test_id_token",
            ),
        )

        mocker.patch(
            "src.service.http.HttpService.get_kakao_jwks",
            return_value=[
                JWK(
                    kty="RSA",
                    n="test_n",
                    e="test_e",
                    kid="test_kid",
                    alg="RS256",
                    use="sig",
                )
            ],
        )

        mocker.patch(
            "jwt.get_unverified_header",
            return_value={
                "alg": "RS256",
                "kid": "test_kid",
            },
        )

        mocker.patch(
            "jwt.decode",
            return_value={
                "iss": "https://kauth.kakao.com",
                "aud": "test_aud",
                "sub": "test_sub",
                "iat": 1629780000,
                "exp": 1629780000,
                "auth_time": 1629780000,
                "nonce": "https://tito.kr/main",
                "nickname": "test_nickname",
                "picture": "test_picture",
                "email": "test_email",
            },
        )

        redirect_url = await kakao_login_service.redirect_url_with_access_token(
            code="test_code",
        )

        parsed_url = urlparse(redirect_url)

        assert parsed_url.scheme == "https"
        assert parsed_url.netloc == "tito.kr"
        assert parsed_url.path == "/main"
        assert "accessToken" in parsed_url.query
