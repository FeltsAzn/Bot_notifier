import json
import redis


class RedisCache:
    def __init__(self, host='localhost', port=6379, db: int= 0, password: str = None, timeout: int = None):
        self.timeout = timeout
        self.pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)

    def check_key_in_redis(self, key: str) -> bool:
        if self.redis.exists(key):
            return True
        return False

    def create_key_and_value(self, key: str, value: dict | str | float) -> None:
        if isinstance(value, dict):
                self.redis.set(name=key, value=json.dumps(value), ex=self.timeout)
        else:
            self.redis.set(name=key, value=value, ex=self.timeout)

    def update_exist_key(self, key: str, new_value: dict | float | str) -> None:
        if isinstance(new_value, dict):
            self.redis.set(name=key, value=json.dumps(new_value), ex=self.timeout)
        else:
            self.redis.set(name=key, value=new_value, ex=self.timeout)

    def get_value(self, key: str) -> dict | float | str | None:
        value = self.redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    def __enter__(self) -> any:
        self.redis = redis.Redis(connection_pool=self.pool)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.redis.close()