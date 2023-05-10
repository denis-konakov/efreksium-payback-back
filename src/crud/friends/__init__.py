from crud.exceptions import *
from sqlalchemy.orm import Session
from crud.err_proxy import CRUDBase
import sqlalchemy as q
from ..db_models import FriendDatabaseModel, UserDatabaseModel
from .models import *
from utils import throws, PaginateContent, PaginateContentParams


class FriendsCRUD(CRUDBase):
    @classmethod
    @throws([
        UserNotFoundException,
        UserAlreadyYourFriendException,
        CannotAddHimselfToFriendsException,
    ])
    def add(cls, db: Session, sender_id: int, recipient_id: int) -> FriendDatabaseModel:
        if sender_id == recipient_id:
            raise CannotAddHimselfToFriendsException()
        check_user_exists = db.query(UserDatabaseModel).where(q.or_(
            UserDatabaseModel.id == sender_id,
            UserDatabaseModel.id == recipient_id,
        )).count() == 2
        if not check_user_exists:
            raise UserNotFoundException()

        invite: FriendDatabaseModel | None = db.query(FriendDatabaseModel).where(q.or_(
            FriendDatabaseModel.sender_id == sender_id & FriendDatabaseModel.recipient_id == recipient_id,
            FriendDatabaseModel.sender_id == recipient_id & FriendDatabaseModel.recipient_id == sender_id,
        )).first()
        if invite is None:
            # Send invite
            n = FriendDatabaseModel(sender_id=sender_id, recipient_id=recipient_id)
            db.add(n)
            db.commit()
            db.refresh(n)
            return n
        if invite.status:
            raise UserAlreadyYourFriendException()
        invite.status = True
        db.commit()
        db.refresh(invite)
        return invite

    @classmethod
    @throws([

    ])
    def get(cls,
            db: Session,
            user: UserDatabaseModel,
            page: PaginateContentParams) -> PaginateContent[FriendDatabaseModel]:
        crit = q.and_(
            FriendDatabaseModel.status == True, q.or_(
                FriendDatabaseModel.sender_id == user.id,
                FriendDatabaseModel.recipient_id == user.id
            )
        )
        friends = db.query(FriendDatabaseModel) \
            .where(crit) \
            .order_by(FriendDatabaseModel.id) \
            .limit(page.count) \
            .offset(page.offset) \
            .all()
        total = db.query(FriendDatabaseModel).where(crit).count()
        return PaginateContent[FriendDatabaseModel](
            result=friends,
            count=len(friends),
            total=total,
        )

    @classmethod
    @throws([

    ])
    def is_friends(cls, db: Session, user1: UserDatabaseModel, user2: UserDatabaseModel) -> bool:
        return db.query(FriendDatabaseModel).filter(
            (FriendDatabaseModel.sender_id == user1.id & FriendDatabaseModel.recipient_id == user2.id) |
            (FriendDatabaseModel.sender_id == user2.id & FriendDatabaseModel.recipient_id == user1.id) &
            FriendDatabaseModel.status == True
        ).limit(1).count() == 1

    @classmethod
    @throws([

    ])
    def user_accepted_friends(cls, db: Session, user: UserDatabaseModel) -> list[UserDatabaseModel]:
        return db.query(UserDatabaseModel).filter(
            ((UserDatabaseModel.id == FriendDatabaseModel.sender_id & FriendDatabaseModel.recipient_id == user.id) |
             (UserDatabaseModel.id == FriendDatabaseModel.recipient_id & FriendDatabaseModel.sender_id == user.id)) &
            FriendDatabaseModel.status == True
        ).all()
