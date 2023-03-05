from utils import throws
from fastapi import Request
from typing import Callable
@throws
def get_confirm_link(request: Request):
    def wraps(code: str) -> str:
        return request.url_for('confirm_email', code=code)
    return wraps

get_confirm_link_type = Callable[[str], str]

