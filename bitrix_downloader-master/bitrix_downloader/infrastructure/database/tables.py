from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bitrix_downloader.infrastructure.database.base import (
    Base,
    IdentifiableMixin,
    TimestampedMixin,
)


class BitrixSNGTable(Base, TimestampedMixin, IdentifiableMixin):
    __tablename__ = "sng"
    __table_args__ = {"schema": "classic"}

    assigned_by_id: Mapped[str | None] = mapped_column(Integer, nullable=True)
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    stage_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    age: Mapped[str | None] = mapped_column(String(512), nullable=True)
    birth_date: Mapped[str | None] = mapped_column(String(512), nullable=True)
    passport: Mapped[int | None] = mapped_column(Integer, nullable=True)
    alabuga_start_game: Mapped[int | None] = mapped_column(Integer, nullable=True)
    refusal: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    citizenship: Mapped[int | None] = mapped_column(Integer, nullable=True)
    date_of_unloading: Mapped[str | None] = mapped_column(String(512), nullable=True)
    date_of_the_first_touch: Mapped[str | None] = mapped_column(
        String(512), nullable=True
    )
    date_receipt_of_passport: Mapped[str | None] = mapped_column(
        String(512), nullable=True
    )
    project: Mapped[str | None] = mapped_column(String(512), nullable=True)


class BitrixWorldTable(Base, TimestampedMixin, IdentifiableMixin):
    __tablename__ = "world"
    __table_args__ = {"schema": "classic"}

    assigned_by_id: Mapped[str] = mapped_column(Integer, nullable=False)
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(512), nullable=False)
    last_name: Mapped[str] = mapped_column(String(512), nullable=False)
    age: Mapped[str | None] = mapped_column(String(512), nullable=True)
    gender: Mapped[int | None] = mapped_column(Integer, nullable=True)
    date_of_birth: Mapped[str | None] = mapped_column(String(512), nullable=True)
    alabuga_start_simulation: Mapped[int] = mapped_column(Integer, nullable=False)
    rejection: Mapped[int | None] = mapped_column(Integer, nullable=True)
    citizenship_form: Mapped[int | None] = mapped_column(Integer, nullable=True)
    passport: Mapped[int] = mapped_column(Integer, nullable=False)
    passport_issue_date: Mapped[str | None] = mapped_column(String(512), nullable=True)
    hundred_words: Mapped[int] = mapped_column(Integer, nullable=False)
    first_touch_date: Mapped[str | None] = mapped_column(String(512), nullable=True)
    upload_date: Mapped[str | None] = mapped_column(String(512), nullable=True)
    project: Mapped[int | None] = mapped_column(Integer, nullable=True)
    stage_id: Mapped[str | None] = mapped_column(String(512), nullable=True)


class AdCallCenterTable(Base, TimestampedMixin, IdentifiableMixin):
    __tablename__ = "ad_call_center"
    __table_args__ = {"schema": "advertisement"}

    stage_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    source_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    user_name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    UTM_term: Mapped[str | None] = mapped_column(String(512), nullable=True)
    UTM_source: Mapped[str | None] = mapped_column(String(512), nullable=True)
    UTM_medium: Mapped[str | None] = mapped_column(String(512), nullable=True)
    UTM_content: Mapped[str | None] = mapped_column(String(512), nullable=True)
    UTM_campaign: Mapped[str | None] = mapped_column(String(512), nullable=True)
    lead_form: Mapped[int | None] = mapped_column(Integer, nullable=True)
    main_source: Mapped[str | None] = mapped_column(String(512), nullable=True)
    secondary_source4: Mapped[str | None] = mapped_column(String(512), nullable=True)
    secondary_source3: Mapped[str | None] = mapped_column(String(512), nullable=True)
    secondary_source2: Mapped[str | None] = mapped_column(String(512), nullable=True)
    secondary_source1: Mapped[str | None] = mapped_column(String(512), nullable=True)


class AdMassRecruitmentTable(Base, TimestampedMixin, IdentifiableMixin):
    __tablename__ = "ad_mass_recruitment"
    __table_args__ = {"schema": "advertisement"}

    stage_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    source_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    user_name: Mapped[str | None] = mapped_column(String(512), nullable=True)


class AdWorldTable(Base, TimestampedMixin, IdentifiableMixin):
    __tablename__ = "ad_world"
    __table_args__ = {"schema": "advertisement"}

    stage_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    source_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    surname: Mapped[str | None] = mapped_column(String(512), nullable=True)


class AdSNGTable(Base, TimestampedMixin, IdentifiableMixin):
    __tablename__ = "ad_sng"
    __table_args__ = {"schema": "advertisement"}

    stage_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    source_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    surname: Mapped[str | None] = mapped_column(String(512), nullable=True)


class BitrixMassSelectionTable(Base, TimestampedMixin, IdentifiableMixin):
    __tablename__ = "mass_selection"
    __table_args__ = {"schema": "mass_selection_schema"}

    stage: Mapped[str | None] = mapped_column(String(512), nullable=True)
    assessment_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    solution: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    comments: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    body_check: Mapped[int | None] = mapped_column(Integer, nullable=True)
    age: Mapped[float | None] = mapped_column(Float, nullable=True)
    employment_stage: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
