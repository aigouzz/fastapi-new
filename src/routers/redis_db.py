from fastapi import FastAPI,Request, Response, UploadFile, Query, APIRouter, Security
from time import sleep

router = APIRouter()

@router.get("/redis")
async def get_redis(request: Request):
    value = await request.app.state.redis.get("fastapi_redis")

    if value is None:
        sleep(5)
        hi = "hey redis"
        await request.app.state.redis.set(
            "fastapi_redis",
            hi,
            ex=60  # 多少秒过期
        )
        return hi
    return value