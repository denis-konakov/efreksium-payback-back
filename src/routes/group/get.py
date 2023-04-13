from . import router
from utils import throws
from crud import GroupCRUD, GroupFull
from depends import Depends, UserDatabaseModel, get_current_user, Session, get_db
from utils import HTTPResponseModel, ResponseException

resp = HTTPResponseModel.success('Информация о группе успешно получена', GroupFull)

@router.get('/{group_id}',
            summary='Получить подробную информацию о группе',
            responses={
                **throws.docs([
                    resp,
                    GroupCRUD.get
                ])
            })
def groups_list(group_id: int,
                db: Session = Depends(get_db),
                user: UserDatabaseModel = Depends(get_current_user)) -> GroupFull:
    try:
        group = GroupCRUD.get(db, group_id, user)
        return resp.response(GroupFull.from_orm(group))
    except ResponseException as e:
        raise e.get()



