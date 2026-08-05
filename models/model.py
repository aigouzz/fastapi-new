# from tortoise import fields 
# from tortoise.models import Model

# class User(Model):
#     id = fields.IntField(primary_key=True, )
#     username = fields.CharField(max_length=50, unique=True)
#     password = fields.CharField(max_length=255)
#     created_at = fields.DatetimeField(auto_now_add=True)

#     class Meta:
#         table = "users"

# class Account(Model):
#     id = fields.IntField(primary_key=True, generated=True)
#     username = fields.CharField(null=False, unique=True, min_length=4, max_length=32, description="用户名")
#     email = fields.CharField(null=False, unique=True, min_length=6, max_length=64, description="电子邮件")
#     hashed_password = fields.CharField(null=False,min_length=6, max_length=256, description="加密后的用户密码")
#     status = fields.SmallIntField(null=False, default=0, description="0-未激活 1-已经激活 5-锁定")
#     create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
#     update_time = fields.DatetimeField(auto_now=True, description="更新时间")


#     class Meta:
#         table_description="Account账户信息表"
#         table = 'account'
from datetime import datetime
from sqlalchemy import DateTime,SmallInteger, String, func, text
from sqlalchemy.orm import Mapped, mapped_column
from database.db_mysql import Base

class Account(Base):
    __tablename__ = 'account'
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    username:Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
        comment='用户名'
    )
    email:Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
        comment='电子邮件'
    )
    hashed_password: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        comment='加密后密码'
    )
    status: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
        server_default=text("0"),
        comment='0-未激活 1-已经激活 5-锁定'
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment='创建时间'
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间'
    )

