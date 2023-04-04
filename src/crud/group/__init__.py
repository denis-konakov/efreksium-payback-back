from ..err_proxy import CRUDBase
from ..db_models import UserDatabaseModel, GroupDatabaseModel, GroupRole, GroupMemberDatabaseModel
from utils import throws
from sqlalchemy.orm import Session
from ..types import GroupName
from crud.exceptions import *
import sqlalchemy as q
class GroupCRUD(CRUDBase):
    @classmethod
    @throws([
        GroupsCreateLimitException
    ])
    def create(cls,
               db: Session,
               user: UserDatabaseModel,
               name: GroupName) -> GroupDatabaseModel:
        limit = user.subscription.groups_limit
        if len(cls.get_members(db, user)) >= limit:
            raise GroupsCreateLimitException()
        g = GroupDatabaseModel(
            name=name,
        )
        db.add(g)
        db.commit()
        db.refresh(g)
        m = GroupMemberDatabaseModel(
            user_id=user.id,
            group_id=g.id,
            role=GroupRole.OWNER,
        )
        db.add(m)
        db.commit()
        return g
    @classmethod
    @throws([

    ])
    def get_members(cls,
                    db: Session,
                    user: UserDatabaseModel) -> list[GroupMemberDatabaseModel]:
        return db.query(GroupMemberDatabaseModel).where(
            GroupMemberDatabaseModel.user_id == user.id
        ).all()
    @classmethod
    @throws([
        UserNotFoundException
    ])
    def get_member(cls,
                   db: Session,
                   group: GroupDatabaseModel,
                   user: UserDatabaseModel) -> GroupMemberDatabaseModel:
        t = db.query(GroupMemberDatabaseModel).filter(q.and_(
            GroupMemberDatabaseModel.group_id == group.id,
            GroupMemberDatabaseModel.user_id == user.id
        )).first()
        if t is None:
            raise UserNotFoundException()
        return t
    @classmethod
    @throws([
        UserAlreadyInGroupException
    ])
    def add_user(cls,
                 db: Session,
                 group: GroupDatabaseModel,
                 user: UserDatabaseModel) -> GroupMemberDatabaseModel:
        t = db.query(GroupMemberDatabaseModel).filter(q.and_(
            GroupMemberDatabaseModel.user_id == user.id,
            GroupMemberDatabaseModel.group_id == group.id
        )).limit(1).count() == 0
        if not t:
            raise UserAlreadyInGroupException()
        gm = GroupMemberDatabaseModel(
            user_id=user.id,
            group_id=group.id
        )
        db.add(gm)
        db.commit()
        db.refresh(gm)
        return gm
    @classmethod
    @throws([
        get_member
    ])
    def set_role(cls,
                 db: Session,
                 group: GroupDatabaseModel,
                 user: UserDatabaseModel,
                 role: GroupRole) -> GroupMemberDatabaseModel:
        t = cls.get_member(db, group, user)
        t.role = role
        db.commit()
        db.refresh(t)
        return t

