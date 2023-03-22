import aiohttp.web_response

from ..err_proxy import CRUDBase
from utils import throws
from crud.exceptions import AttachmentServiceDeniedException
from aiohttp import ClientSession
from config import Config
import json
from crud.user import UserDatabaseModel
from .models import AvatarUploadInfo
from crud.exceptions import AvatarAlreadyExistsException
from crud.types import AttachmentID
class AttachmentsCRUD(CRUDBase):
    @classmethod
    @throws([
        AttachmentServiceDeniedException,
    ])
    def _session(cls) -> ClientSession:
        if not Config.AttachmentsService.ENABLED:
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
        async with cls._session() as session:
            data = json.dumps(dict(
                id=user.id,
                flags=flags
            ))
            async with session.post(f'{Config.AttachmentsService.PRIVATE_URL}/create', data=data) as resp:
                if not resp.status == 200:
                    raise AttachmentServiceDeniedException()
                body = await resp.json()
                return AvatarUploadInfo(**body)
    @classmethod
    @throws([
        create,
        AvatarAlreadyExistsException,
    ])
    async def create_avatar(cls, user: UserDatabaseModel):
        if user.avatar != AttachmentID.default():
            raise AvatarAlreadyExistsException()
        return await cls.create(user, {
            'type': 'user_avatar'
        })












            

