from pydantic import BaseModel
from datetime import datetime
from ..db_models.group_member import GroupRole
from ..db_models.group_history import GroupAction


class Group(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class GroupMemberShared(BaseModel):
    id: int
    user_id: int
    user: 'UserShared'
    role: GroupRole
    balance: int

    class Config:
        orm_mode = True

class GroupMember(GroupMemberShared):
    group_id: int
    group: Group

    class Config:
        orm_mode = True



class GroupHistoryEntry(BaseModel):
    id: int
    user_id: int
    user: 'UserShared'
    action: GroupAction
    action_description: dict[str, str]
    time: datetime

    class Config:
        orm_mode = True


class GroupWithHistory(Group):
    history: list[GroupHistoryEntry]

    class Config:
        orm_mode = True

class GroupFull(GroupWithHistory):
    members: list[GroupMemberShared]

    class Config:
        orm_mode = True


class ChangeBalanceEvent(BaseModel):
    user_id: int
    value: int
    time: datetime


class GroupBalanceUpdate(BaseModel):
    user_id: int
    group_id: int
    events: list[ChangeBalanceEvent]
