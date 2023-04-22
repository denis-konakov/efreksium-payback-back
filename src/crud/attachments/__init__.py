
from ..err_proxy import CRUDBase
from utils import throws
from crud.exceptions import AttachmentServiceDeniedException
from aiohttp import ClientSession
from config import Config
from crud.user import UserDatabaseModel
from crud.group import GroupDatabaseModel
from .models import AvatarUploadInfo
from crud.exceptions import *
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
    async def create(cls, target: int, flags: dict) -> AvatarUploadInfo:
        tid = target
        try:
            async with cls._session() as session:
                data = dict(
                    id=tid,
                    flags=flags
                )
                async with session.post(f'{Config.AttachmentsService.PRIVATE_URL}/create', json=data) as resp:
                    logger.debug('AttachmentsService.create response {}', await resp.json())
                    assert resp.status == 200
                    body = await resp.json()
                    return AvatarUploadInfo(**body)
        except Exception as e:
            logger.warning('Error while run /create method on AttachmentsService\n{}', e)
            raise AttachmentServiceDeniedException()
    @classmethod
    @throws([
        _session,
        AttachmentServiceDeniedException,
    ])
    async def delete(cls, image_id: AttachmentID):
        try:
            data = {
                'image_id': image_id,
            }
            async with cls._session() as s:
                async with s.post(f'{Config.AttachmentsService.PRIVATE_URL}/delete', json=data) as req:
                    assert req.status == 200
                    await req.json()

        except Exception as e:
            logger.warning('Error while run /delete method on AttachmentsService\n{}', e)
            raise AttachmentServiceDeniedException()

    @classmethod
    @throws([
        create,
        AvatarAlreadyExistsException,
    ])
    async def create_user_avatar(cls, user: UserDatabaseModel):
        if user.avatar != AttachmentID.default():
            raise AvatarAlreadyExistsException()
        data = await cls.create(user.id, {
            'type': 'user_avatar'
        })
        user.avatar = data.image_id
        user.session().commit()
        return data

    @classmethod
    @throws([
        delete,
        AvatarDontExistsException,
    ])
    async def delete_user_avatar(cls, user: UserDatabaseModel):
        if user.avatar == AttachmentID.default():
            raise AvatarDontExistsException()
        await cls.delete(user.avatar)
        user.avatar = AttachmentID.default()
        user.session().commit()

    @classmethod
    @throws([
        create,
        AvatarAlreadyExistsException,
    ])
    async def create_group_avatar(cls, group: GroupDatabaseModel) -> AvatarUploadInfo:
        if group.avatar != AttachmentID.default():
            raise AvatarAlreadyExistsException()
        data = await cls.create(-group.id, {
            'type': 'user_avatar'
        })
        group.avatar = data.image_id
        group.session().commit()
        return data
    @classmethod
    @throws([
        delete,
        AvatarDontExistsException
    ])
    async def delete_group_avatar(cls, group: GroupDatabaseModel):
        if group.avatar == AttachmentID.default():
            raise AvatarDontExistsException()
        await cls.delete(group.avatar)
        group.avatar = AttachmentID.default()
        group.session().commit()



















            

