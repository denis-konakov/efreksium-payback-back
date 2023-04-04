import datetime

import sqlalchemy as q
from sqlalchemy.orm import relationship

from db import Base
from crud.types import AttachmentID
from functools import cached_property
from crud.exceptions import WrongConfigurationException


class UserDatabaseModel(Base):
    __tablename__ = 'users'
    id = q.Column(q.Integer, primary_key=True, index=True)

    username = q.Column(q.String(128), unique=False)
    email = q.Column(q.String(128), unique=True)
    number = q.Column(q.String(20), unique=True)
    avatar = q.Column(q.String(32), nullable=False, default=AttachmentID.default())

    hashed_password = q.Column(q.String(128), nullable=False)

    email_confirmation_code = q.Column(q.String(128), nullable=True)
    email_confirmed = q.Column(q.Boolean, default=False)

    password_reset_code = q.Column(q.String(128))

    subscriptions = relationship('SubscriptionDatabaseModel', back_populates='user')

    groups = relationship('GroupMemberDatabaseModel', back_populates='user')

    actions = relationship('GroupHistoryDatabaseModel', back_populates='user')

    @cached_property
    def subscription(self):
        from ..db_models import SubscriptionDatabaseModel, SubscriptionVariantDatabaseModel
        t = self.session().execute(q.union_all(
            q.select(SubscriptionDatabaseModel.variant_id).where(q.and_(
                SubscriptionDatabaseModel.expiration_time > q.func.now(),
                SubscriptionDatabaseModel.user_id == self.id
            )).limit(1),
            q.select(SubscriptionVariantDatabaseModel.id).where(
                SubscriptionVariantDatabaseModel.default == True
            ).limit(1)
        ).limit(1)).first()
        if t is None or len(t) != 1:
            raise WrongConfigurationException
        r: SubscriptionVariantDatabaseModel = self.session()\
            .query(SubscriptionVariantDatabaseModel)\
            .filter(SubscriptionVariantDatabaseModel.id == t[0])\
            .first()
        return r
