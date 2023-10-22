import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from pydantic_settings import SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import ConfigTemplate
from src.main import app
from src.models import model

ConfigTemplate.model_config = SettingsConfigDict(
    env_file=".env.test", env_file_encoding="utf-8", env_prefix="APP_"
)

assert ConfigTemplate().model_config.get("env_file") == ".env.test"
assert ConfigTemplate().DATABASE_NAME == "dev-test"


@pytest.fixture()
def client():
    return TestClient(app=app)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(ConfigTemplate().db_uri)

    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture()
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(model.Base.metadata.create_all)

    sessionmaker = async_sessionmaker(
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        bind=engine,
    )

    async with sessionmaker() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(model.Base.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True, name="redis")
async def redis():
    from src.database.connection import Redis

    redis = Redis(ConfigTemplate())
    redis_client = redis.client()

    try:
        yield redis_client
    finally:
        await redis_client.flushdb()
        await redis_client.aclose()
        await redis.pool.disconnect()
