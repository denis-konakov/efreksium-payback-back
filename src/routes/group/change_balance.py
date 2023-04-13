from . import router
from utils import HTTPResponseModel, throws, ResponseException
from crud import GroupCRUD, ChangeBalanceEvent
from depends import Depends, get_db, Session, get_current_user, UserDatabaseModel
resp = HTTPResponseModel.success('Баланс участников группы успешно изменен')

@router.post('/change_balance',
             summary='Изменить баланс участников группы',
             responses=throws.docs([
                GroupCRUD.get,
                GroupCRUD.change_balance,
                get_db,
                get_current_user,
             ]))
def change_balance(group_id: int,
                   events: list[ChangeBalanceEvent],
                   db: Session = Depends(get_db),
                   user: UserDatabaseModel = Depends(get_current_user)):
    try:
        group = GroupCRUD.get(db, group_id, user)
        GroupCRUD.change_balance(db, group, user, events)
        return resp.response()
    except ResponseException as e:
        raise e.get()
