from fastapi import Cookie, HTTPException, status, Depends
from fastapi.security import SecurityScopes
from ..auth import get_user_token as get_token

ALL_USERS = {
    'jack': ['admin', 'users'],
    'rose': ['admin', 'users'],
    'tom': ['users'],
    'jerry': ['users'],
}

ROLE_PERMISSIONS = {
    'admin': ['upload', 'download'],
    'users': ['visit']
}

def get_user_token(token=Depends(get_token)):
    user_name = token['user_name']
    if user_name is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user_name is required")
    return user_name

# def get_user_permissons(token: str = Depends(get_user_token)):
#     if token == 'Tai_admin':
#         return 'admin'
#     elif token == 'Tai_user':
#         return 'users'

def get_role_permissons(role_name: list[str]):
    permissions = []
    for role in role_name:
        for perm in ROLE_PERMISSIONS[role]:
            permissions.append(perm)
    return permissions

def get_user_permissions(token: str = Depends(get_user_token)):
    if token in ALL_USERS:
        return get_role_permissons(ALL_USERS[token])
    return None

def check_user(security_scopes: SecurityScopes, user_permission: str = Depends(get_user_permissions)):
    for scope in security_scopes.scopes:
        if scope not in user_permission:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="您没有权限执行该操作")