from . import user
from .. import crud

def ban_qq(qq: int, ban_end: str) -> bool:
    """禁用qq号"""
    exist = user.check_qq_exist(qq)
    if not exist:
        return False
    status = crud.user.update_user(qq, "ban_end", ban_end)
    return status
