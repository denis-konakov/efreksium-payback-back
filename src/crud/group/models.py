from pydantic import BaseModel
from datetime import datetime
from ..db_models.group_member import GroupRole
from ..db_models.group_history import Action
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
    action: Action
    action_description: dict[str, str]
    time: datetime
