import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
# 配置redis连接池
redis_pool = redis.ConnectionPool(
    host='127.0.0.1',
    password=REDIS_PASSWORD,
    port=6379,
    decode_responses=True, # redis默认返回字节码
    encoding="utf-8"
)

async def redis_connect():
    try:
        redis_client = redis.Redis(connection_pool=redis_pool)
        sig = redis_client.ping()
        print(sig, 'redis 链接正确')
        return redis_client
    except ConnectionError as conecp:
        print('redis 连接出错，', conecp)
    except TimeoutError:
        print('redis 连接超时')
    except Exception as excp:
        print("redis 链接异常，", excp)




