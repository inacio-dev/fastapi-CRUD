import os

from datetime import datetime
from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.sync_db import Base


class AbstractModel(Base):
    __abstract__ = True
    __table_args__ = {"schema": os.getenv("POSTGRES_SCHEMA", "public")}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
