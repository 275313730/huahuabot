from datetime import datetime
from ..database import db


def join_tree_hole(qq: int, nickname: str) -> bool:
    """加入树洞"""

    stamp = datetime.now()
    time = stamp.strftime("%y/%m/%d")
    return db.user.create_user(qq, nickname, time)


def modify_nickname(qq: int, nickname: str) -> bool:
    """修改昵称"""

    return db.user.update_user(qq, "nickname", nickname)


def check_qq_exist(qq: int) -> bool:
    """查看qq号是否存在"""

    exist = False
    users = db.user.get_user(qq)
    if len(users) > 0:
        exist = True
    return exist


def check_nickname_exist(nickname: str) -> bool:
    """查看昵称是否存在"""

    exist = False
    users = db.user.get_user_by_nickname(nickname)
    if len(users) > 0:
        exist = True
    return exist


def check_qq_ban(qq: int) -> bool:
    """查看qq是否被封禁"""

    status = False
    now = datetime.now()
    users = db.user.get_user(qq, 'ban_end_time')
    if len(users) > 0:
        user = users[0]
        ban_end_time = datetime.strptime(user[0], '%Y/%m/%d')
        days = (now - ban_end_time).days
        status = (days <= 0)
    return status


def update_last_use_time(qq: int) -> bool:
    """更新用户最后使用时间"""

    stamp = datetime.now()
    last_use_time = stamp.strftime('%Y/%m/%d')
    status = db.user.update_user(qq, "last_use_time", last_use_time)
    return status


def get_qq_by_note(uid: int) -> int:
    """获取小纸条的所属用户"""

    qq = 0
    notes = db.note.get_note_by_uid(uid, "qq")
    if len(notes) > 0:
        note = notes[0]
        qq = int(note[0])
    return qq
