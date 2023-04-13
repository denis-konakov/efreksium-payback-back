from . import router
from depends import Depends, Session, get_db, get_current_user, UserDatabaseModel
from utils import HTTPResponseModel, throws, ResponseException
from crud import GroupCRUD, UserCRUD, GroupRole
resp = HTTPResponseModel.success('Роль пользователя изменена')

@router.post('/set_role',
             summary='Изменить роль участника',
             responses=throws.docs([
                 resp,
                 get_db,
                 get_current_user,
                 UserCRUD.get,
                 GroupCRUD.get,
                 GroupCRUD.set_role,
             ]))
def add_member(group_id: int,
               user_id: int,
               role: GroupRole,
               db: Session = Depends(get_db),
               user: UserDatabaseModel = Depends(get_current_user)):
    try:
        adduser = UserCRUD.get(db, id=user_id)
        group = GroupCRUD.get(db, group_id, user)
        GroupCRUD.set_role(db, user, group, adduser, role)
    except ResponseException as e:
        raise e.get()
