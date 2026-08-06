# from contextlib import asynccontextmanager

# from fastapi import FastAPI
# from tortoise.contrib.fastapi import RegisterTortoise
# from tortoise import connections

# from config import config

# MYSQL_HOST = config.MYSQL_HOST
# MYSQL_PORT = config.MYSQL_PORT
# MYSQL_USER = config.MYSQL_USER
# MYSQL_PASSWORD = config.MYSQL_PASSWORD
# MYSQL_DATABASE = config.MYSQL_DATABASE


# TORTOISE_MODELS = [
#     'models.model',
# ]

# TORTOISE_CONFIG = {
#     "connections": {
#         "default": {
#             "engine": "tortoise.backends.mysql",
#             "credentials": {
#                 "host": MYSQL_HOST,
#                 "port": MYSQL_PORT,
#                 "user": MYSQL_USER,
#                 "password": MYSQL_PASSWORD,
#                 "database": MYSQL_DATABASE,
#             }
#         }
#     },
#     "apps": {
#         "tai_models": {
#             "models": TORTOISE_MODELS,
#             "default_connection": 'default'        
#         }
#     },
#     "use_tz": False, # 不使用默认时区
#     "timezone": "Asia/Shanghai",
# }

# @asynccontextmanager
# async def register_mysql(app: FastAPI):
#     try:
#         async with RegisterTortoise(
#             app,
#             config=TORTOISE_CONFIG,
#             generate_schemas=False, # 是否在建立连接时候根据数据模型类来表数据表
#         ):
#             print("mysql 数据库连接成功")
#             yield 
#             await connections.close_all()
#             print("mysql 数据库连接已经关闭")
#     except Exception as excp:
#         print(excp)
from ..config import config
from sqlalchemy import URL,create_engine,text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

MYSQL_HOST = config.MYSQL_HOST
MYSQL_PORT = config.MYSQL_PORT
MYSQL_USER = config.MYSQL_USER
MYSQL_PASSWORD = config.MYSQL_PASSWORD
MYSQL_DATABASE = config.MYSQL_DATABASE

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database='fast_db',
)

engine = create_engine(
    DATABASE_URL,
    echo=False,  # 是否展示数据库连接log
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as session:
        yield session

def check_database_connection() -> None:
    with SessionLocal() as session:
        result = session.scalar(text("SELECT 1"))
        if result != 1:
            raise RuntimeError("数据库连接测试异常")