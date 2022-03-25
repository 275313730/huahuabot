import json
from datetime import datetime
from random import randint

from nonebot.adapters.onebot.v11 import unescape
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


def check_note_exist(uid: int) -> bool:
    """查看指定编号的小纸条是否存在"""

    exist = False
    notes = db.note.get_note_by_uid(uid)
    if len(notes) > 0:
        exist = True
    return exist


def check_note_visible(uid: int) -> bool:
    """查看指定编号的小纸条是否被删除"""

    visible = True
    notes = db.note.get_note_by_uid(uid, "visible")
    if len(notes) > 0:
        note = notes[0]
        visible = (note[0] == 1)
    return visible


def post_note(qq: int, content: str) -> bool:
    """投递小纸条"""
    status = False

    nickname = db.user.get_user(qq, "nickname")[0][0]
    if nickname:
        stamp = datetime.now()
        time = stamp.strftime("%y/%m/%d")
        status = db.note.create_note(qq, content, time)

    return status


def get_someone_notes(qq: int) -> str:
    """获取某人的小纸条"""

    note_str = ""
    notes = db.note.get_notes_from(qq, "uid,qq,content,post_time")
    if len(notes) > 0:
        note_str = trans_notes_to_str(notes)
    return note_str


def get_random_note(qq: int) -> str:
    """随机获取一个小纸条"""

    read: list = []

    note_str = ""
    users = db.user.get_user(qq, "read")

    if len(users) > 0:
        user = users[0]
        read: list = json.loads(user[0])

    notes = db.note.get_others_notes(qq, "uid,qq,content,post_time", read)
    if len(notes) == 0:
        note_str = "暂无新的小纸条"
    else:
        random_index = randint(1, len(notes))
        index = 1
        for note in notes:
            if index == random_index:
                read.append(note[0])
                read_str = json.dumps(read)
                db.user.update_user(qq, "read", read_str)
                note_str = trans_note_to_str(note)
            index += 1
    return note_str


def get_my_notes(qq: int) -> str:
    """获取我的小纸条"""

    notes = db.note.get_notes_from(qq)

    if len(notes) > 0:
        notes_str = trans_notes_to_str(notes)
    else:
        notes_str = ""
    return notes_str


def report_note(qq: int, uid: int, description: str) -> bool:
    """举报小纸条"""

    status = False
    notes = db.note.get_note_by_uid(uid, "report")
    if len(notes) > 0:
        note = notes[0]
        report: list = json.loads(note[0])
        report.append(dict(qq=qq, description=description))
        report_str = unescape(json.dumps(report))
        status = db.note.update_note(uid, "report", report_str)
    return status


def delete_note(qq: int, uid: int) -> bool:
    """删除小纸条"""

    status = False
    notes = db.note.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        if note[1] == qq:
            status = db.note.delete_note(uid)
    return status


def get_note_by_uid(uid: int) -> str:
    """根据uid获取小纸条"""

    note_str = ""
    notes = db.note.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        note_str = trans_note_to_str(note)
    return note_str


def get_note_reports_by_uid(uid: int) -> str:
    reports_str = ""

    notes = db.note.get_note_by_uid(uid, "reports")
    reports_str += get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        reports: list = json.loads(note[0])
        for report in reports:
            reports_str += str(f"\n————————————"
                               f"\n举报人qq：{report['qq']}"
                               f"\n举报描述：{report['description']}")
    else:
        reports_str += "\n\n暂无举报"
    return reports_str


def add_note_to_favorites(qq: int, uid: int) -> str:
    status = False

    if not check_note_exist(uid):
        return "小纸条不存在"

    users = db.user.get_user(qq, 'favorites')
    if len(users) > 0:
        user = users[0]
        favorites: list = json.loads(user[0])
        if uid in favorites:
            return "已经收藏过了"
        favorites.append(uid)
        status = db.user.update_user(qq, 'favorites', json.dumps(favorites))
        if status:
            return "收藏成功"
    return "收藏失败，原因未知，请向开发者反馈"


def remove_note_from_favorites(qq: int, uid: int) -> bool:
    status = False

    if not check_note_exist(uid):
        return status

    users = db.user.get_user(qq, 'favorites')
    if len(users) > 0:
        user = users[0]
        favorites: list = json.loads(user[0])
        if uid in favorites:
            favorites.remove(uid)
            status = db.user.update_user(
                qq, 'favorites', json.dumps(favorites))
    return status
