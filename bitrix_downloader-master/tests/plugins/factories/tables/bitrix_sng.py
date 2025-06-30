from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.infrastructure.database.tables import BitrixSNGTable


class BitrixSNGTableFactory(factory.Factory):
    class Meta:
        model = BitrixSNGTable

    id = factory.Sequence(lambda n: n)
    assigned_by_id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    stage_id = factory.Sequence(lambda n: f"stage_id_{n}")
    name = factory.Sequence(lambda n: f"name_{n}")
    last_name = factory.Sequence(lambda n: f"last_name_{n}")
    age = factory.Faker("word")
    birth_date = factory.Faker("word")
    passport = factory.Sequence(lambda n: n)
    alabuga_start_game = factory.Sequence(lambda n: n)
    refusal = factory.Sequence(lambda n: n if n % 8 == 0 else None)
    sex = factory.Sequence(lambda n: n if n % 9 == 0 else None)
    citizenship = factory.Sequence(lambda n: n)
    date_of_unloading = factory.Faker("date")
    date_of_the_first_touch = factory.Faker("date")
    date_receipt_of_passport = factory.Faker("date")
    project = factory.Faker("word")


@pytest.fixture
def create_bitrix_sng(session: AsyncSession) -> Callable:
    async def _create(**kwargs) -> BitrixSNGTable:
        bitrix_sng = BitrixSNGTableFactory(**kwargs)
        session.add(bitrix_sng)
        await session.commit()
        await session.flush(bitrix_sng)
        return bitrix_sng

    return _create
