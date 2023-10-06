import enum


class ErrCode(str, enum.Enum):
    HttpClientError = "HttpClientError"
    KakaoUnknownError = "KakaoUnknownError"
    KakaoTokenExpired = "KakaoTokenExpired"
    KakaoTokenVerifyError = "KakaoTokenVerifyError"
    KakaoTokenVerifyFailed = "KakaoTokenVerifyFailed"

    @property
    def message(self):
        return {
            ErrCode.HttpClientError: "HTTP 요청 중 에러가 발생했습니다.",
            ErrCode.KakaoUnknownError: (
                "카카오 API 서버에서 알 수 없는 에러가 발생했습니다."
            ),
            ErrCode.KakaoTokenExpired: "카카오 토큰이 만료되었습니다.",
            ErrCode.KakaoTokenVerifyError: "카카오 토큰 검증 중 에러가 발생했습니다.",
            ErrCode.KakaoTokenVerifyFailed: "카카오 토큰 검증에 실패했습니다.",
        }[self]


class ServiceException(Exception):
    def __init__(
        self, error_code: ErrCode, status_code: int = 500, message: str = ""
    ) -> None:
        self.status_code = status_code
        self.message = message or error_code.message
        self.error_code = error_code
