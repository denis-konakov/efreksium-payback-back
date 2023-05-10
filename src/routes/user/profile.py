from fastapi import Depends
from depends import Session, get_db, get_current_user
from crud import UserDatabaseModel, UserPublicWithGroupsAndFriends, GroupDatabaseModel
from . import router
from utils.throws import throws
from utils import HTTPResponseModel
from crud import FriendsCRUD, PaginateContentParams
resp = HTTPResponseModel.success(
    'Получение данных пользователя',
    UserPublicWithGroupsAndFriends
)
@router.get(
    '/profile',
    summary="Получение данных о пользователе",
    responses={
        **throws.docs([
            get_current_user,
            resp
        ]),
    }
)
def profile(db: Session = Depends(get_db),
            user: UserDatabaseModel = Depends(get_current_user)) -> UserPublicWithGroupsAndFriends:
    user.friends = FriendsCRUD.user_accepted_friends(db, user)
    return resp.response(
        UserPublicWithGroupsAndFriends.from_orm(user)
    )
