from enum import Enum
from fastapi import FastAPI, HTTPException,Request, Response, UploadFile, Query, Security, Depends, Cookie, status
from fastapi import __version__ as fastapi_version
from fastapi.staticfiles import StaticFiles
import sys,time,hashlib,logging
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from .config import config
from functools import lru_cache
from .router import all_routers
from .utils.admin import check_user
from .auth import create_user_token, get_user_token
from .middleware.middle import tai_middleware
from contextlib import asynccontextmanager
from .database.db_redis import redis_connect
from .database.db_mysql import check_database_connection,engine
from starlette.concurrency import run_in_threadpool
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

@asynccontextmanager
async def tai_init(app: FastAPI):
    # 启动会执行事件
    # logger_init()  日志启动服务
    # db_init()  连接数据库
    # db_settings()  获取动态配置
    # service_init()  启动第三方的服务
    # send_email()  发送email给服务者
    app.state.redis = await redis_connect()
    try:
        await run_in_threadpool(check_database_connection)
        logger.info("Mysql 数据库连接成功")
        print('mysql 数据库连接成功')
    except SQLAlchemyError as exce:
        logger.exception("mysql 数据库连接失败，错误", str(exce))
        raise RuntimeError("Fastapi启动失败：无法连接mysql")

    try:
        yield
    finally:
        await run_in_threadpool(engine.dispose)
        logger.info("SQLAlchemy 连接池已经关闭")

    # logger()  记录关闭日志
    # db_close() 关闭链接
    # service_close()  关闭第三方
    # send_email()  发送邮件通知
    assert app.state.redis is not None
    await app.state.redis.aclose()
    print('tai关闭器')

app = FastAPI(
    debug=config.Debug,
    lifespan=tai_init
)
app.mount(config.STATIC_URL, StaticFiles(directory=config.STATIC_DIR), name=config.STATIC_NAME)
app.include_router(all_routers)
jinja2_templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

tai_middleware(app)



@app.get("/") # dependencies=[Security(check_user, scopes=['visit'])]
async def index():
    return {"message": "Hello 改变"}

@app.get("/resources/path/{file}")
@app.post("/resources/path/{file}")
@app.put("/resources/path/{file}")
@app.delete("/resources/path/{file}")
async def http_url(*, request: Request):
    response = {
        "method": request.method,
        "scheme": request.url.scheme, # 协议名称
        "host": request.url.hostname, # 主机名
        "port": request.url.port, # 端口号
        "path": request.url.path, # 路径
        "query": request.url.query, # 查询字符串
        "headers": dict(request.headers),
        "body": await request.body()
    }
    print(response,)
    return response

@app.get("/file/{video_id}", dependencies=[Security(check_user, scopes=['visit'])])
async def play(video_id):
    return FileResponse(f"static/video/{video_id}.mp4", media_type="video/mp4")

@app.get("/video_function", dependencies=[Security(check_user, scopes=['visit'])])
async def video_function(*, request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    

@app.get("/server_status", include_in_schema=False)
async def server_status(*, request: Request, response: Response, token: str | None = None):
    if token == 'Tai':
        return {"status": "运行正常",
                "fastapi_version": fastapi_version,
                "python_version": f"{sys.version_info}"
                }
    else:
        response.status_code = 404
        return {"message": "404 not found"}


@app.get("/post_v3", response_class=HTMLResponse, dependencies=[Security(check_user, scopes=['visit'])])
async def post_v3(*, request: Request, response: Response):
    data = {
        "name": 'fastapi 开发部署',
        "title": '这是文章标题',
        "fastapi_version": fastapi_version,
        "python_version": f"{sys.version_info}",
        "id": 1
    }
    return jinja2_templates.TemplateResponse(name="index.html", context=data, request=request)
    # return html_maker(context=data, request=request)

class TypeName(str, Enum):
    blog = "blog"
    comment = "comment"
    page = "page"

@app.get("/post_v4/{type_name}", dependencies=[Security(check_user, scopes=['visit'])])
async def post_v4(*, request: Request, response: Response, type_name: TypeName):
    data = None
    if type_name == TypeName.blog:
        data = '<h1>Blog Posts</h1>'
    elif type_name == TypeName.comment:
        data = '<h1>Comments</h1>'
    elif type_name == TypeName.page:
        data = '<h1>Pages</h1>'
    # return HTMLResponse(content=data, status_code=200)
    return {"data": data}

@app.get("/post_v5/{file_path:path}", dependencies=[Security(check_user, scopes=['visit'])])
async def post_v5(*, request: Request, response: Response, file_path: str):
    return {"file_path": file_path}

@app.get("/login")
async def login(*, request: Request, response: Response, user_name: str | None = None):
    response.set_cookie('user_name', user_name if user_name else '', expires=600)
    return {"data": "200"}

@app.get("/send_token")
async def send_token(request: Request):
    data = {
        "user_name": "jack"
    }
    tokens = create_user_token(data)
    return tokens

@app.get("/get_token", dependencies=[Security(check_user, scopes=['visit'])])
async def get_token(request: Request):
    print(request.headers)
    return {'data': 'ok'}
