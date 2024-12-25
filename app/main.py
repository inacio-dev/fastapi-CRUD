import asyncio

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.redis import setup_redis_cache
from app.api.router import router as api_router
from app.utils.logger import register_logging_middleware, log_info
from app.core.tasks.example import set_example_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    log_info("Application is starting up")
    setup_redis_cache(app)

    # Inicializar e configurar o scheduler
    scheduler = AsyncIOScheduler()
    app.state.scheduler = scheduler

    # Adicionar tarefas diárias
    scheduler.add_job(set_example_task, CronTrigger(hour=2, minute=0), id="daily_task_2am")

    # Iniciar o scheduler
    scheduler.start()

    asyncio.create_task(set_example_task())

    yield

    # Shutdown
    scheduler.shutdown(wait=False)
    log_info("Application is shutting down")


app = FastAPI(
    title="FastAPI App",
    description="FastAPI application with PostgreSQL and logging",
    version="1.0.0",
    lifespan=lifespan,
)

register_logging_middleware(app)


@app.get("/")
async def home():
    return JSONResponse(content={"message": "Welcome to the FastAPI App", "docs": "/docs", "redoc": "/redoc"})


app.include_router(api_router, prefix="/api")
