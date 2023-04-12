from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
from enum import StrEnum

class GroupAction(StrEnum):
    CREATE = 'create'
    PAYMENT = 'payment'
    ADD_MEMBER = 'add_member'
    REMOVE_MEMBER = 'remove_member'
    CHANGE_ROLE = 'change_role'
    CHANGE_BALANCE = 'change_balance'
    CHANGE_NAME = 'change_name'
    CHANGE_AVATAR = 'change_avatar'


class GroupHistoryDatabaseModel(Base):
    __tablename__ = 'group_history'
    id = q.Column(q.Integer,
                  primary_key=True,
                  index=True)
    group_id = q.Column(q.Integer,
                        q.ForeignKey('group.id'))
    group = relationship('GroupDatabaseModel',
                         back_populates='history')
    user_id = q.Column(q.Integer,
                       q.ForeignKey('users.id'))
    user = relationship('UserDatabaseModel',
                        foreign_keys=['group_history.user_id'],
                        back_populates='actions')
    action = q.Column(q.Enum(GroupAction),
                      default=GroupAction.PAYMENT)
    action_description = q.Column(q.JSON,
                                  nullable=False)
    time = q.Column(q.DateTime,
                    nullable=False,
                    server_default=q.func.now())
