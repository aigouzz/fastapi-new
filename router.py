from fastapi import APIRouter
from routers.news import router as news_router
from routers.upload import router as upload_router
from routers.redis_db import router as database_router
from models.router import router as models_router
from utils.email import router as email_router
from utils.websocket import router as websocket_router

all_routers = APIRouter()
all_routers.include_router(news_router, prefix="/news")
all_routers.include_router(upload_router, prefix="/upload")
all_routers.include_router(database_router, prefix="/database")
all_routers.include_router(models_router, prefix="/account", tags=["用户注册"])
all_routers.include_router(email_router, prefix="/email", tags=["发送邮件"])
all_routers.include_router(websocket_router, prefix="/websocket", tags=["websocket链接"])