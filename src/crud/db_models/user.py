import sqlalchemy as q
from sqlalchemy.orm import relationship
from db import Base


class UserDatabaseModel(Base):
    __tablename__ = 'users'
    id = q.Column(q.Integer, primary_key=True, index=True)

    username = q.Column(q.String(128), unique=False)
    email = q.Column(q.String(128), unique=True)
    number = q.Column(q.String(20), unique=True)
    avatar = q.Column(q.String(32), nullable=False, default='default')

    hashed_password = q.Column(q.String(128), nullable=False)

    email_confirmation_code = q.Column(q.String(128), nullable=True)
    email_confirmed = q.Column(q.Boolean, default=False)

    password_reset_code = q.Column(q.String(128))

    subscription_id = q.Column(q.Integer, q.ForeignKey('subscriptions.id'))
    subscription = relationship('SubscriptionDatabaseModel', backref='users')


