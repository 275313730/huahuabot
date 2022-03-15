import json
from datetime import datetime
from random import randint
from nonebot.adapters.onebot.v11 import unescape
from .. import crud


def trans_note_to_str(note: dict) -> str:
    """将小纸条dict转化为字符串"""

    nickname = crud.user.get_user(note[1], "nickname")[0][0]
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


def check_note_exist(uid: int) -> bool:
    """查看指定编号的小纸条是否存在"""

    exist = False
    notes = crud.note.get_note_by_uid(uid)
    if len(notes) > 0:
        exist = True
    return exist


def post_note(qq: int, content: str) -> bool:
    """投递小纸条"""
    status = False

    nickname = crud.user.get_user(qq, "nickname")[0][0]
    if nickname:
        stamp = datetime.now()
        time = stamp.strftime("%y/%m/%d")
        status = crud.note.create_note(qq, content, time)

    return status


def get_someone_notes(qq: int) -> str:
    """获取某人的小纸条"""

    note_str = ""
    notes = crud.note.get_notes_from(qq)
    if len(notes) > 0:
        note_str = trans_notes_to_str(notes)
    return note_str


def get_random_note(qq: int) -> str:
    """随机获取一个小纸条"""

    note_str = ""
    notes = crud.note.get_others_notes(qq)
    random_index = randint(1, len(notes))
    index = 1
    for note in notes:
        if index == random_index:
            note_str = trans_note_to_str(note)
        index += 1
    return note_str


def get_my_notes(qq: int) -> str:
    """获取我的小纸条"""

    notes = crud.note.get_notes_from(qq)

    if len(notes) > 0:
        notes_str = trans_notes_to_str(notes)
    else:
        notes_str = ""
    return notes_str


def report_note(qq: int, uid: int, description: str) -> bool:
    """举报小纸条"""

    status = False
    notes = crud.note.get_note_by_uid(uid, "report")
    if len(notes) > 0:
        note = notes[0]
        report: list = json.loads(note[0])
        report.append(dict(qq=qq, description=description))
        report_str = unescape(json.dumps(report))
        status = crud.note.update_note(uid, "report", report_str)
    return status


def delete_note(qq: int, uid: int) -> bool:
    """删除小纸条"""

    status = False
    notes = crud.note.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        if note[1] == qq:
            status = crud.note.delete_note(uid)
    return status


def get_note_by_uid(uid: int) -> str:
    """根据uid获取小纸条"""

    note_str = ""
    notes = crud.note.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        note_str = trans_note_to_str(note)
    return note_str


def get_note_report_by_uid(uid: int) -> str:
    pass


def add_note_to_favorites(qq: int, uid: int) -> bool:
    status = False

    if not check_note_exist(uid):
        return status

    users = crud.user.get_user(qq, 'favorites')
    if len(users) > 0:
        user = users[0]
        favorites: list = json.loads(user[0])
        if uid in favorites:
            return status
        favorites.append(uid)
        status = crud.user.update_user(qq, 'favorites', json.dumps(favorites))
    return status


def remove_note_from_favorites(qq: int, uid: int) -> bool:
    status = False

    if not check_note_exist(uid):
        return status

    users = crud.user.get_user(qq, 'favorites')
    if len(users) > 0:
        user = users[0]
        favorites: list = json.loads(user[0])
        if uid in favorites:
            favorites.append(uid)
            status = crud.user.update_user(qq, 'favorites', json.dumps(favorites))
    return status
