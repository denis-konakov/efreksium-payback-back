from . import router
from depends import *
from crud import FriendsCRUD, PaginateContentParams, PaginateContent, FriendPublic
from utils import throws, HTTPResponseModel
resp = HTTPResponseModel.success('Список друзей', PaginateContent[FriendPublic])
@router.get('/get',
            summary='Получить список друзей',
            responses=throws.docs([
                FriendsCRUD.get,
                get_db,
                get_current_user,
                resp
            ]))
def friends_get(page: PaginateContentParams,
                user: UserPrivate = Depends(get_current_user),
                db: Session = Depends(get_db)):
    try:
        return resp.response(PaginateContent[FriendPublic].from_orm(
            FriendsCRUD.get(db, user.id, page, True)
        ))
    except ResponseException as e:
        raise e.get()
