from app.core.schemas.base import SchemaBase


class ExampleBase(SchemaBase):
    description: str | None = None

    class Config:
        from_attributes = True
        exclude_none = True


class Example(ExampleBase):
    class Config:
        from_attributes = True
