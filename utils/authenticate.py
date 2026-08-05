from fastapi.security import APIKeyHeader
from typing import Annotated
from fastapi import Security,HTTPException, status

authentication_header = APIKeyHeader(
    name="Authentication",
    scheme_name="Authentication",
    description="请输入访问令牌",
    auto_error=False,
)


async def check_authentication(
    token: Annotated[
        str | None,
        Security(authentication_header),
    ],
):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return token