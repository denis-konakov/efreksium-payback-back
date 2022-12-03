from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
from enum import Enum

class Action(Enum):
    PAYMENT = 0
    ADD_MEMBER = 1
    REMOVE_MEMBER = 2
    CHANGE_ROLE = 3
    CHANGE_BALANCE = 4
    CHANGE_NAME = 5
    CHANGE_AVATAR = 6


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
