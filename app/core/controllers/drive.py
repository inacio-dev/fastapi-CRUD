from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models.drive import Arquive


def get_arquives_by_parent(parent: str | None = None, db: Session | None = None) -> list[Arquive]:
    if db is None:
        raise ValueError("Database session is required")

    query = select(Arquive)

    # Usando operador ternário para simplificar a lógica de filtragem
    query = query.where(Arquive.parent == parent) if parent is not None else query.where(Arquive.parent.is_(None))

    # Executar a query
    result = db.execute(query)
    arquives = result.scalars().all()

    return list(arquives)
