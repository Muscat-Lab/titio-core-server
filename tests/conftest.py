import pytest
from fastapi.testclient import TestClient

from src.config import ConfigTemplate
from src.main import app
from src.models import model

ConfigTemplate.Config.env_file = ".env.test"

assert ConfigTemplate().Config.env_file == ".env.test"
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
