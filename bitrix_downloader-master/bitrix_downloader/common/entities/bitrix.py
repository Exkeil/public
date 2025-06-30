from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from msgspec import field

from bitrix_downloader.common.entities.base import Entity


class BitrixModel(Entity, frozen=True):
    id: int
    properties: Mapping[str, Any]


class BitrixSNGModel(Entity, frozen=True):
    id: int = field(name="id")
    assigned_by_id: int = field(name="assignedById")
    created_time: datetime = field(name="createdTime")
    stage_id: str = field(name="stageId")
    name: str = field(name="ufCrm23_1710937794")
    last_name: str = field(name="ufCrm23_1710937991")
    age: str = field(name="ufCrm23_1710938033")
    birth_date: str | None = field(name="ufCrm23_1710938474")
    passport: int = field(name="ufCrm23_1710939449")
    alabuga_start_game: int = field(name="ufCrm23_1710942062")
    refusal: int | None = field(name="ufCrm23_1710942433")
    sex: int | None = field(name="ufCrm23_1710945931")
    citizenship: int | None = field(name="ufCrm23_1710947671")
    date_of_unloading: str | None = field(name="ufCrm23_1716619640273")
    date_of_the_first_touch: str | None = field(name="ufCrm23_1716622092407")
    date_receipt_of_passport: str | None = field(name="ufCrm23_1716817266")
    project: str | None = field(name="ufCrm23_1716879053")


class BitrixWorldModel(Entity, frozen=True):
    id: int = field(name="id")
    assigned_by_id: int | None = field(name="assignedById")
    created_time: datetime = field(name="createdTime")
    stage_id: str | None = field(name="stageId")
    first_name: str | None = field(name="ufCrm20_1710308337539")
    last_name: str | None = field(name="ufCrm20_1710308353693")
    age: str | None = field(name="ufCrm20_1710308372853")
    gender: int | None = field(name="ufCrm20_1710308497445")
    date_of_birth: str | None = field(name="ufCrm20_1710309130539")
    alabuga_start_simulation: int | None = field(name="ufCrm20_1710492855399")
    rejection: int | None = field(name="ufCrm20_1710493359806")
    citizenship_form: int | None = field(name="ufCrm20_1710833955002")
    passport: int | None = field(name="ufCrm20_1711029907")
    passport_issue_date: str | None = field(name="ufCrm20_1712566725")
    hundred_words: int | None = field(name="ufCrm20_1712923122")
    first_touch_date: str | None = field(name="ufCrm20_1714739083")
    upload_date: str | None = field(name="ufCrm20_1715346103")
    project: int | None = field(name="ufCrm20_1716798467")


class AdWorldModel(Entity, frozen=True):
    id: int = field(name="id")
    created_time: datetime = field(name="createdTime")
    stage_id: str | None = field(name="stageId")
    source_id: str | None = field(name="ufCrm20_1716909279")
    name: str | None = field(name="ufCrm20_1710308337539")
    surname: str | None = field(name="ufCrm20_1710308353693")


class AdSNGModel(Entity, frozen=True):
    id: int = field(name="id")
    created_time: datetime = field(name="createdTime")
    stage_id: str | None = field(name="stageId")
    source_id: str | None = field(name="ufCrm23_1716909298")
    name: str = field(name="ufCrm23_1710937794")
    surname: str = field(name="ufCrm23_1710937991")


class AdMassRecruitmentModel(Entity, frozen=True):
    id: int = field(name="id")
    stage_id: str | None = field(name="stageId")
    source_id: int | None = field(name="ufCrm5_1717078179")
    created_time: datetime = field(name="createdTime")
    user_name: str | None = field(name="ufCrm5_1706947526")


class AdCallCenterModel(Entity, frozen=True):
    id: int = field(name="id")
    stage_id: str | None = field(name="stageId")
    source_id: str | None = field(name="sourceId")
    created_time: datetime = field(name="createdTime")
    user_name: str | None = field(name="ufCrm15_1708599858537")
    UTM_term: str | None = field(name="ufCrm15_1709032200935")
    UTM_source: str | None = field(name="ufCrm15_1709032219283")
    UTM_medium: str | None = field(name="ufCrm15_1709032128595")
    UTM_content: str | None = field(name="ufCrm15_1709032182621")
    UTM_campaign: str | None = field(name="ufCrm15_1709032153650")
    lead_form: int | None = field(name="ufCrm15_1713513061")
    main_source: str | None = field(name="ufCrm15_1708584336136")
    secondary_source4: str | None = field(name="ufCrm15_1708584391194")
    secondary_source3: str | None = field(name="ufCrm15_1708584379794")
    secondary_source2: str | None = field(name="ufCrm15_1708584366043")
    secondary_source1: str | None = field(name="ufCrm15_1708584351136")


class BitrixMassSelectionModel(Entity, frozen=True):
    id: int = field(name="id")
    stage: str | None = field(name="stageId")
    assessment_date: datetime | None = field(name="ufCrm5_1706447447")
    solution: int | None = field(name="ufCrm5_1710238329892")
    user_name: str | None = field(name="ufCrm5_1706947526")
    comments: int | None = field(name="ufCrm5_1710237996027")
    sp: int | None = field(name="ufCrm5_1710238078012")
    body_check: int | None = field(name="ufCrm5_1710239649116")
    age: float | None = field(name="ufCrm5_1706447172")
    employment_stage: datetime | None = field(name="ufCrm5_1706860136")


class BitrixSNGModelResultApplicant(Entity, frozen=True):
    items: Sequence[BitrixSNGModel]


class BitrixSNGApplicantPage(Entity, frozen=True):
    result: BitrixSNGModelResultApplicant
    next: int | None = None


class BitrixWorldModelResultApplicant(Entity, frozen=True):
    items: Sequence[BitrixWorldModel]


class BitrixWorldApplicantPage(Entity, frozen=True):
    result: BitrixWorldModelResultApplicant
    next: int | None = None


class AdSNGModelResultApplicant(Entity, frozen=True):
    items: Sequence[AdSNGModel]


class AdSNGApplicantPage(Entity, frozen=True):
    result: AdSNGModelResultApplicant
    next: int | None = None


class AdWorldModelResultApplicant(Entity, frozen=True):
    items: Sequence[AdWorldModel]


class AdWorldApplicantPage(Entity, frozen=True):
    result: AdWorldModelResultApplicant
    next: int | None = None


class AdMassRecruitmentModelResultApplicant(Entity, frozen=True):
    items: Sequence[AdMassRecruitmentModel]


class AdMassRecruitmentApplicantPage(Entity, frozen=True):
    result: AdMassRecruitmentModelResultApplicant
    next: int | None = None


class AdCallCenterModelResultApplicant(Entity, frozen=True):
    items: Sequence[AdCallCenterModel]


class AdCallCenterApplicantPage(Entity, frozen=True):
    result: AdCallCenterModelResultApplicant
    next: int | None = None


class BitrixMassSelectionResult(Entity, frozen=True):
    items: Sequence[BitrixMassSelectionModel]


class BitrixMassSelectionPage(Entity, frozen=True):
    result: BitrixMassSelectionResult
    next: int | None = None
