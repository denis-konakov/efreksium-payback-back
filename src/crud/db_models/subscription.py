from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
import datetime
class SubscriptionDatabaseModel(Base):
    __tablename__ = 'subscriptions'
    id = q.Column(q.Integer, primary_key=True, index=True)
    variant_id = q.Column(q.Integer, q.ForeignKey('subscription_variants.id'))
    variant = relationship('SubscriptionVariantDatabaseModel', backref='subscriptions')
    receipt_time = q.Column(q.DateTime, nullable=False)
    expiration_time = q.Column(q.DateTime, nullable=False)
    def is_expired(self):
        return self.expiration_time < datetime.datetime.utcnow()
    def is_active(self):
        return not self.is_expired()
