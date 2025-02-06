from datetime import datetime

from pydantic import BaseModel


class SchemaBase(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
        exclude_none = True
