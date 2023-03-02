from depends import Depends, get_current_user, UserPrivate
from . import router
from utils.response import HTTPResponseModel
from utils.throws import throws
from crud import UserCRUD, TokenDecodeException, ResponseException
doc, resp = HTTPResponseModel.success('Код для смены пароля отправлен')

@router.post(
    '/change_password',
     summary='Сменить пароль',
     responses={
         **throws.docs([
             get_current_user
         ]),
         **doc,
     }
)
def change_password(user: UserPrivate = Depends(get_current_user)):
    pass
