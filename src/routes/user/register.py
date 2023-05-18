from config import Config
from crud import (
    UserRegistrationForm,
    UserCRUD,
    UserAlreadyExistsException,
    UserNotFoundException,
    UserNotActiveException,
    UserDatabaseModel,
)
from depends import confirm
from depends import get_db, Session, Depends, get_mail, MailManager
from utils import HTTPResponseModel, ResponseException, throws
from . import router
from sqlalchemy.inspection import inspect

resp = HTTPResponseModel.success(
    'Код подтверждения почты отправлен' if Config.Email.ENABLED else
    'Успешная регистрация'
)

@router.post(
    '/register',
     summary='Регистрация пользователя',
     responses={
         **throws.docs([
             confirm,
             get_db,
             MailManager.send_confirmation,
             UserCRUD.register,
             UserCRUD.generate_email_confirmation_code,
             UserNotFoundException,
             UserAlreadyExistsException,
             UserNotActiveException,
             resp,
         ]),
     }
)
def register(data: UserRegistrationForm,
             link: confirm.type = Depends(confirm),
             db: Session = Depends(get_db),
             mail: MailManager = Depends(get_mail)):
    try:
        user = UserCRUD.register(db, data, not Config.Email.ENABLED)
<<<<<<< HEAD
=======
        
>>>>>>> 2fbbd5d645757d4e23960c20ae121f8088e56a42
    except UserAlreadyExistsException as e:
        user: UserDatabaseModel = e.additional.get('user')
        if user.email_confirmed:
            raise UserAlreadyExistsException.get()
    if Config.Email.ENABLED:
        code = UserCRUD.generate_email_confirmation_code(user)
        mail.send_confirmation(user.email, link(code.private), user)
    return resp.response()






