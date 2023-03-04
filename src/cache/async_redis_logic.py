import json
import functools
import redis
import redis.asyncio as async_redis
from logger import logger


class AsyncRedisCache:
    def __init__(self, host='localhost', port=6379, db: int = 0, password: str = None, timeout: int = None):
        self.timeout = timeout
        self.pool = async_redis.ConnectionPool(host=host, port=port, db=db, password=password)

    @staticmethod
    def exception_middleware(func):
        @functools.wraps(func)
        async def wrap(*args):
            try:
                return await func(*args)
            except redis.exceptions.ConnectionError:
                logger.error("The redis connection is refused. The redis container not responding. Restart a container.")
                raise ConnectionError
        return wrap

    @exception_middleware
    async def check_key_in_async_redis(self, key: str) -> bool:
        if await self.async_redis.exists(key):
            return True
        return False

    @exception_middleware
    async def create_key_and_value(self, key: str, value: dict | str | float) -> None:
        if isinstance(value, dict):
            await self.async_redis.set(name=key, value=json.dumps(value), ex=self.timeout)
        else:
            await self.async_redis.set(name=key, value=value, ex=self.timeout)

    @exception_middleware
    async def update_exist_key(self, key: str, new_value: dict | float | str) -> None:
        if isinstance(new_value, dict):
            await self.async_redis.set(name=key, value=json.dumps(new_value), ex=self.timeout)
        else:
            await self.async_redis.set(name=key, value=new_value, ex=self.timeout)

    @exception_middleware
    async def get_value(self, key: str) -> dict:
        value = await self.async_redis.get(key)
        if value is None:
            return {}
        return json.loads(value)

    @exception_middleware
    async def __aenter__(self) -> any:
        self.async_redis = await async_redis.Redis(connection_pool=self.pool)
        return self

    @exception_middleware
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.async_redis.close()
