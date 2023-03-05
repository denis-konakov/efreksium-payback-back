from . import router
from fastapi import Query
from utils import throws, HTTPResponseModel, ResponseException
from crud import FriendsCRUD

from depends import Depends, Session, get_db, UserPrivate, get_current_user

invite_send = HTTPResponseModel.success('Приглашение в друзья отправлено')
invite_accept = HTTPResponseModel.success('Приглашение в друзья принято')
@router.post('/add',
             summary='Добавить друга',
             responses={
                 **throws.docs([
                     get_current_user,
                     get_db,
                     FriendsCRUD.add,
                     invite_send,
                     invite_accept,
                 ])
             })
def friends_add(recipient_id: int,
                user: UserPrivate = Depends(get_current_user),
                db: Session = Depends(get_db)):
    try:
        invite = FriendsCRUD.add(db, user.id, recipient_id)
    except ResponseException as e:
        raise e.get()
    if invite.status:
        return invite_accept.response()
    return invite_send.response()


