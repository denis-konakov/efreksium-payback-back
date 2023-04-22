from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
from enum import StrEnum, Enum
from utils import EnumGroup

class GroupRole(StrEnum):
    OWNER = 'owner'
    MODERATOR = 'moder'
    MEMBER = 'member'

_ = EnumGroup

class GroupRolePermissions(EnumGroup[GroupRole], Enum):
    ADD_MEMBER = _(GroupRole.OWNER, GroupRole.MODERATOR)
    SET_ROLE = _(GroupRole.OWNER)
    CHANGE_BALANCE = _(GroupRole.OWNER, GroupRole.MODERATOR)
    CHANGE_AVATAR = _(GroupRole.OWNER)


class GroupMemberDatabaseModel(Base):
    __tablename__ = 'group_members'
    id = q.Column(q.Integer, primary_key=True, index=True)
    user_id = q.Column(q.Integer, q.ForeignKey('users.id'))
    user = relationship('UserDatabaseModel', back_populates='member_in_groups')
    group_id = q.Column(q.Integer, q.ForeignKey('group.id'))
    group = relationship('GroupDatabaseModel', back_populates='members')
    role = q.Column(q.Enum(GroupRole), default=GroupRole.MEMBER)
    balance = q.Column(q.Integer, default=0)
