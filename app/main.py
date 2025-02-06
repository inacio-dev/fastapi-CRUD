# import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.router import router as api_router
from app.redis import setup_redis_cache
from app.utils.logger import log_info, register_logging_middleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    log_info("Application is starting up")
    setup_redis_cache(app)

    # Inicializar e configurar o scheduler
    scheduler = AsyncIOScheduler()
    app.state.scheduler = scheduler

    # Adicionar tarefas diárias
    # scheduler.add_job(cost_center.cost_centers_daily_task, CronTrigger(hour=2, minute=0), id="daily_task_2am")

    # Iniciar o scheduler
    scheduler.start()

    # Adicionar tarefas ao iniciar
    # copy_db_task = asyncio.create_task(copy_telemetria_db(), name="copy_telemetria_db")
    # app.state.copy_db_task = copy_db_task

    yield

    # Shutdown
    scheduler.shutdown(wait=False)

    # Cancelar a task se ainda estiver rodando
    """ if not copy_db_task.done():
        copy_db_task.cancel()
        try:
            await copy_db_task
        except asyncio.CancelledError:
            log_info("Copy database task was cancelled during shutdown") """

    log_info("Application is shutting down")


app = FastAPI(
    title="FastAPI App",
    description="FastAPI application with PostgreSQL and logging",
    version="1.0.0",
    lifespan=lifespan,
)

register_logging_middleware(app)


@app.get("/")
async def home() -> JSONResponse:
    return JSONResponse(content={"message": "Welcome to the FastAPI App", "docs": "/docs", "redoc": "/redoc"})


app.include_router(api_router, prefix="/api")
