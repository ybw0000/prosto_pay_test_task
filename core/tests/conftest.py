import asyncio
from typing import AsyncGenerator
from typing import Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from core.base.models import metadata
from core.conf.app import create_app
from core.conf.settings import Settings
from core.conf.settings import settings


def _create_db(test_db_name: str):
    engine = create_engine(settings.sync_sqlalchemy_database_uri)
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text('DROP DATABASE IF EXISTS "{}"'.format(test_db_name)))
        conn.execute(text('CREATE DATABASE "{}"'.format(test_db_name)))


def _drop_db(test_db_name: str):
    engine = create_engine(settings.sync_sqlalchemy_database_uri)

    with engine.connect() as conn:
        conn.execute(
            text(
                "SELECT pg_terminate_backend(pg_stat_activity.pid) "
                "FROM pg_stat_activity "
                "WHERE pg_stat_activity.datname = :db_name "
                "AND pid <> pg_backend_pid()"
            ),
            {"db_name": test_db_name},
        )

    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text('DROP DATABASE "{}"'.format(test_db_name)))


@pytest.fixture(scope="session")
def test_db_name() -> str:
    return "prosto_pay_test"


@pytest.fixture(scope="session")
def test_settings(test_db_name: str) -> Settings:
    return Settings(DATABASE_NAME=test_db_name)


@pytest.fixture(scope="session", autouse=True)
def db_engine(test_settings: Settings) -> Generator["Engine", None, None]:
    _create_db(test_settings.DATABASE_NAME)
    engine = create_engine(url=test_settings.sync_sqlalchemy_database_uri)
    metadata.create_all(engine)
    yield engine
    metadata.drop_all(engine)
    engine.dispose()
    _drop_db(test_settings.DATABASE_NAME)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_db_engine(test_settings: Settings) -> AsyncGenerator["AsyncEngine", None]:
    yield create_async_engine(test_settings.sqlalchemy_database_uri)


@pytest_asyncio.fixture(autouse=True, scope="function")
async def async_db_session(async_db_engine: AsyncEngine):
    session_local = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        expire_on_commit=False,
    )()

    yield session_local  # every test will get a new db session

    await session_local.rollback()  # rollback the transactions

    # truncate all tables
    for table in reversed(metadata.sorted_tables):
        await session_local.execute(text(f"TRUNCATE {table.name} CASCADE;"))
        await session_local.commit()

    await session_local.close()


@pytest_asyncio.fixture(scope="function")
async def http_client(app: "FastAPI") -> AsyncGenerator["AsyncClient", None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://test/api/v1/",
    ) as http_client:
        yield http_client


@pytest.fixture(scope="session")
def app(test_settings: Settings) -> "FastAPI":
    return create_app(test_settings)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
