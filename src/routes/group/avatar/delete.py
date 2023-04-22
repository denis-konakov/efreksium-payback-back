from . import router
from utils import throws, HTTPResponseModel, ResponseException
from crud import AttachmentsCRUD, GroupCRUD, GroupRolePermissions, GroupPermissionDeniedException
from depends import Depends, get_current_user, UserDatabaseModel, Session, get_db

resp = HTTPResponseModel.success('Аватар удален')


@router.post('/delete',
             summary='Удалить аватар',
             responses=throws.docs([
                 resp,
                 AttachmentsCRUD.delete_group_avatar,
                 get_db,
                 get_current_user,
                 GroupCRUD.check_in_group,
                 GroupPermissionDeniedException,
                 GroupCRUD.get,
             ]))
async def delete_avatar(group_id: int,
                        db: Session = Depends(get_db),
                        user: UserDatabaseModel = Depends(get_current_user)):
    try:
        group = GroupCRUD.get(db, group_id, user)
        if GroupCRUD.check_in_group(db, user, group) != GroupRolePermissions.CHANGE_AVATAR:
            raise GroupPermissionDeniedException()
        await AttachmentsCRUD.delete_group_avatar(user)
        return resp.response()
    except ResponseException as e:
        raise e.get()
