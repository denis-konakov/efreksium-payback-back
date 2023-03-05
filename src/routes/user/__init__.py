from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=['user'])

from . import login
from . import profile
from . import register
from . import confirm_email
from . import send_registration_confirm_code
from . import change_password
from . import get
