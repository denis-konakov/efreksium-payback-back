from depends import Depends, get_db, get_mail, Session, MailManager, confirm
from . import router
from utils.response import HTTPResponseModel
from utils.throws import throws
from crud import UserCRUD, ResponseException
from pydantic import EmailStr, AnyHttpUrl
from utils import url_add_arguments

resp = HTTPResponseModel.success('Код для смены пароля отправлен')


@router.post(
    '/send_reset_password_code',
     summary='Отправить код для смены пароля',
     responses={
         **throws.docs([
             get_db,
             get_mail,
             UserCRUD.get,
             resp
         ]),
     })
def send_reset_password_code(email: EmailStr,
                             link: confirm.type = Depends(confirm),
                             db: Session = Depends(get_db),
                             mail: MailManager = Depends(get_mail)):
    try:
        user = UserCRUD.get(db, email=email)
    except ResponseException as e:
        raise e.get()
    code = UserCRUD.generate_reset_password_code(user)
    mail.send_confirmation(
        to=email,
        link=link(code.private),
        user=user,
    )
    return resp.response()


