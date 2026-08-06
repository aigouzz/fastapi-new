from collections import defaultdict
import time
from typing import Any, Callable
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
import logging

from starlette.responses import Response
from starlette.types import ASGIApp

# logger = logging.getLogger("uvicorn.access")
# logger.disabled = True

def my_logger(message: str):
    print(message)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.request_records: dict[str, float] = defaultdict(float)
    async def dispatch(self, request: Request, call_next):
        if request.client is not None:
            ip = request.client.host
        else:
            ip = "none"
        current_time = time.time()
        if current_time - self.request_records[ip] < 5:
            return Response(content='超过访问限制', status_code=429)
        response = await call_next(request)
        self.request_records[ip] = current_time
        return response

def tai_middleware(app: FastAPI):

    @app.middleware("http")
    async def count_time(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        response_time = time.time() -start_time
        print(f"{response_time}s")
        return response
    @app.middleware("http")
    async def tai_logging(request: Request, call_next):
        if request.client is not None:
            message = f"{request.client.host}:{request.client.port} {request.method} {request.url.path}"
        else:
            message = f"{request.method} {request.url.path}"
        my_logger(message)
        response = await call_next(request)

        return response
    
    # app.add_middleware(RateLimitMiddleware)
    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_credentials=False,
                       allow_methods=['*'],
                       allow_headers=['*'])








# @app.middleware("http")
# async def only_for_request(request: Request, call_next):
#     print('获取到请求', request.url)
#     response = await call_next(request)
#     return response

# @app.middleware("http")
# async def only_for_response(request: Request, call_next):
#     response = await call_next(request)
#     print('获取到响应结果：', response.headers)
#     return response