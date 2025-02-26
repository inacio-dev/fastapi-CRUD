import json
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, TypeVar, cast

from fastapi import Request
from fastapi.encoders import jsonable_encoder

from app.redis import redis_client
from app.utils.logger import log_error, log_info, log_warning

# Definindo TypeVar para uso nos decoradores
R = TypeVar("R")


async def remove_cache_item(key: str) -> None:
    try:
        if "*" in key:
            # Se o padrão contém '*', busca todas as chaves correspondentes
            keys_result = await redis_client.keys(key)
            keys: list[str] = [k.decode("utf-8") if isinstance(k, bytes) else str(k) for k in keys_result]
            if keys:
                await redis_client.delete(*keys)
                log_info(f"Itens removidos do cache para o padrão: {key}")
            else:
                log_info(f"Nenhuma chave encontrada para o padrão: {key}")
        else:
            # Remove apenas a chave específica
            result = await redis_client.delete(key)
            if result:
                log_info(f"Item removido do cache: {key}")
            else:
                log_info(f"Item não encontrado no cache: {key}")
    except Exception as e:
        log_error(f"Erro ao remover item do cache {key}: {e!s}")


async def remove_related_cache(path: str) -> None:
    try:
        pattern = f"cache:{path}*"
        keys_result = await redis_client.keys(pattern)
        keys: list[str] = [k.decode("utf-8") if isinstance(k, bytes) else str(k) for k in keys_result]
        if keys:
            await redis_client.delete(*keys)
            log_info(f"Cache removido para o padrão: {pattern}")
    except Exception as e:
        log_error(f"Erro ao remover cache para {path}: {e!s}")


def custom_cache(expire: int = 60) -> Callable[[Callable[..., Awaitable[R]]], Callable[..., Awaitable[R]]]:
    def decorator(func: Callable[..., Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> R:
            request = kwargs.get("request") or next((arg for arg in args if isinstance(arg, Request)), None)
            if not request or not isinstance(request, Request):
                log_warning(f"Request válido não encontrado para {func.__name__}. Cache desativado.")
                return await func(*args, **kwargs)

            # Para métodos de modificação, remover o cache relacionado e executar a função
            if request.method in ["POST", "PATCH", "PUT", "DELETE"]:
                await remove_related_cache(request.url.path)
                return await func(*args, **kwargs)

            # Gerar uma chave base única para a rota
            base_key = f"cache:{request.url.path}"

            # Gerar chaves separadas para cada parâmetro
            param_keys = []
            for key, value in request.query_params.items():
                param_keys.append(f"{key}:{value}")

            # Combinar a chave base com as chaves de parâmetros
            cache_key = f"{base_key}:{':'.join(sorted(param_keys))}"

            try:
                # Verificar se o resultado está no cache de forma assíncrona
                cached_result = await redis_client.get(cache_key)
                if cached_result:
                    log_info(f"Cache hit para {cache_key}")
                    return cast(R, json.loads(cached_result))

                log_info(f"Cache miss para {cache_key}")

                # Se não estiver no cache, executar a função
                result = await func(*args, **kwargs)

                # Serializar o resultado antes de armazenar no cache
                serialized_result = jsonable_encoder(result)

                # Armazenar o resultado serializado no cache de forma assíncrona
                await redis_client.setex(cache_key, expire, json.dumps(serialized_result))
                log_info(f"Resultado armazenado no cache para {cache_key}")

                return result

            except json.JSONDecodeError:
                log_error(f"Erro ao decodificar JSON do cache para {cache_key}")
                return await func(*args, **kwargs)
            except Exception as e:
                log_error(f"Erro no cache para {cache_key}: {e!s}")
                return await func(*args, **kwargs)

        return wrapper

    return decorator
