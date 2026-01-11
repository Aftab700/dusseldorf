from typing import List, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, Json


class ComponentBase(BaseModel):
    ispredicate: bool
    actionname: str
    actionvalue: Union[str, Json]
    # actionvalue: str


class ComponentAction(BaseModel):
    actionvalue: str


class ComponentCreate(ComponentBase):
    pass


class RuleComponent(ComponentBase):
    componentid: UUID = Field(default_factory=uuid4)


class RuleBase(BaseModel):
    priority: int


class RulePriority(RuleBase):
    pass


class RuleCreate(RuleBase):
    zone: str
    name: str
    networkprotocol: str


class Rule(RuleCreate):
    ruleid: UUID = Field(default_factory=uuid4)
    rulecomponents: List[RuleComponent]  # | None
