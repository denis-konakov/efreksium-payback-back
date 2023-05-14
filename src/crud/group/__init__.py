from ..err_proxy import CRUDBase
from ..db_models import (
    UserDatabaseModel,
    GroupDatabaseModel,
    GroupMemberDatabaseModel,
    GroupHistoryDatabaseModel,
    GroupRolePermissions,
)
from utils import throws
from sqlalchemy.orm import Session
from ..types import GroupName
from crud.exceptions import *
from crud.friends import FriendsCRUD
import sqlalchemy as q
from .models import *



class GroupCRUD(CRUDBase):
    @classmethod
    @throws([

    ])
    def check_in_group(cls, db: Session, user: UserDatabaseModel, group: GroupDatabaseModel) -> GroupRole | None:
        t: GroupMemberDatabaseModel = db.query(GroupMemberDatabaseModel).filter(q.and_(
            GroupMemberDatabaseModel.user_id == user.id,
            GroupMemberDatabaseModel.group_id == group.id
        )).limit(1).first()
        if t is None:
            return None
        return t.role

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
        if len(cls.get_groups(db, user)) >= limit:
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
    def get_groups(cls,
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
        check_in_group,
        UserAlreadyInGroupException,
        GroupPermissionDeniedException,
        FriendsCRUD.is_friends,
    ])
    def add_member(cls,
                   db: Session,
                   initiator: UserDatabaseModel,
                   group: GroupDatabaseModel,
                   user: UserDatabaseModel) -> GroupMemberDatabaseModel:

        if cls.check_in_group(db, initiator, group) != GroupRolePermissions.SET_ROLE:
            raise GroupPermissionDeniedException()
        if cls.check_in_group(db, user, group) is not None:
            raise UserAlreadyInGroupException()
        if not FriendsCRUD.is_friends(db, initiator, user):
            raise GroupPermissionDeniedException()
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
        check_in_group,
        GroupPermissionDeniedException,
    ])
    def set_role(cls,
                 db: Session,
                 initiator: UserDatabaseModel,
                 group: GroupDatabaseModel,
                 user: UserDatabaseModel,
                 role: GroupRole) -> GroupMemberDatabaseModel:
        if cls.check_in_group(db, user, group) != GroupRolePermissions.SET_ROLE:
            raise GroupPermissionDeniedException()
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

    @classmethod
    @throws([
        check_in_group,
        GroupNotFoundException,
        GroupPermissionDeniedException,
    ])
    def get(cls, db: Session, group_id: int, user: UserDatabaseModel | None = None) -> GroupDatabaseModel:
        group = db.query(GroupDatabaseModel).filter(
            GroupDatabaseModel.id == group_id
        ).first()
        if group is None:
            raise GroupNotFoundException()
        if user is None or cls.check_in_group(db, user, group) is not None:
            return group
        raise GroupPermissionDeniedException()

    @classmethod
    @throws([
        UserNotFoundException,
        GroupPermissionDeniedException,
    ])
    def change_balance(cls,
                       db: Session,
                       group: GroupDatabaseModel,
                       user: UserDatabaseModel,
                       events: list[ChangeBalanceEvent]):
        if cls.check_in_group(db, user, group) != GroupRolePermissions.CHANGE_BALANCE:
            raise GroupPermissionDeniedException()
        members: list[GroupMemberDatabaseModel] = group.members
        for i in events:
            member = [j for j in members if j.id == i.target_id]
            if len(member) != 1:
                raise UserNotFoundException()
            member = member[0]
            cls.record_event(
                db,
                group,
                user,
                GroupAction.CHANGE_BALANCE,
                dict(
                    target_id=i.target_id,
                    old_balance=member.balance,
                    new_balance=member.balance + i.value,
                )
            )
            member.balance += i.value
        db.commit()
