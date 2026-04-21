from fastapi import Depends
from typing import Any, Callable
from functools import wraps
from pickle import dumps, loads

import redis.asyncio as redis
from src.config import config


redis_client = redis.from_url(url=config.REDIS_URL)


class ObjectCacheHandler:
    @staticmethod
    async def get(key: str) -> Any:
        cached_bytes = await redis_client.get(name=key)
        if cached_bytes:
            return loads(cached_bytes)
    
    @staticmethod
    async def set(
        key: str, value: Any, 
        ttl: int = config.REDIS_TIME_TO_LIVE_SECONDS
    ) -> None:
        await redis_client.set(
            name=key, 
            value=dumps(value), 
            ex=ttl
        )


def CacheDecoratorFactory(ttl: int = config.REDIS_TIME_TO_LIVE_SECONDS):
    def cache_decoraror(function: Callable):
    
        @wraps(function)
        async def decorated_function(*args, **kwargs):
            if not (cache_object_id:=kwargs.get("order_uuid")):
                raise ValueError("Caching is not supported for this function")
            
            cache_object_key = f"{function.__name__ }:{cache_object_id}"
            cached_order = await ObjectCacheHandler.get(
                key = cache_object_key
            )
            if cached_order:
                return cached_order
            
            call_results = await function(*args, **kwargs)
            
            await ObjectCacheHandler.set(
                key=cache_object_key, 
                value=call_results, 
                ttl=ttl
            )
            return call_results
    
        return decorated_function
    return cache_decoraror





























