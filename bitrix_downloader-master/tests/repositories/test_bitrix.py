from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.domains.bitrix.repositories.bitrix import IBitrixRepository
from bitrix_downloader.infrastructure.database.tables import (
    AdCallCenterTable,
    AdMassRecruitmentTable,
    AdSNGTable,
    AdWorldTable,
    BitrixMassSelectionTable,
    BitrixSNGTable,
    BitrixWorldTable,
)
from tests.plugins.factories.entities.ad_call_center import AdCallCenterModelFactory
from tests.plugins.factories.entities.ad_mass_recruitment import (
    AdMassRecruitmentModelFactory,
)
from tests.plugins.factories.entities.ad_sng import AdSNGModelFactory
from tests.plugins.factories.entities.ad_world import AdWorldModelFactory
from tests.plugins.factories.entities.bitrix_mass_selection import (
    BitrixMassSelectionTableFactory,
)
from tests.plugins.factories.entities.bitrix_sng import BitrixSNGModelFactory
from tests.plugins.factories.entities.bitrix_world import BitrixWorldModelFactory


async def test_create_many_sng_empty(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_sng(items=[])
    assert await session.scalar(select(func.count()).select_from(BitrixSNGTable)) == 0


async def test_create_many_sng_one(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_sng(items=[BitrixSNGModelFactory()])
    assert await session.scalar(select(func.count()).select_from(BitrixSNGTable)) == 1


async def test_create_many_sng_many(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_sng(
        items=[BitrixSNGModelFactory() for _ in range(5)]
    )
    assert await session.scalar(select(func.count()).select_from(BitrixSNGTable)) == 5


async def test_create_many_sng_duplicate(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
    create_bitrix_sng,
):
    bitrix_sng = await create_bitrix_sng()
    await bitrix_repository.create_many_sng(
        items=[BitrixSNGModelFactory(id=bitrix_sng.id)]
    )
    assert await session.scalar(select(func.count()).select_from(BitrixSNGTable)) == 1


async def test_create_many_world_empty(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_world(items=[])
    assert await session.scalar(select(func.count()).select_from(BitrixWorldTable)) == 0


async def test_create_many_world_one(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_world(items=[BitrixWorldModelFactory()])
    assert await session.scalar(select(func.count()).select_from(BitrixWorldTable)) == 1


async def test_create_many_world_many(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_world(
        items=[BitrixWorldModelFactory() for _ in range(4)]
    )
    assert await session.scalar(select(func.count()).select_from(BitrixWorldTable)) == 4


async def test_create_many_world_duplicate(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
    create_bitrix_world,
):
    bitrix_world = await create_bitrix_world()
    await bitrix_repository.create_many_world(
        items=[BitrixWorldModelFactory(id=bitrix_world.id)]
    )
    assert await session.scalar(select(func.count()).select_from(BitrixWorldTable)) == 1


async def test_create_many_ad_sng_empty(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_sng(items=[])
    assert await session.scalar(select(func.count()).select_from(AdSNGTable)) == 0


async def test_create_many_ad_sng_one(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_sng(items=[AdSNGModelFactory()])
    assert await session.scalar(select(func.count()).select_from(AdSNGTable)) == 1


async def test_create_many_ad_sng_many(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_sng(
        items=[AdSNGModelFactory() for _ in range(5)]
    )
    assert await session.scalar(select(func.count()).select_from(AdSNGTable)) == 5


async def test_create_many_ad_sng_duplicate(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
    create_ad_sng,
):
    ad_sng = await create_ad_sng()
    await bitrix_repository.create_many_ad_sng(items=[AdSNGModelFactory(id=ad_sng.id)])
    assert await session.scalar(select(func.count()).select_from(AdSNGTable)) == 1


async def test_create_many_ad_world_empty(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_world(items=[])
    assert await session.scalar(select(func.count()).select_from(AdWorldTable)) == 0


async def test_create_many_ad_world_one(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_world(items=[AdWorldModelFactory()])
    assert await session.scalar(select(func.count()).select_from(AdWorldTable)) == 1


async def test_create_many_ad_world_many(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_world(
        items=[AdWorldModelFactory() for _ in range(4)]
    )
    assert await session.scalar(select(func.count()).select_from(AdWorldTable)) == 4


async def test_create_many_ad_world_duplicate(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
    create_ad_world,
):
    ad_world = await create_ad_world()
    await bitrix_repository.create_many_ad_world(
        items=[AdWorldModelFactory(id=ad_world.id)]
    )
    assert await session.scalar(select(func.count()).select_from(AdWorldTable)) == 1


async def test_create_many_ad_call_center_empty(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_call_center(items=[])
    assert (
        await session.scalar(select(func.count()).select_from(AdCallCenterTable)) == 0
    )


async def test_create_many_ad_call_center_one(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_call_center(
        items=[AdCallCenterModelFactory()]
    )
    assert (
        await session.scalar(select(func.count()).select_from(AdCallCenterTable)) == 1
    )


async def test_create_many_ad_call_center_many(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_call_center(
        items=[AdCallCenterModelFactory() for _ in range(4)]
    )
    assert (
        await session.scalar(select(func.count()).select_from(AdCallCenterTable)) == 4
    )


async def test_create_many_ad_call_center_duplicate(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
    create_call_center,
):
    call_center = await create_call_center()
    await bitrix_repository.create_many_ad_call_center(
        items=[AdCallCenterModelFactory(id=call_center.id)]
    )
    assert (
        await session.scalar(select(func.count()).select_from(AdCallCenterTable)) == 1
    )


async def test_create_many_ad_mass_recruitment_empty(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_mass_recruitment(items=[])
    assert (
        await session.scalar(select(func.count()).select_from(AdMassRecruitmentTable))
        == 0
    )


async def test_create_many_ad_mass_recruitment_one(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_mass_recruitment(
        items=[AdMassRecruitmentModelFactory()]
    )
    assert (
        await session.scalar(select(func.count()).select_from(AdMassRecruitmentTable))
        == 1
    )


async def test_create_many_ad_mass_recruitment_many(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_ad_mass_recruitment(
        items=[AdMassRecruitmentModelFactory() for _ in range(4)]
    )
    assert (
        await session.scalar(select(func.count()).select_from(AdMassRecruitmentTable))
        == 4
    )


async def test_create_many_ad_mass_recruitment_duplicate(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
    create_mass_recruitment,
):
    mass_recruitment = await create_mass_recruitment()
    await bitrix_repository.create_many_ad_mass_recruitment(
        items=[AdMassRecruitmentModelFactory(id=mass_recruitment.id)]
    )
    assert (
        await session.scalar(select(func.count()).select_from(AdMassRecruitmentTable))
        == 1
    )


async def test_create_many_mass_selection_empty(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_mass_selection(items=[])
    assert (
        await session.scalar(select(func.count()).select_from(BitrixMassSelectionTable))
        == 0
    )


async def test_create_many_mass_selection_one(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_mass_selection(
        items=[BitrixMassSelectionTableFactory()]
    )
    assert (
        await session.scalar(select(func.count()).select_from(BitrixMassSelectionTable))
        == 1
    )


async def test_create_many_mass_selection_many(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
):
    await bitrix_repository.create_many_mass_selection(
        items=[BitrixMassSelectionTableFactory() for _ in range(4)]
    )
    assert (
        await session.scalar(select(func.count()).select_from(BitrixMassSelectionTable))
        == 4
    )


async def test_create_many_mass_selection_duplicate(
    bitrix_repository: IBitrixRepository,
    session: AsyncSession,
    create_bitrix_world,
):
    bitrix_world = await create_bitrix_world()
    await bitrix_repository.create_many_mass_selection(
        items=[BitrixMassSelectionTableFactory(id=bitrix_world.id)]
    )
    assert (
        await session.scalar(select(func.count()).select_from(BitrixMassSelectionTable))
        == 1
    )
