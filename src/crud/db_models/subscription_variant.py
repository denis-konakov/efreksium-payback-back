from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship

class SubscriptionVariantDatabaseModel(Base):
    __tablename__ = 'subscription_variants'

    id = q.Column(q.Integer, primary_key=True, index=True)
    default = q.Column(q.Boolean, default=False, nullable=False)

    name = q.Column(q.String(128), nullable=False)
    description = q.Column(q.String(256), nullable=False)

    price = q.Column(q.Integer, nullable=False)
    duration = q.Column(q.Integer, nullable=False)  # in days

    groups_limit = q.Column(q.Integer, nullable=False)
    vip_groups = q.Column(q.Boolean, default=False, nullable=False)
    unlimited = q.Column(q.Boolean, default=False, nullable=False)  # снимает все ограничения

    subscriptions = relationship('SubscriptionDatabaseModel', back_populates='variant')


