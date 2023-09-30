from pydantic.v1 import BaseSettings


class ConfigTemplate(BaseSettings):
    DATABASE_USER: str = "user"
    DATABASE_PASSWORD: str = "user1234"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = "dev"

    SECRET_KEY: str = "secret"
    SERVER_HOST: str = "http://localhost:8000"
    KAKAO_CLIENT_ID: str = "3c197967ac7ccc836c6c0adea23698c5"
    KAKAO_API_HOST: str = "kauth.kakao.com"

    @property
    def db_uri(self) -> str:
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "APP_"


config = ConfigTemplate()


def get_config() -> ConfigTemplate:
    return config
