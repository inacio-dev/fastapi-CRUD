import os
from datetime import UTC, datetime
from typing import ClassVar

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import SchemaItem

from app.core.database.sync_db import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class AbstractModel(Base):
    __abstract__ = True
    __table_args__: ClassVar[dict[str, str] | SchemaItem] = {"schema": os.getenv("POSTGRES_SCHEMA", "public")}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
