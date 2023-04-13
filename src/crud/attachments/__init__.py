
from ..err_proxy import CRUDBase
from utils import throws
from crud.exceptions import AttachmentServiceDeniedException
from aiohttp import ClientSession
from config import Config
from crud.user import UserDatabaseModel
from crud.group import GroupDatabaseModel
from .models import AvatarUploadInfo
from crud.exceptions import AvatarAlreadyExistsException
from crud.types import AttachmentID
from loguru import logger
class AttachmentsCRUD(CRUDBase):
    @classmethod
    @throws([
        AttachmentServiceDeniedException,
    ])
    def _session(cls) -> ClientSession:
        if not Config.AttachmentsService.ENABLED:
            logger.warning('Attachments service disabled in config')
            raise AttachmentServiceDeniedException()
        return ClientSession(headers={
            'X-Token': Config.AttachmentsService.SECRET_KEY,
        })
    @classmethod
    @throws([
        _session,
        AttachmentServiceDeniedException,
    ])
    async def create(cls, target: UserDatabaseModel | GroupDatabaseModel, flags: dict) -> AvatarUploadInfo:
        tid = target.id
        if isinstance(target, GroupDatabaseModel):
            tid  = -tid
        try:
            async with cls._session() as session:
                data = dict(
                    id=tid,
                    flags=flags
                )
                async with session.post(f'{Config.AttachmentsService.PRIVATE_URL}/create', json=data) as resp:
                    logger.debug('AttachmentsService.create response {}', await resp.json())
                    if not resp.status == 200:
                        raise AttachmentServiceDeniedException()
                    body = await resp.json()
                    return AvatarUploadInfo(**body)
        except Exception as e:
            logger.warning('Error while run /create method on AttachmentsService\n{}', e)
            raise AttachmentServiceDeniedException()
    @classmethod
    @throws([
        _session,
    ])
    def delete(cls, target: UserDatabaseModel | GroupDatabaseModel):
        ...
    @classmethod
    @throws([
        create,
        AvatarAlreadyExistsException,
    ])
    async def create_user_avatar(cls, user: UserDatabaseModel):
        if user.avatar != AttachmentID.default():
            raise AvatarAlreadyExistsException()
        data = await cls.create(user, {
            'type': 'user_avatar'
        })
        user.avatar = data.image_id
        user.session().commit()
        return data

    @classmethod
    @throws([
        _session,
    ])
    async def delete_user_avatar(cls, user: UserDatabaseModel):
        ...















            

