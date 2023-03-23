
from ..err_proxy import CRUDBase
from utils import throws
from crud.exceptions import AttachmentServiceDeniedException
from aiohttp import ClientSession
from config import Config
from crud.user import UserDatabaseModel
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
    async def create(cls, user: UserDatabaseModel, flags: dict) -> AvatarUploadInfo:
        try:
            async with cls._session() as session:
                data = dict(
                    id=user.id,
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
        create,
        AvatarAlreadyExistsException,
    ])
    async def create_avatar(cls, user: UserDatabaseModel):
        if user.avatar != AttachmentID.default():
            raise AvatarAlreadyExistsException()
        data = await cls.create(user, {
            'type': 'user_avatar'
        })
        user.avatar = data.image_id
        user.session().commit()
        return data












            

