from enum import IntEnum

from pydantic import BaseModel


class Permission(IntEnum):
    NOPERMISSION = -999
    READONLY = 0
    READWRITE = 10
    ASSIGNROLES = 20
    OWNER = 999
    ADMIN = 10000


class AuthzBase(BaseModel):
    alias: str
    authzlevel: int  # IntEnum?


class AuthzPermission(AuthzBase):
    pass


class PermissionRequest(BaseModel):
    alias: str
    permission: str
    # permission: Permission


class PermissionCreate(BaseModel):
    zone: str
    user: str
    permission: Permission


class PermissionUpdate(BaseModel):
    permission: Permission


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
