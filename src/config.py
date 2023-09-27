from pydantic.v1 import BaseSettings


class ConfigTemplate(BaseSettings):
    DB_URI: str = "mysql+pymysql://user:user1234@localhost:3306/dev"

    SECRET_KEY: str = "secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "APP_"


config = ConfigTemplate()
