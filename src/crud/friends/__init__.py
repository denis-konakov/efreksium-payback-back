from .. import CRUDBase, Session, UserNotFoundException, CannotAddHimselfToFriendsException, UserAlreadyYourFriendException
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
    def add(cls, db: Session, sender_id: int, recipient_id: int) -> FriendPrivate:
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
            return FriendPrivate.from_orm(n)
        if invite.status:
            raise UserAlreadyYourFriendException()
        invite.status = True
        db.commit()
        return FriendPrivate.from_orm(invite)
    @classmethod
    @throws([UserNotFoundException])
    def get(cls,
            db: Session,
            user_id: int,
            page: PaginateContentParams,
            exists: bool = False) -> PaginateContent[FriendPrivate]:
        if not exists:
            if db.query(UserDatabaseModel).filter_by(id=user_id).first() is None:
                raise UserNotFoundException()
        crit = q.and_(
            FriendDatabaseModel.status == True, q.or_(
                FriendDatabaseModel.sender_id == user_id,
                FriendDatabaseModel.recipient_id == user_id
            )
        )
        friends = db.query(FriendDatabaseModel)\
            .where(crit)\
            .order_by(FriendDatabaseModel.id)\
            .limit(page.count)\
            .offset(page.offset)\
            .all()
        total = db.query(FriendDatabaseModel).where(crit).count()
        return PaginateContent[FriendPrivate](
            result=friends,
            count=len(friends),
            total=total,
        )


