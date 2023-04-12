from . import router
from utils import throws
from crud.types import GroupName
from crud import GroupCRUD, Group
from depends import Depends, UserDatabaseModel, get_current_user, Session, get_db
from utils import HTTPResponseModel, ResponseException

resp = HTTPResponseModel.success('Группа успешно создана', Group)

@router.post('/create',
             summary='Создать группу',
             responses={
                **throws.docs([
                    resp,
                    GroupCRUD.create
                ])
             })
def groups_create(name: GroupName,
                  db: Session = Depends(get_db),
                  user: UserDatabaseModel = Depends(get_current_user)) -> Group:
    try:
        group = GroupCRUD.create(db, user, name)
    except ResponseException as e:
        raise e.get()
    return resp.response(Group.from_orm(group))



