from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.infrastructure.database.tables import BitrixWorldTable


class BitrixWorldTableFactory(factory.Factory):
    class Meta:
        model = BitrixWorldTable

    id = factory.Sequence(lambda n: n)
    assigned_by_id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    stage_id = factory.Sequence(lambda n: f"stage_id_{n}")
    first_name = factory.Faker("word")
    last_name = factory.Faker("word")
    age = factory.Faker("word")
    gender = factory.Sequence(lambda n: n)
    date_of_birth = factory.Faker("word")
    alabuga_start_simulation = factory.Sequence(lambda n: n)
    rejection = factory.Sequence(lambda n: n)
    citizenship_form = factory.Sequence(lambda n: n)
    passport = factory.Sequence(lambda n: n)
    passport_issue_date = factory.Faker("word")
    hundred_words = factory.Sequence(lambda n: n)
    first_touch_date = factory.Faker("word")
    upload_date = factory.Faker("word")
    project = factory.Sequence(lambda n: n)


@pytest.fixture
def create_bitrix_world(session: AsyncSession) -> Callable:
    async def _create(**kwargs) -> BitrixWorldTable:
        bitrix_world = BitrixWorldTableFactory(**kwargs)
        session.add(bitrix_world)
        await session.commit()
        await session.flush(bitrix_world)
        return bitrix_world

    return _create
