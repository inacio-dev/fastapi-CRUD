import asyncio
import json
import sys
import time
import traceback
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, Response
from loguru import logger
from pydantic import BaseModel


class LogConfig(BaseModel):
    LOGGER_NAME: str = "fastapi_app"
    LOG_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    LOG_LEVEL: str = "DEBUG"


def setup_logging() -> None:
    config = LogConfig()

    # Get the base directory (2 levels up from the current file)
    base_dir = Path(__file__).parent.parent.parent
    logs_dir = base_dir / "logs"

    # Create logs directory if it doesn't exist
    logs_dir.mkdir(exist_ok=True)

    # Remove default logger
    logger.remove()

    # Add stdout handler
    logger.add(sys.stdout, format=config.LOG_FORMAT, level=config.LOG_LEVEL, enqueue=True)

    # Add rotating file handler for general logs
    logger.add(
        str(logs_dir / "app.log"),
        format=config.LOG_FORMAT,
        level=config.LOG_LEVEL,
        rotation="5 MB",
        retention="10 days",
        compression="zip",
        enqueue=True,
        serialize=True,
    )

    # Add rotating file handler for debug logs
    logger.add(
        str(logs_dir / "debug_{time:DD-MM-YYYY}.txt"),
        format=config.LOG_FORMAT,
        level="DEBUG",
        rotation="5 MB",
        retention="5 days",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )


def register_logging_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next: Callable[[Request], Any]) -> Response:
        start_time = time.time()
        trace_id = str(uuid.uuid4())

        # Add trace_id to request state
        request.state.trace_id = trace_id

        try:
            response: Response = await call_next(request)

            # Log successful requests
            log_data = {
                "trace_id": trace_id,
                "status_code": response.status_code,
                "method": request.method,
                "host": request.url.hostname,
                "endpoint": request.url.path,
                "processing_time": round(time.time() - start_time, 4),
                "headers": dict(request.headers),
                "client_ip": request.client.host if request.client else None,
            }

            await log_async(log_data, response.status_code)

            return response

        except Exception as error:
            # Log exceptions
            error_data = {
                "trace_id": trace_id,
                "error": str(error),
                "error_type": str(type(error)),
                "traceback": traceback.format_exc(),
                "method": request.method,
                "endpoint": request.url.path,
                "processing_time": round(time.time() - start_time, 4),
            }

            await log_async(error_data, 500)

            return Response(
                status_code=500,
                content=json.dumps({"detail": ["Unexpected error occurred", f"Trace ID: {trace_id}", str(error)]}),
                media_type="application/json",
            )


async def log_async(data: dict[str, Any], status_code: int) -> None:
    if status_code >= 500:
        logger.error(data)
    elif status_code >= 400:
        logger.warning(data)
    else:
        logger.info(data)


def _log_async(func: Callable[..., None], msg: str, **kwargs: Any) -> None:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.call_soon(func, msg, **kwargs)
    else:
        func(msg, **kwargs)


# Utility functions for logging in both sync and async contexts
def log_debug(msg: str, **kwargs: Any) -> None:
    _log_async(logger.debug, msg, **kwargs)


def log_info(msg: str, **kwargs: Any) -> None:
    _log_async(logger.info, msg, **kwargs)


def log_warning(msg: str, **kwargs: Any) -> None:
    _log_async(logger.warning, msg, **kwargs)


def log_error(msg: str, **kwargs: Any) -> None:
    _log_async(logger.error, msg, **kwargs)


def log_critical(msg: str, **kwargs: Any) -> None:
    _log_async(logger.critical, msg, **kwargs)


# Initialize logger
setup_logging()
