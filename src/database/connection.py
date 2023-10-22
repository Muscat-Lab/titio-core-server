import redis.asyncio as async_redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import ConfigTemplate, get_config


class SqlaEngine:
    def __init__(
        self,
        config: ConfigTemplate,
    ) -> None:
        self._engine = create_async_engine(config.db_uri, logging_name="sa_logger")

    @property
    def engine(self):
        return self._engine

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            bind=self._engine,
        )


async def get_db(
    config: ConfigTemplate = Depends(get_config),
):
    session = SqlaEngine(config).session()

    if session is None:
        raise Exception("session is not connected")
    try:
        yield session
    finally:
        await session.close()


class Redis:
    def __init__(
        self,
        config: ConfigTemplate,
    ) -> None:
        self.pool = async_redis.ConnectionPool.from_url(config.REDIS_URI)

    def client(self) -> async_redis.Redis:
        return async_redis.Redis(connection_pool=self.pool)


async def get_redis(
    config: ConfigTemplate = Depends(get_config),
):
    redis_client = Redis(config).client()

    if redis_client is None:
        raise Exception("redis is not connected")
    try:
        yield redis_client
    finally:
        await redis_client.aclose()
