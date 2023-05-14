from . import router
from depends import Depends, Session, get_db, get_current_user, UserDatabaseModel
from utils import HTTPResponseModel, throws, ResponseException
from crud import GroupCRUD, UserCRUD
resp = HTTPResponseModel.success('Пользователь успешно добавлен в группу')

@router.post('/add',
             summary='Добавить участника в группу (можно добавлять только друзей)',
             responses=throws.docs([
                 resp,
                 get_db,
                 get_current_user,
                 UserCRUD.get,
                 GroupCRUD.get,
                 GroupCRUD.add_member,
             ]))
def add_member(group_id: int, user_id: int,
               db: Session = Depends(get_db),
               user: UserDatabaseModel = Depends(get_current_user)):
    try:
        adduser = UserCRUD.get(db, id=user_id)
        group = GroupCRUD.get(db, group_id, user)
        GroupCRUD.add_member(db, user, group, adduser)
        return resp.response()
    except ResponseException as e:
        raise e.get()
