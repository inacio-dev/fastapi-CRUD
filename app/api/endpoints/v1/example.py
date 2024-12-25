import os

from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from app.core.database.sync_db import get_db
from app.core.schemas.example import Example as example_schema
from app.core.schemas.pagination import Pagination
from app.utils.cache import custom_cache
from app.utils.enums import OrderDirection
from app.core.controllers.common import set_pagination


CACHE_TIMEOUT = os.getenv("CACHE_TIMEOUT", 30)

router = APIRouter()


@router.get(
    "/{id}",
    response_model=example_schema,
    response_model_exclude_none=True,
)
@custom_cache(expire=CACHE_TIMEOUT)
async def read_item_by_id(
    request: Request,
    fields: str = Query(None),
    db: Session = Depends(get_db),
):
    item = {"id": id, "fields": fields}

    return item


@router.get("", response_model=Pagination[example_schema] | list[example_schema], response_model_exclude_none=True)
@custom_cache(expire=CACHE_TIMEOUT)
async def read_items(
    request: Request,
    # List
    fields: str = Query(None),
    order: OrderDirection = Query(OrderDirection.desc),
    # Pagination
    page: int = Query(None, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    # Filters
    item_exact: str | None = Query(None),
    item_icontains: str | None = Query(None),
    item_in: str | None = Query(None),
    #
    db: Session = Depends(get_db),
):
    items = [
        {
            "page": page,
            "per_page": per_page,
            "fields": fields,
            "order": order,
            "item_exact": item_exact,
            "item_icontains": item_icontains,
            "item_in": item_in,
        }
    ]

    if page:
        return await set_pagination(items, page, per_page)

    return items
