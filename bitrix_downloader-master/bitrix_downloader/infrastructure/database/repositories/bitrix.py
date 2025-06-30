from collections.abc import Sequence

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bitrix_downloader.common.entities.bitrix import (
    AdCallCenterModel,
    AdMassRecruitmentModel,
    AdSNGModel,
    AdWorldModel,
    BitrixMassSelectionModel,
    BitrixSNGModel,
    BitrixWorldModel,
)
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


class BitrixRepository(IBitrixRepository):
    def __init__(self, *, session: AsyncSession) -> None:
        self.__session = session

    async def create_many_sng(self, *, items: Sequence[BitrixSNGModel]) -> None:
        if not items:
            return None
        stmt = insert(BitrixSNGTable).values([item.to_dict() for item in items])
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "id": stmt.excluded.id,
                "assigned_by_id": stmt.excluded.assigned_by_id,
                "created_time": stmt.excluded.created_time,
                "stage_id": stmt.excluded.stage_id,
                "name": stmt.excluded.name,
                "last_name": stmt.excluded.last_name,
                "age": stmt.excluded.age,
                "birth_date": stmt.excluded.birth_date,
                "passport": stmt.excluded.passport,
                "alabuga_start_game": stmt.excluded.alabuga_start_game,
                "refusal": stmt.excluded.refusal,
                "sex": stmt.excluded.sex,
                "citizenship": stmt.excluded.citizenship,
                "date_of_unloading": stmt.excluded.date_of_unloading,
                "date_of_the_first_touch": stmt.excluded.date_of_the_first_touch,
                "date_receipt_of_passport": stmt.excluded.date_receipt_of_passport,
                "project": stmt.excluded.project,
            },
        )
        await self.__session.execute(stmt)

    async def create_many_world(self, *, items: Sequence[BitrixWorldModel]) -> None:
        if not items:
            return None
        stmt = insert(BitrixWorldTable).values([item.to_dict() for item in items])
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "id": stmt.excluded.id,
                "assigned_by_id": stmt.excluded.assigned_by_id,
                "created_time": stmt.excluded.created_time,
                "first_name": stmt.excluded.first_name,
                "last_name": stmt.excluded.last_name,
                "age": stmt.excluded.age,
                "gender": stmt.excluded.gender,
                "date_of_birth": stmt.excluded.date_of_birth,
                "alabuga_start_simulation": stmt.excluded.alabuga_start_simulation,
                "rejection": stmt.excluded.rejection,
                "citizenship_form": stmt.excluded.citizenship_form,
                "passport": stmt.excluded.passport,
                "passport_issue_date": stmt.excluded.passport_issue_date,
                "hundred_words": stmt.excluded.hundred_words,
                "first_touch_date": stmt.excluded.first_touch_date,
                "upload_date": stmt.excluded.upload_date,
                "project": stmt.excluded.project,
                "stage_id": stmt.excluded.stage_id,
            },
        )
        await self.__session.execute(stmt)

    async def create_many_ad_sng(self, *, items: Sequence[AdSNGModel]) -> None:
        if not items:
            return None
        stmt = insert(AdSNGTable).values([item.to_dict() for item in items])
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "id": stmt.excluded.id,
                "created_time": stmt.excluded.created_time,
                "stage_id": stmt.excluded.stage_id,
                "name": stmt.excluded.name,
                "surname": stmt.excluded.surname,
                "source_id": stmt.excluded.source_id,
            },
        )
        await self.__session.execute(stmt)

    async def create_many_ad_world(self, *, items: Sequence[AdWorldModel]) -> None:
        if not items:
            return None
        stmt = insert(AdWorldTable).values([item.to_dict() for item in items])
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "id": stmt.excluded.id,
                "created_time": stmt.excluded.created_time,
                "name": stmt.excluded.name,
                "surname": stmt.excluded.surname,
                "stage_id": stmt.excluded.stage_id,
                "source_id": stmt.excluded.source_id,
            },
        )
        await self.__session.execute(stmt)

    async def create_many_ad_mass_recruitment(
        self, *, items: Sequence[AdMassRecruitmentModel]
    ) -> None:
        if not items:
            return None
        stmt = insert(AdMassRecruitmentTable).values([item.to_dict() for item in items])
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "id": stmt.excluded.id,
                "stage_id": stmt.excluded.stage_id,
                "created_time": stmt.excluded.created_time,
                "source_id": stmt.excluded.source_id,
                "user_name": stmt.excluded.user_name,
            },
        )
        await self.__session.execute(stmt)

    async def create_many_ad_call_center(
        self, *, items: Sequence[AdCallCenterModel]
    ) -> None:
        if not items:
            return None
        stmt = insert(AdCallCenterTable).values([item.to_dict() for item in items])
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "id": stmt.excluded.id,
                "stage_id": stmt.excluded.stage_id,
                "source_id": stmt.excluded.source_id,
                "created_time": stmt.excluded.created_time,
                "user_name": stmt.excluded.user_name,
                "UTM_term": stmt.excluded.UTM_term,
                "UTM_source": stmt.excluded.UTM_source,
                "UTM_medium": stmt.excluded.UTM_medium,
                "UTM_content": stmt.excluded.UTM_content,
                "UTM_campaign": stmt.excluded.UTM_campaign,
                "lead_form": stmt.excluded.lead_form,
                "main_source": stmt.excluded.main_source,
                "secondary_source4": stmt.excluded.secondary_source4,
                "secondary_source3": stmt.excluded.secondary_source3,
                "secondary_source2": stmt.excluded.secondary_source2,
                "secondary_source1": stmt.excluded.secondary_source1,
            },
        )
        await self.__session.execute(stmt)

    async def create_many_mass_selection(
        self, *, items: Sequence[BitrixMassSelectionModel]
    ) -> None:
        if not items:
            return None
        stmt = insert(BitrixMassSelectionTable).values(
            [item.to_dict() for item in items]
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "stage": stmt.excluded.stage,
                "assessment_date": stmt.excluded.assessment_date,
                "solution": stmt.excluded.solution,
                "user_name": stmt.excluded.user_name,
                "comments": stmt.excluded.comments,
                "sp": stmt.excluded.sp,
                "body_check": stmt.excluded.body_check,
                "age": stmt.excluded.age,
                "employment_stage": stmt.excluded.employment_stage,
            },
        )
        await self.__session.execute(stmt)
