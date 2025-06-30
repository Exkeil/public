from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.infrastructure.database.tables import AdSNGTable


class AdSNGTableFactory(factory.Factory):
    class Meta:
        model = AdSNGTable

    id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    stage_id = factory.Sequence(lambda n: f"stage_id_{n}")
    name = factory.Sequence(lambda n: f"name_{n}")
    source_id = factory.Sequence(lambda n: f"source_id_{n}")
    surname = factory.Faker("word")


@pytest.fixture
def create_ad_sng(session: AsyncSession) -> Callable:
    async def _create(**kwargs) -> AdSNGTable:
        ad_sng = AdSNGTableFactory(**kwargs)
        session.add(ad_sng)
        await session.commit()
        await session.flush(ad_sng)
        return ad_sng

    return _create
