import json
import time
from cache.redis_logic import RedisCache
import redis

cache1 = RedisCache()
cache2 = RedisCache(db=1)
timer1 = {
    "timer_5": {
        "time": str(time.time()),
        "vol": 30000
    },
    "timer_30": {
        "time": str(time.time()),
        "vol": 50000
    }
}

timer2 = {
    "timer_5": {
        "time": str(time.time()),
        "vol": 1000000
    },
    "timer_30": {
        "time": str(time.time()),
        "vol": 80000
    }
}

with cache1 as redis_session_1:
    redis_session_1.create_key_and_value("BTC/USDT|huobi", timer1)
    print(type(redis_session_1.get_value("BTC/USDT|huobi")), redis_session_1.get_value("BTC/USDT|huobi"))

with cache2 as redis_session_2:
    redis_session_2.create_key_and_value("BTC/USDT|binance", timer2)
    print(redis_session_2.check_key_in_redis("BTC/USDT|binance"))
    print(redis_session_2.check_key_in_redis("BTC/USDT|"))
    print(type(redis_session_2.get_value("BTC/USDT|binance")), redis_session_2.get_value("BTC/USDT|binance"))



host='localhost'
port=6379
db=0
pool = redis.ConnectionPool(host=host, port=port, db=db)
redis = redis.Redis(connection_pool=pool)
redis.flushall()

with cache1 as redis_session_1:
    print(type(redis_session_1.get_value("BTC/USDT|huobi")), redis_session_1.get_value("BTC/USDT|huobi"))

with cache2 as redis_session_2:
    print(type(redis_session_2.get_value("BTC/USDT|huobi")), redis_session_2.get_value("BTC/USDT|huobi"))




