from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")


class Pagination(BaseModel, Generic[T]):
    count: int  # Total de itens disponíveis
    total_pages: int  # Total de páginas disponíveis
    current_page: int  # Página atual
    per_page: int  # Itens por página
    next: bool | None  # Existe próxima página?
    previous: bool | None  # Existe página anterior?
    results: List[T]  # Resultados paginados
