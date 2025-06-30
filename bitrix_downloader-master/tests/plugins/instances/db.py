from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.schema import CreateSchema

from bitrix_downloader.args import Parser
from bitrix_downloader.infrastructure.database.tables import Base
from bitrix_downloader.infrastructure.database.utils import (
    create_engine,
    create_session_factory,
)


@pytest.fixture(scope="session")
def pg_url(parser: Parser) -> str:
    return parser.database.url


@pytest.fixture
async def engine(pg_url: str) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_engine(url=pg_url, debug=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(CreateSchema("classic", if_not_exists=True))
        await conn.execute(CreateSchema("advertisement", if_not_exists=True))
        await conn.execute(CreateSchema("mass_selection_schema", if_not_exists=True))
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return create_session_factory(engine=engine)


@pytest.fixture
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
