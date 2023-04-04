from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
from enum import StrEnum


class GroupRole(StrEnum):
    OWNER = 'owner'
    MODERATOR = 'moder'
    MEMBER = 'member'


class GroupMemberDatabaseModel(Base):
    __tablename__ = 'group_members'
    id = q.Column(q.Integer, primary_key=True, index=True)
    user_id = q.Column(q.Integer, q.ForeignKey('users.id'))
    user = relationship('UserDatabaseModel', back_populates='groups')
    group_id = q.Column(q.Integer, q.ForeignKey('groups.id'))
    group = relationship('GroupDatabaseModel', back_populates='members')
    role = q.Column(q.Enum(GroupRole), default=GroupRole.MEMBER)
    balance = q.Column(q.Integer, default=0)
