from fastapi import FastAPI,Request, Response, APIRouter

router = APIRouter()


@router.get("/index") # /news/index
async def index(*, request: Request, response: Response):
    return {"message": "new index"}