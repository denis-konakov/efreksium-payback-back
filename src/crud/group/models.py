from pydantic import BaseModel
from datetime import datetime
from ..db_models.group_member import GroupRole
from ..db_models.group_history import GroupAction


class Group(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GroupMember(BaseModel):
    id: int
    user_id: int
    user: 'UserPublic'
    group_id: int
    group: Group
    role: GroupRole
    balance: int

    class Config:
        orm_mode = True


class GroupHistoryEntry(BaseModel):
    id: int
    group_id: int
    group: Group
    user_id: int
    user: 'UserPublic'
    action: GroupAction
    action_description: dict[str, str]
    time: datetime


class ChangeBalanceEvent(BaseModel):
    user_id: int
    value: int
    time: datetime

class GroupBalanceUpdate(BaseModel):
    user_id: int
    group_id: int
    events: list[ChangeBalanceEvent]



