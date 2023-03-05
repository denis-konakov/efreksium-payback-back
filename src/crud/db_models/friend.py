from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
from .user import UserDatabaseModel
class FriendDatabaseModel(Base):
    __tablename__ = 'friends'
    id = q.Column(q.Integer, primary_key=True, index=True)
    sender_id = q.Column(q.Integer, q.ForeignKey('users.id'))
    recipient_id = q.Column(q.Integer, q.ForeignKey('users.id'))
    sender = relationship('UserDatabaseModel', foreign_keys=[sender_id])
    recipient = relationship('UserDatabaseModel', foreign_keys=[recipient_id])
    status = q.Column(q.Boolean, default=False)


