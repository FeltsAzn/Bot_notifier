import json
import redis.asyncio as async_redis


class AsyncRedisCache:
    def __init__(self, host='localhost', port=6379, db: int = 0, password: str = None, timeout: int = None):
        self.timeout = timeout
        self.pool = async_redis.ConnectionPool(host=host, port=port, db=db, password=password)

    async def check_key_in_async_redis(self, key: str) -> bool:
        if await self.async_redis.exists(key):
            return True
        return False

    async def create_key_and_value(self, key: str, value: dict | str | float) -> None:
        if isinstance(value, dict):
            await self.async_redis.set(name=key, value=json.dumps(value), ex=self.timeout)
        else:
            await self.async_redis.set(name=key, value=value, ex=self.timeout)

    async def update_exist_key(self, key: str, new_value: dict | float | str) -> None:
        if isinstance(new_value, dict):
            await self.async_redis.set(name=key, value=json.dumps(new_value), ex=self.timeout)
        else:
            await self.async_redis.set(name=key, value=new_value, ex=self.timeout)

    async def get_value(self, key: str) -> dict | float | str | None:
        value = await self.async_redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def __aenter__(self) -> any:
        self.async_redis = await async_redis.Redis(connection_pool=self.pool)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.async_redis.close()
