import enum
import os

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import AbstractModel

POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")


class ArquiveType(enum.Enum):
    FOLDER = "folder"
    FILE = "file"


class Arquive(AbstractModel):
    __tablename__ = "arquives"

    google_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(255), nullable=False)

    type: Mapped[ArquiveType] = mapped_column(Enum(ArquiveType, schema=POSTGRES_SCHEMA), nullable=False)
    parent: Mapped[str | None] = mapped_column(String(255), nullable=True)
