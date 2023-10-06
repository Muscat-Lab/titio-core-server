from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import ConfigTemplate, get_config


class SqlaEngine:
    def __init__(
        self,
        config: ConfigTemplate,
    ) -> None:
        self._engine = create_engine(
            config.db_uri,
            logging_name="sa_logger",
        )

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self) -> sessionmaker[Session]:
        return sessionmaker(
            autoflush=False, autocommit=False, expire_on_commit=False, bind=self._engine
        )


def get_db(
    config: ConfigTemplate = Depends(get_config),
):
    session = SqlaEngine(config).session()

    if session is None:
        raise Exception("session is not connected")
    try:
        yield session
    finally:
        session.close()
