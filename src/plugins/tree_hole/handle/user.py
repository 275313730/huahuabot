import json
from nonebot.log import logger
from datetime import datetime
from .. import database as db


def trans_note_to_str(note: dict) -> str:
    """将小纸条dict转化为字符串"""

    nickname = db.user.get_user(note[1], "nickname")[0][0]
    return str(f"来自'{nickname}'的小纸条(编号:{note[0]})"
               f"\n投递时间：{note[3]}"
               f"\n小纸条内容：{note[2]}")


def trans_notes_to_str(notes: list) -> str:
    """将小纸条list转化为字符串"""

    notes_str = ""
    num = len(notes)
    for i in range(num):
        if i < num - 1:
            notes_str += f"{trans_note_to_str(notes[i])}\n\n"
        else:
            notes_str += f"{trans_note_to_str(notes[i])}"
    return notes_str


def join_tree_hole(qq: int, nickname: str) -> bool:
    """加入树洞"""

    stamp = datetime.now()
    logger.debug(stamp)
    time = stamp.strftime("%y/%m/%d")
    logger.debug(time)
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
        ban_end_time = datetime.strptime(user[0], '%y/%m/%d')
        days = (now - ban_end_time).days
        status = (days < 0)
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


def get_my_favorites(qq: int) -> str:
    data = db.user.get_user(qq, "favorites")
    if len(data) > 0:
        uid_list = json.loads(data[0][0])
        logger.debug(uid_list)
        favorites = []
        for uid in uid_list:
            favorites.append(db.note.get_note_by_uid(uid)[0])
        logger.debug(favorites)
        return trans_notes_to_str(favorites)
    return ""
