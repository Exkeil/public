import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.domains.bitrix.repositories.bitrix import IBitrixRepository
from bitrix_downloader.infrastructure.database.repositories.bitrix import (
    BitrixRepository,
)


@pytest.fixture
def bitrix_repository(session: AsyncSession) -> IBitrixRepository:
    return BitrixRepository(session=session)
