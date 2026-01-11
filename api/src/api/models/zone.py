from datetime import datetime
from typing import List, Optional

from models.auth import AuthzBase
from pydantic import BaseModel


class ZoneBase(BaseModel):
    fqdn: str
    domain: str
    expiry: datetime | None
    authz: List[AuthzBase]


class ZoneCreate(BaseModel):
    domain: Optional[str] = ""
    num: Optional[int] = 1
    zone: Optional[str] = ""


class Zone(BaseModel):
    fqdn: str
    domain: str


class ZoneRecord(BaseModel):
    name: str
    type: str
    content: str
    ttl: int
    priority: Optional[int] = None
