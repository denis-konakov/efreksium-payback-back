from db import Base
import sqlalchemy as q

class SubscriptionVariantDatabaseModel(Base):
    __tablename__ = 'subscription_variants'
    id = q.Column(q.Integer, primary_key=True, index=True)
    name = q.Column(q.String(128), nullable=False)
    description = q.Column(q.String(256), nullable=False)
    price = q.Column(q.Integer, nullable=False)
    duration = q.Column(q.Integer, nullable=False)  # in days
