import os

from fastapi import FastAPI
from redis.asyncio import Redis

# Criando um cliente Redis assíncrono
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", 6379)), db=0, decode_responses=True
)


def setup_redis_cache(app: FastAPI) -> None:
    app.state.redis = redis_client
