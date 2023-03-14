from . import router
from depends import Depends, get_db, Session
from crud import UserShared, UserCRUD, ResponseException, UserNotFoundException
from utils import throws, HTTPResponseModel

resp = HTTPResponseModel.success('Информация о пользователе получена успешно', UserShared)

@router.get('/get/{user_id}',
            summary='Получение публичной информации о пользователе',
            responses={
                **throws.docs([
                    get_db,
                    UserCRUD.get,
                    UserNotFoundException,
                    resp,
                ]),
            })
def get_user(user_id: int,
             db: Session = Depends(get_db)) -> UserShared:
    try:
        user = UserCRUD.get(db, id=user_id)
    except ResponseException as e:
        raise e.get()
    if not user.is_active:
        raise UserNotFoundException.get()
    return resp.response(UserShared.from_orm(user))
