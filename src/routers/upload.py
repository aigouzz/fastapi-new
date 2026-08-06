from fastapi import FastAPI,Request, Response, UploadFile, Query, APIRouter, Security
from fastapi.staticfiles import StaticFiles
import sys,time,hashlib,os,uuid
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from ..config import config
# from utils.fakeDB import file_db
from ..utils.admin import check_user
from typing import Annotated

router = APIRouter()

jinja2_templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

def unique_generator(*, length=6):
    unique_name = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:length]
    return unique_name

# @router.post("/upload_file", summary="Upload a file", dependencies=[Security(check_user, scopes=['upload'])])
# async def upload_file(file: UploadFile, request: Request, response: Response): # path_var: str | None = None, code: str | None = Query(default=None, description="Optional code parameter")
#     file_local = await save_file(file)
#     file_db.create_file(file_local, file.filename if file.filename else "")
#     share_code = unique_generator(length=6)
#     file_db.create_share_code(file_local, share_code)
#     print(file_local, file.filename, share_code)
#     return {
#         "filename": file.filename,
#         "file_local": file_local,
#         "code": share_code,
#         "url": request.url_for("file_page", file_local=file_local).path
#     }

# async def save_file(file):
#     if not os.path.exists(config.UPLOAD_DIR):
#         os.mkdir(config.UPLOAD_DIR)
#     res = await file.read()
#     hash_name = hashlib.md5(file.filename.encode()).hexdigest()
#     filename = f"{hash_name}.{file.filename.rsplit('.', 1)[-1]}"
#     fullfile = f"{config.UPLOAD_DIR}/{filename}"
#     with open(fullfile, 'wb') as fw:
#         fw.write(res)
#     return filename

# @router.get("/share", summary="全部下载页面", dependencies=[Security(check_user, scopes=['visit'])])
# async def share_page(request: Request):
#     files = file_db.get_all_files()
#     data = {
#         "all_files": files,
#     }
#     return jinja2_templates.TemplateResponse(name="share.html", request=request, context=data)

# @router.get("/file/{file_local}", summary="文件下载页面", name="file_page", dependencies=[Security(check_user, scopes=['visit', 'download'])])
# async def file_page(request: Request, file_local: str, share_code: str | None = Query(default=None, min_length=6)):
#     file_name = file_db.get_file(file_local)
#     if not file_name:
#         return JSONResponse(content={"message": "File not found"}, status_code=404)
    
#     code = file_db.get_share_code(file_local)
#     if share_code and share_code != code:
#         return JSONResponse(content={"message": "Invalid share code"}, status_code=403)

#     data = {
#         "file_name": file_name,
#         "file_local": file_local,
#         "share_code": share_code,
#     }

#     return jinja2_templates.TemplateResponse(name="file.html", request=request, context=data)

# @router.post("/download_file/{file_local}", summary="下载文件", name="download_file", dependencies=[Security(check_user, scopes=['download'])])
# async def download_file(file_local: str, share_code: str | None = Query(default=None)):
#     file_name = file_db.get_file(file_local)
#     if not file_name:
#         return JSONResponse(content={"message": "File not found"}, status_code=404)
    
#     code = file_db.get_share_code(file_local)
#     if share_code and share_code != code:
#         return JSONResponse(content={"message": "Invalid share code"}, status_code=403)
#     filepath = config.UPLOAD_DIR + '/' + file_local
#     return FileResponse(path=filepath, filename=file_name, media_type="application/octet-stream")