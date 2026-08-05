from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig, NameEmail
from config import config
from fastapi import APIRouter, HTTPException,status,BackgroundTasks
from constants import SEND_EMAIL_TO
import time
import logging

router = APIRouter()

yahoo_mail_config = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_SERVER='smtp.163.com',
    MAIL_PORT=465,       # 服务器端口
    MAIL_SSL_TLS=True,    # 用于465端口
    MAIL_STARTTLS=False,  # 用于587端口
    USE_CREDENTIALS=True,   # 使用凭证
    VALIDATE_CERTS=True,   # 证书验证， 在虚拟开发环境中会提示验证有误，
)

class Email(BaseModel):
    address: list[NameEmail]  # 类型是list 方便给多个地址发邮件，emailstr是pydantic的邮件格式校验

@router.post("/send_email")
async def send_email(email: Email, background_tasks: BackgroundTasks):
    start_time = time.time()

    body_html = """
    <h1>这是fastapi发送的邮件</h1>    
    <p>当你看到时标识发送邮件成功</p>
    """

    message = MessageSchema(
        subject="Fastapi 邮件",
        recipients=[address for address in email.address],
        body=body_html,
        subtype=MessageType.html,
    )
    try:
        fm = FastMail(yahoo_mail_config)
        # await fm.send_message(message=message)
        background_tasks.add_task(fm.send_message, message=message)
    except Exception as e:
        logging.getLogger(__name__).exception('邮件发送失败，' + str(e))
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='发送邮件失败')
        

    return {
        "address": email.address,
        "发送邮件所用时间": time.time() - start_time,
    }