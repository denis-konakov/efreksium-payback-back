from . import router
from crud import GroupCRUD, GroupWithHistory
from depends import Depends, get_db, Session, UserDatabaseModel, get_current_user
from utils import HTTPResponseModel, throws, ResponseException

resp = HTTPResponseModel.success('История группы успешно получена', GroupWithHistory)

@router.get('/{group_id}',
            summary='Информация о группе',
            responses=throws.docs([
                resp,
                get_db,
                get_current_user,
                GroupCRUD.get,
            ]))
def get_history(group_id: int,
                db: Session = Depends(get_db),
                user: UserDatabaseModel = Depends(get_current_user)) -> GroupWithHistory:
    try:
        t = GroupCRUD.get(db, group_id, user)
        return resp.response(GroupWithHistory.from_orm(
            t
        ))
    except ResponseException as e:
        raise e.get()

