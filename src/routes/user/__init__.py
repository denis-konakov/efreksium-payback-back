from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=['user'])

from . import login
from . import profile
from . import register
from . import confirm_email
from . import send_reset_password_code
from . import confirm_reset_password
from . import create_avatar
from . import get

