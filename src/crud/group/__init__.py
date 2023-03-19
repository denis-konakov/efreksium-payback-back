from ..err_proxy import CRUDBase
from ..db_models import UserDatabaseModel
from utils import throws
from sqlalchemy.orm import Session
from ..types import GroupName
class GroupCRUD(CRUDBase):
    @throws([

    ])
    def create(self, db: Session, user: UserDatabaseModel, name: GroupName):
        pass
