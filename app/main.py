import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import router as api_router
from app.redis import setup_redis_cache
from app.utils.logger import log_info, register_logging_middleware

DEBUG = os.getenv("DEBUG", "True").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE,OPTIONS").split(",")
CORS_HEADERS = os.getenv("CORS_HEADERS", "Authorization,Content-Type").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    log_info("Application is starting up")
    setup_redis_cache(app)

    # Inicializar e configurar o scheduler
    scheduler = AsyncIOScheduler()
    app.state.scheduler = scheduler

    # Iniciar o scheduler
    scheduler.start()

    log_info("Application is started")

    yield

    # Shutdown
    scheduler.shutdown(wait=False)

    log_info("Application is shutting down")


app = FastAPI(
    title="FastAPI App",
    description="FastAPI application with PostgreSQL and logging",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

register_logging_middleware(app)


@app.get("/")
async def home() -> JSONResponse:
    content = {"message": "Welcome to the FastAPI App"}

    if DEBUG:
        content.update({"docs": "/docs", "redoc": "/redoc"})

    return JSONResponse(content=content)


app.include_router(api_router, prefix="/api")
