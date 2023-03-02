import sqlalchemy as q
from sqlalchemy.orm import relationship
from db import Base
import enum
class ConfirmationVariant(enum.IntEnum):
    NONE = enum.auto()
    REGISTRATION = enum.auto()
    PASSWORD_RESET = enum.auto()

class UserDatabaseModel(Base):
    __tablename__ = 'users'
    id = q.Column(q.Integer, primary_key=True, index=True)
    username = q.Column(q.String(128), unique=True, index=True)
    email = q.Column(q.String(128), unique=True)
    number = q.Column(q.String(20), unique=True)
    hashed_password = q.Column(q.String(128), nullable=False)
    is_active = q.Column(q.Boolean, default=False)
    confirmation_code = q.Column(q.String(128), nullable=True)
    confirmation_variant = q.Column(q.Enum(ConfirmationVariant))
    subscription_id = q.Column(q.Integer, q.ForeignKey('subscriptions.id'))
    subscription = relationship('SubscriptionDatabaseModel', backref='users')


