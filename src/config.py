from pydantic import SecretStr
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    STATIC_DIR: str = "static"
    STATIC_URL: str = "/sub"
    STATIC_NAME: str = "statics"
    TEMPLATES_DIR: str = "templates"
    Debug: bool = False
    UPLOAD_DIR: str = "files"
    REDIS_HOST: str = ''
    REDIS_PASSWORD: str= ''
    MYSQL_HOST: str = ''
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = 'root'
    MYSQL_PASSWORD: str = ''
    MYSQL_DATABASE: str = 'fast_db'
    MAIL_USERNAME: str = 'ghc245@163.com'
    MAIL_PASSWORD: SecretStr = SecretStr('')
    MAIL_FROM: str = 'ghc245@163.com'

    # token生成
    SECRET_KEY: str = ''
    ALGORITHM: str = ''
    ACCESS_TOKEN_EXPIRED_MINUTES: int = 1
    class Config:
        env_file = (".env", ".env.prod", ".env.dev")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

config = get_settings()