from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.infrastructure.database.tables import AdWorldTable


class AdWorldTableFactory(factory.Factory):
    class Meta:
        model = AdWorldTable

    id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    stage_id = factory.Sequence(lambda n: f"stage_id_{n}")
    source_id = factory.Sequence(lambda n: f"source_id{n}")
    name = factory.Faker("word")
    surname = factory.Faker("word")


@pytest.fixture
def create_ad_world(session: AsyncSession) -> Callable:
    async def _create(**kwargs) -> AdWorldTable:
        ad_world = AdWorldTableFactory(**kwargs)
        session.add(ad_world)
        await session.commit()
        await session.flush(ad_world)
        return ad_world

    return _create
