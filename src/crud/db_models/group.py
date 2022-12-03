from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship

class GroupDatabaseModel(Base):
    __tablename__ = 'groups'
    id = q.Column(q.Integer, primary_key=True, index=True)
    name = q.Column(q.String(128), nullable=False)


