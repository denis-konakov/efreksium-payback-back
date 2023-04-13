from routes.user import router
from utils import throws, HTTPResponseModel, ResponseException
from crud import AttachmentsCRUD, AvatarUploadInfo
from depends import Depends, get_current_user, UserDatabaseModel

resp = HTTPResponseModel.success('Ссылка для загрузки медиа подготовлена', AvatarUploadInfo)


@router.post('/create',
             summary='Загрузить аватар',
             description='Возвращает ссылку и ключ, которые нужны для загрузки вложений в сервис вложений',
             responses=throws.docs([
                 resp,
                 AttachmentsCRUD.create_user_avatar,
                 get_current_user,
             ]))
async def create_avatar(user: UserDatabaseModel = Depends(get_current_user)) -> AvatarUploadInfo:
    try:
        data = await AttachmentsCRUD.create_user_avatar(user)
        return resp.response(data)
    except ResponseException as e:
        raise e.get()
