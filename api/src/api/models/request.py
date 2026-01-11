from typing import Any

from pydantic import BaseModel, Json


class Request(BaseModel):
    zone: str
    time: int
    fqdn: str
    protocol: str
    clientip: str
    request: Json[Any]
    response: Json[Any]
    reqsummary: str
    respsummary: str
