from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.infrastructure.database.tables import BitrixMassSelectionTable


class BitrixMassSelectionTableFactory(factory.Factory):
    class Meta:
        model = BitrixMassSelectionTable

    id = factory.Sequence(lambda n: n)
    stage = factory.Sequence(lambda n: f"stage_id_{n}")
    assessment_date = factory.Faker("date_time")
    solution = factory.Sequence(lambda n: n)
    user_name = factory.Sequence(lambda n: f"stage_id_{n}")
    comments = factory.Sequence(lambda n: n)
    sp = factory.Sequence(lambda n: n)
    body_check = factory.Sequence(lambda n: n)
    age = factory.Sequence(lambda n: n)
    employment_stage = factory.Faker("date_time")


@pytest.fixture
def create_bitrix_mass_selection(session: AsyncSession) -> Callable:
    async def _create(**kwargs) -> BitrixMassSelectionTable:
        bitrix_mass_selection = BitrixMassSelectionTableFactory(**kwargs)
        session.add(bitrix_mass_selection)
        await session.commit()
        await session.flush(bitrix_mass_selection)
        return bitrix_mass_selection

    return _create
