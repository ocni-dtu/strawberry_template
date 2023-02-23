import time
from typing import Generator

import docker
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from core.config import settings
from core.connection import create_postgres_engine


@pytest.fixture(scope="session")
def docker_client():
    yield docker.from_env()


@pytest.fixture(scope="session")
def postgres(docker_client):
    container = docker_client.containers.run(
        "postgres:13.1-alpine",
        ports={"5432": settings.POSTGRES_PORT},
        environment={
            "POSTGRES_DB": settings.POSTGRES_DB,
            "POSTGRES_PASSWORD": settings.POSTGRES_PASSWORD,
            "POSTGRES_USER": settings.POSTGRES_USER,
        },
        detach=True,
        auto_remove=True,
    )

    time.sleep(3)
    try:
        yield container
    finally:
        container.stop()


@pytest.fixture()
def db(postgres):
    engine = create_postgres_engine()
    SQLModel.metadata.create_all(engine)

    yield engine

    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def client(db) -> Generator:
    from main import app

    with TestClient(app=app, base_url=settings.SERVER_HOST) as _client:
        try:
            yield _client
        except Exception as exc:
            print(exc)
