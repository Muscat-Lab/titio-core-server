import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from pydantic_settings import SettingsConfigDict

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


@pytest.fixture(autouse=True, scope="session")
def db():
    from src.database.connection import SqlaEngine

    engine = SqlaEngine(ConfigTemplate()).engine

    model.Base.metadata.create_all(engine)

    try:
        yield engine
    finally:
        model.Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture()
def session(db):
    from src.database.connection import SqlaEngine

    session = SqlaEngine(ConfigTemplate()).session()
    session.begin_nested()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


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
