from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, MetaData, text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()],
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)  # type: ignore[arg-type]


def now_with_tz() -> datetime:
    return datetime.now(tz=UTC)


class TimestampedMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_with_tz,
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_with_tz,
        onupdate=now_with_tz,
        server_default=text("TIMEZONE('utc', now())"),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, index=True
    )


class IdentifiableMixin:
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
    )
