from . import router
from utils import throws, HTTPResponseModel, ResponseException
from crud import AttachmentsCRUD, AvatarUploadInfo, GroupCRUD, GroupRolePermissions
from depends import Depends, get_current_user, UserDatabaseModel, Session, get_db
from crud.exceptions import *

resp = HTTPResponseModel.success('Ссылка для загрузки медиа подготовлена', AvatarUploadInfo)


@router.post('/create',
             summary='Загрузить аватар',
             description='Возвращает ссылку и ключ, которые нужны для загрузки вложений в сервис вложений',
             responses=throws.docs([
                 resp,
                 GroupCRUD.get,
                 AttachmentsCRUD.create_group_avatar,
                 get_current_user,
                 GroupPermissionDeniedException,
                 GroupCRUD.check_in_group,
                 get_db,
             ]))
async def create_avatar(group_id: int,
                        db: Session = Depends(get_db),
                        user: UserDatabaseModel = Depends(get_current_user)) -> AvatarUploadInfo:
    try:
        group = GroupCRUD.get(db, group_id, user)
        if GroupCRUD.check_in_group(db, user, group) != GroupRolePermissions.CHANGE_AVATAR:
            raise GroupPermissionDeniedException()
        data = await AttachmentsCRUD.create_group_avatar(group)
        return resp.response(data)
    except ResponseException as e:
        raise e.get()
