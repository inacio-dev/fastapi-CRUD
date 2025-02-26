import os

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.controllers.drive import get_arquives_by_parent
from app.core.database.sync_db import get_db
from app.core.schemas.drive import ArquiveSchema
from app.utils.cache import custom_cache

CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", "30"))

router = APIRouter()


@router.get(
    "/arquives",
    response_model=list[ArquiveSchema],
    response_model_exclude_none=True,
)
@custom_cache(expire=CACHE_TIMEOUT)
async def list_arquives(
    request: Request, parent: str | None = None, db: Session = Depends(get_db)  # noqa: B008
) -> list[ArquiveSchema]:
    try:
        arquives = get_arquives_by_parent(parent, db)
        return [ArquiveSchema.model_validate(arquive) for arquive in arquives]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar arquives: {e!s}") from e
