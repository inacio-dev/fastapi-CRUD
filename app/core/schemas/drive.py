from app.core.models.drive import ArquiveType
from app.core.schemas.base import SchemaBase


class ArquiveSchema(SchemaBase):
    google_id: str
    name: str
    mime_type: str
    type: ArquiveType
    parent: str | None

    class Config:
        from_attributes = True
        exclude_none = True
        use_enum_values = True
