import json
import asyncio

from functools import wraps
from fastapi import Request
from fastapi.encoders import jsonable_encoder

from app.utils.logger import log_info, log_error, log_warning
from app.redis import redis_client


async def remove_cache_item(key: str):
    try:
        if "*" in key:
            # Se o padrão contém '*', busca todas as chaves correspondentes
            keys = await asyncio.to_thread(redis_client.keys, key)
            if keys:
                await asyncio.to_thread(redis_client.delete, *keys)
                log_info({"message": f"Itens removidos do cache para o padrão: {key}", "cache_key": key})
            else:
                log_info({"message": f"Nenhuma chave encontrada para o padrão: {key}", "cache_key": key})
        else:
            # Remove apenas a chave específica
            result = await asyncio.to_thread(redis_client.delete, key)
            if result:
                log_info({"message": f"Item removido do cache: {key}", "cache_key": key})
            else:
                log_info({"message": f"Item não encontrado no cache: {key}", "cache_key": key})
    except Exception as e:
        log_error({"message": f"Erro ao remover item do cache {key}", "error": str(e), "cache_key": key})


async def remove_related_cache(path: str):
    try:
        pattern = f"cache:{path}*"
        keys = await asyncio.to_thread(redis_client.keys, pattern)
        if keys:
            await asyncio.to_thread(redis_client.delete, *keys)
            log_info({"message": f"Cache removido para o padrão: {pattern}", "pattern": pattern})
    except Exception as e:
        log_error({"message": f"Erro ao remover cache para {path}", "error": str(e), "path": path})


def custom_cache(expire: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request") or next((arg for arg in args if isinstance(arg, Request)), None)
            if not request or not isinstance(request, Request):
                log_warning(
                    {
                        "message": f"Request válido não encontrado para {func.__name__}. Cache desativado.",
                        "function": func.__name__,
                    }
                )
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
                cached_result = await asyncio.to_thread(redis_client.get, cache_key)
                if cached_result:
                    log_info({"message": f"Cache hit para {cache_key}", "cache_key": cache_key, "cache_status": "hit"})
                    return json.loads(cached_result)

                log_info({"message": f"Cache miss para {cache_key}", "cache_key": cache_key, "cache_status": "miss"})

                # Se não estiver no cache, executar a função
                result = await func(*args, **kwargs)

                # Serializar o resultado antes de armazenar no cache
                serialized_result = jsonable_encoder(result)

                # Armazenar o resultado serializado no cache de forma assíncrona
                await asyncio.to_thread(redis_client.setex, cache_key, expire, json.dumps(serialized_result))
                log_info(
                    {
                        "message": f"Resultado armazenado no cache para {cache_key}",
                        "cache_key": cache_key,
                        "expire": expire,
                    }
                )

                return result

            except json.JSONDecodeError:
                log_error(
                    {
                        "message": f"Erro ao decodificar JSON do cache para {cache_key}",
                        "cache_key": cache_key,
                        "error_type": "JSONDecodeError",
                    }
                )
                return await func(*args, **kwargs)
            except Exception as e:
                log_error(
                    {
                        "message": f"Erro no cache para {cache_key}",
                        "cache_key": cache_key,
                        "error": str(e),
                        "error_type": type(e).__name__,
                    }
                )
                return await func(*args, **kwargs)

        return wrapper

    return decorator
