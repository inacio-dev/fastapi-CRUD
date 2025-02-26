from fastapi import APIRouter

from . import drive

router = APIRouter()

router.include_router(drive.router, prefix="/drive", tags=["drive"])
