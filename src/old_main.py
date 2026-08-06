# uvicorn main:app --port 8000 --reload
from fastapi import FastAPI,Request, Response
from fastapi import __version__ as fastapi_version
from fastapi.staticfiles import StaticFiles
import sys,time
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from config import config
from functools import lru_cache


app = FastAPI(
    debug=config.Debug,
)
app.mount(config.STATIC_URL, StaticFiles(directory=config.STATIC_DIR), name=config.STATIC_NAME)
# app.mount("/news", news_app)
jinja2_templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

@app.get("/")
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

@app.get("/file/{video_id}")
async def play(video_id):
    return FileResponse(f"static/video/{video_id}.mp4", media_type="video/mp4")

@app.get("/video_function")
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


@app.get("/post_v3", response_class=HTMLResponse)
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

# @lru_cache(maxsize=2)
# def get_lru_cache_data(change):
#     print("get_lru_cache_data called")
#     time.sleep(3)
#     data = {
#         "video_id": change
#     }
#     return {"data": data}

# @app.get("/lru_cache_test/{change}")
# async def lru_cache_test(change: str):
#     data = get_lru_cache_data(change)
#     print(data, 'lru cache data')
#     print(get_lru_cache_data.cache_info())
#     return {"message": "Hello from LRU cache"}