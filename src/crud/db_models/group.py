from db import Base
import sqlalchemy as q
from sqlalchemy.orm import relationship
from crud.types import AttachmentID
class GroupDatabaseModel(Base):
    __tablename__ = 'group'
    id = q.Column(q.Integer, primary_key=True, index=True)
    name = q.Column(q.String(128), nullable=False)
    avatar = q.Column(q.String(32), nullable=False, default=AttachmentID.default())

    history = relationship('GroupHistoryDatabaseModel', back_populates='group')
    members = relationship('GroupMemberDatabaseModel', back_populates='group')


