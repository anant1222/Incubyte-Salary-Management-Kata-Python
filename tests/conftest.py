import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.db.database import Base, engine


@pytest.fixture
def reset_db() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(reset_db) -> Generator[TestClient, None, None]:
    with TestClient(create_app()) as test_client:
        yield test_client
