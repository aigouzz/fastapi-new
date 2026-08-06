"""
定义请求和响应模型

"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer

class AccountCreate(BaseModel):
    username: str = Field(min_length=4, max_length=32)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class AccountLogin(BaseModel):
    username: str = Field(min_length=4, max_length=32)
    password: str = Field(min_length=6, max_length=128)

class AccountUpdate(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=4,
        max_length=32
    )
    email: EmailStr | None = None
    status: int = Field(ge=0, le=5)

class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    status: int
    create_time: datetime
    update_time: datetime

    @field_serializer("create_time", "update_time")
    def serialize_datetime(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
