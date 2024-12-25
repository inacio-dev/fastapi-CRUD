from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import AbstractModel


class Example(AbstractModel):
    __tablename__ = "examples"

    description: Mapped[str] = mapped_column(String(512), default="")
