from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.infrastructure.database.tables import AdMassRecruitmentTable


class AdMassRecruitmentTableFactory(factory.Factory):
    class Meta:
        model = AdMassRecruitmentTable

    id = factory.Sequence(lambda n: n)
    stage_id = factory.Sequence(lambda n: f"stage_id{n}")
    source_id = factory.Sequence(lambda n: n)
    created_time = factory.Faker("date_time")
    user_name = factory.Faker("word")


@pytest.fixture
def create_mass_recruitment(session: AsyncSession) -> Callable:
    async def _create(**kwargs) -> AdMassRecruitmentTable:
        mass_recruitment = AdMassRecruitmentTableFactory(**kwargs)
        session.add(mass_recruitment)
        await session.commit()
        await session.flush(mass_recruitment)
        return mass_recruitment

    return _create
