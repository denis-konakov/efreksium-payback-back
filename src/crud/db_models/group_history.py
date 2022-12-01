from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
from enum import Enum

class Action(Enum):
    PAYMENT: int
    ADD_MEMBER: int
    REMOVE_MEMBER: int
    CHANGE_ROLE: int
    CHANGE_BALANCE: int
    CHANGE_NAME: int
    CHANGE_AVATAR: int


class GroupHistoryDatabaseModel(Base):
    __tablename__ = 'group_history'
    id = q.Column(q.Integer, primary_key=True, index=True)
    group_id = q.Column(q.Integer, q.ForeignKey('groups.id'))
    group = relationship('GroupDatabaseModel', backref='history')
    user_id = q.Column(q.Integer, q.ForeignKey('users.id'))
    user = relationship('UserDatabaseModel', backref='group_history')
    action = q.Column(q.Enum(Action), default=Action.PAYMENT)
    action_description = q.Column(q.JSON, nullable=False)
    time = q.Column(q.DateTime, nullable=False, server_default=q.func.now())
