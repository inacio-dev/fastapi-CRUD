from typing import List, TypeVar
from math import ceil

from app.core.schemas.pagination import Pagination

T = TypeVar("T")


async def set_pagination(
    items: List[T],
    page: int = 1,
    per_page: int = 20,
) -> Pagination[T]:
    # Get pagination information
    total_count = len(items)
    total_pages = ceil(total_count / per_page)
    offset = (page - 1) * per_page

    # Slice the list for pagination
    paginated_items = items[offset : offset + per_page]

    # Prepare response
    response = Pagination(
        count=total_count,
        total_pages=total_pages,
        current_page=page,
        per_page=per_page,
        next=page < total_pages,
        previous=page > 1,
        results=paginated_items,
    )

    return response
