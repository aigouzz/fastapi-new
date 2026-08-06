from fastapi import APIRouter, Request, HTTPException, Response, status, Depends
from pydantic import BaseModel, Field
from .model import Account
from pwdlib import PasswordHash
from starlette.concurrency import run_in_threadpool
from .schemas import AccountCreate, AccountUpdate, AccountResponse, AccountLogin
from ..database.db_mysql import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select,or_
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

password_hash = PasswordHash.recommended()

def get_password_hash(password:str):
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


@router.post("/signup")
async def signup(request: Request, account: AccountCreate, db: Session = Depends(get_db)):
    statement = select(Account).where(
        or_(
            Account.username == account.username,
            Account.email == account.email
        )
    )
    existing_account = db.scalar(statement=statement)
    if existing_account:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户名或者邮箱已经存在")
    hashed_password = await run_in_threadpool(get_password_hash, account.password)
    try:
        now_account = Account(
            username=account.username,
            email=account.email,
            hashed_password=hashed_password
        )
        db.add(now_account)
        db.commit()
        db.refresh(now_account)
        return Response(status_code=status.HTTP_200_OK, content="用户创建成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=AccountResponse)
async def login(account: AccountLogin, db: Session = Depends(get_db)):
    username = account.username.strip()
    statement = select(Account).where(Account.username == account.username)
    # statement1 = select(Account).where(Account.email == account.email)
    existing_account = db.scalar(statement=statement)
    if not existing_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')
    if not verify_password(account.password, existing_account.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="密码错误")
    return existing_account