from . import router
from utils import throws, HTTPResponseModel, ResponseException
from crud import AttachmentsCRUD, AvatarUploadInfo
from depends import Depends, get_current_user, UserDatabaseModel

resp = HTTPResponseModel.success('Аватар удален')


@router.post('/delete',
             summary='Удалить аватар',
             responses=throws.docs([
                 resp,
                 AttachmentsCRUD.delete_user_avatar,
                 get_current_user,
             ]))
async def delete_avatar(user: UserDatabaseModel = Depends(get_current_user)):
    try:
        await AttachmentsCRUD.delete_user_avatar(user)
        return resp.response()
    except ResponseException as e:
        raise e.get()
