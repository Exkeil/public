from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.infrastructure.database.tables import AdCallCenterTable


class AdCallCenterTableFactory(factory.Factory):
    class Meta:
        model = AdCallCenterTable

    id = factory.Sequence(lambda n: n)

    stage_id = factory.Sequence(lambda n: f"stage_id{n}")
    source_id = factory.Sequence(lambda n: f"source_id{n}")
    created_time = factory.Faker("date_time")
    user_name = factory.Faker("word")
    UTM_term = factory.Faker("word")
    UTM_source = factory.Faker("word")
    UTM_medium = factory.Faker("word")
    UTM_content = factory.Faker("word")
    UTM_campaign = factory.Faker("word")
    lead_form = factory.Sequence(lambda n: n)
    main_source = factory.Faker("word")
    secondary_source4 = factory.Faker("word")
    secondary_source3 = factory.Faker("word")
    secondary_source2 = factory.Faker("word")
    secondary_source1 = factory.Faker("word")


@pytest.fixture
def create_call_center(session: AsyncSession) -> Callable:
    async def _create(**kwargs) -> AdCallCenterTable:
        call_center = AdCallCenterTableFactory(**kwargs)
        session.add(call_center)
        await session.commit()
        await session.flush(call_center)
        return call_center

    return _create
