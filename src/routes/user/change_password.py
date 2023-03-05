from depends import Depends, get_db, get_mail, Session, MailManager, get_confirm_link, get_confirm_link_type
from . import router
from utils.response import HTTPResponseModel
from utils.throws import throws
from crud import UserCRUD, ResponseException
from pydantic import EmailStr
resp = HTTPResponseModel.success('Код для смены пароля отправлен')

@router.post(
    '/change_password',
     summary='Сменить пароль',
     responses={
         **throws.docs([
             get_db,
             get_mail,
             UserCRUD.get_user_by_email,
             resp
         ]),
     }
)
def change_password(email: EmailStr,
                    confirm_link: get_confirm_link_type = Depends(get_confirm_link),
                    db: Session = Depends(get_db),
                    mail: MailManager = Depends(get_mail)):
    try:
        user = UserCRUD.get_user_by_email(db, email)
    except ResponseException as e:
        raise e.get()
    code = UserCRUD.generate_confirmation_code(db, user.id, UserCRUD.cv.RESET_PASSWORD)
    link = confirm_link(code)
    mail.send_confirmation(email, link, user)
    return resp.response()


