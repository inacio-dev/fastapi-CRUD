import os

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from app.core.database.async_db import get_async_db
from app.utils.cache import remove_cache_item

POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")


async def set_example_task():
    try:
        async for session in get_async_db():
            # Configurar search_path se necessário
            await session.execute(text(f"SET search_path TO '{POSTGRES_SCHEMA}'"))

            # Limpar cache relacionado
            await remove_cache_item("cache:/api/v1/example*")

            return "Exemples processed successfully"

    except SQLAlchemyError as e:
        raise e
    except Exception as e:
        raise e
