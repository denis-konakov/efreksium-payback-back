from ..err_proxy import CRUDBase
from ..db_models import (
    UserDatabaseModel,
    GroupDatabaseModel,
    GroupRole,
    GroupMemberDatabaseModel,
    GroupHistoryDatabaseModel,
    GroupAction
)
from utils import throws
from sqlalchemy.orm import Session
from ..types import GroupName
from crud.exceptions import *
import sqlalchemy as q
class GroupCRUD(CRUDBase):
    @classmethod
    @throws([

    ])
    def record_event(cls,
                     db: Session,
                     group: GroupDatabaseModel,
                     user: UserDatabaseModel,
                     action: GroupAction,
                     payload: dict | None = None) -> GroupHistoryDatabaseModel:
        t = GroupHistoryDatabaseModel(
            group_id=group.id,
            user_id=user.id,
            action=action,
            action_description=payload or dict(),
        )
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    @classmethod
    @throws([
        GroupsCreateLimitException,
        record_event,
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
        cls.record_event(
            db,
            g,
            user,
            GroupAction.CREATE,
        )
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
        UserNotFoundException,
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
        UserAlreadyInGroupException,
    ])
    def add_member(cls,
                   db: Session,
                   initiator: UserDatabaseModel,
                   group: GroupDatabaseModel,
                   user: UserDatabaseModel) -> GroupMemberDatabaseModel:
        t = db.query(GroupMemberDatabaseModel).filter(q.and_(
            GroupMemberDatabaseModel.user_id == user.id,
            GroupMemberDatabaseModel.group_id == group.id
        )).limit(1).count() == 0
        if not t:
            raise UserAlreadyInGroupException()
        cls.record_event(
            db,
            group,
            initiator,
            GroupAction.ADD_MEMBER,
            dict(
                target=user.id,
            )
        )
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
        get_member,
        record_event,
    ])
    def set_role(cls,
                 db: Session,
                 initiator: UserDatabaseModel,
                 group: GroupDatabaseModel,
                 user: UserDatabaseModel,
                 role: GroupRole) -> GroupMemberDatabaseModel:
        t = cls.get_member(db, group, user)
        cls.record_event(
            db,
            group,
            initiator,
            GroupAction.CHANGE_ROLE,
            dict(
                target=user.id,
                old_role=t.role,
                new_role=role,
            )
        )
        t.role = role
        db.commit()
        db.refresh(t)
        return t

