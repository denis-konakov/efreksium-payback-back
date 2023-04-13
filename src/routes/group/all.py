from . import router
from utils import throws
from crud.types import GroupName
from crud import GroupCRUD, Group
from depends import Depends, UserDatabaseModel, get_current_user, Session, get_db
from utils import HTTPResponseModel, ResponseException
from pydantic import BaseModel
class GroupList(BaseModel):
    __root__: list[Group]

resp = HTTPResponseModel.success('Список групп успешно получен', GroupList)

@router.get('/all',
            summary='Получить список групп',
            responses={
                **throws.docs([
                    resp,
                    GroupCRUD.get_groups
                ])
            })
def groups_list(db: Session = Depends(get_db),
                user: UserDatabaseModel = Depends(get_current_user)) -> GroupList:
    try:
        groups = GroupCRUD.get_groups(db, user)
        groups = GroupList.parse_obj([
            i.group
            for i in groups
        ])
        return resp.response(groups)
    except ResponseException as e:
        raise e.get()



