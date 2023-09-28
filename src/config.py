from pydantic.v1 import BaseSettings


class ConfigTemplate(BaseSettings):
    DB_URI: str = "mysql+pymysql://user:user1234@localhost:3306/dev"
    SECRET_KEY: str = "secret"
    SERVER_HOST: str = "http://localhost:8000"
    KAKAO_CLIENT_ID: str = "3c197967ac7ccc836c6c0adea23698c5"
    KAKAO_API_HOST: str = "kauth.kakao.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "APP_"


config = ConfigTemplate()


def get_config() -> ConfigTemplate:
    return config
