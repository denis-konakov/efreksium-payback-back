import sqlalchemy as q
from sqlalchemy.orm import relationship
from db import Base


class UserDatabaseModel(Base):
    __tablename__ = 'users'
    id = q.Column(q.Integer, primary_key=True, index=True)
    username = q.Column(q.String(128), unique=True, index=True)
    email = q.Column(q.String(128), unique=True)
    number = q.Column(q.String(20), unique=True)
    hashed_password = q.Column(q.String(128), nullable=False)
    is_active = q.Column(q.Boolean, default=True)
    subscription_id = q.Column(q.Integer, q.ForeignKey('subscriptions.id'))
    subscription = relationship('SubscriptionDatabaseModel', backref='users')


