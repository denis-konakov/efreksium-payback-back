from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
from enum import Enum


class GroupRole(Enum):
    OWNER = 2
    MODERATOR = 1
    MEMBER = 0


class GroupMemberDatabaseModel(Base):
    __tablename__ = 'group_members'
    id = q.Column(q.Integer, primary_key=True, index=True)
    user_id = q.Column(q.Integer, q.ForeignKey('users.id'))
    user = relationship('UserDatabaseModel', backref='groups')
    group_id = q.Column(q.Integer, q.ForeignKey('groups.id'))
    group = relationship('GroupDatabaseModel', backref='members')
    role = q.Column(q.Enum(GroupRole), default=GroupRole.MEMBER)
    balance = q.Column(q.Integer, default=0)
