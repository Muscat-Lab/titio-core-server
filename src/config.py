import os.path

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigTemplate(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.expandvars(".env"),
        env_file_encoding="utf-8",
        env_prefix="APP_",
    )

    DATABASE_USER: str = "user"
    DATABASE_PASSWORD: str = "user1234"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = "dev"

    SECRET_KEY: str = "secret"
    SERVER_HOST: str = "http://localhost:8000"
    KAKAO_CLIENT_ID: str = "3c197967ac7ccc836c6c0adea23698c5"
    KAKAO_API_HOST: str = "kauth.kakao.com"

    AWS_ACCESS_KEY_ID: str = "minio"
    AWS_SECRET_ACCESS_KEY: str = "minio1234"
    AWS_S3_ENDPOINT_URL: str = "http://localhost:9000"
    AWS_S3_BUCKET_NAME: str = "dev"

    MAX_UPLOAD_IMAGE_SIZE: int = 1024 * 1024 * 10  # 10MB

    REDIS_URI: str = "redis://redis:6379/0"

    @property
    def db_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )


config = ConfigTemplate()


def get_config() -> ConfigTemplate:
    return config
