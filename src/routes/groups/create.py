from . import router
from utils import throws
from crud.types import GroupName
from depends import Depends, UserDatabaseModel, get_current_user
from utils import HTTPResponseModel


resp = HTTPResponseModel.success('Группа успешно создана')

@router.post('/create',
             summary='Создать группу',
             responses={
                **throws.docs([
                    resp,
                ])
             })
def groups_create(name: GroupName,
                  user: UserDatabaseModel = Depends(get_current_user)):
    pass
