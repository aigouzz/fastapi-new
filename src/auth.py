import jwt
from datetime import datetime,timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import config

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRED_MINUTES = config.ACCESS_TOKEN_EXPIRED_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def create_user_token(data: dict):
    to_encode = data.copy()
    print(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRED_MINUTES)
    to_encode.update({
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRED_MINUTES)
    })
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

def get_user_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 已经过期",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token无效',
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


