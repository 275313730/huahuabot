import json
from random import randint

from nonebot.adapters.onebot.v11 import unescape

from src.plugins.tree_hole.crud import crud
from . import utils


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

    nickname = crud.user.get_nickname(qq)
    if nickname:
        status = crud.note.create_note(qq, nickname, content)

    return status


def get_someone_notes(qq: int) -> str:
    """获取某人的小纸条"""

    note_str = ""
    notes = crud.note.get_notes_from(qq)
    if len(notes) > 0:
        note_str = utils.trans_notes_to_str(notes)
    return note_str


def get_random_note(qq: int) -> str:
    """随机获取一个小纸条"""

    note_str = ""
    notes = crud.note.get_others_notes(qq)
    random_index = randint(1, len(notes))
    index = 1
    for note in notes:
        if index == random_index:
            note_str = utils.trans_note_to_str(note)
        index += 1
    return note_str


def get_my_notes(qq: int) -> str:
    """获取我的小纸条"""

    notes = crud.note.get_notes_from(qq)

    if len(notes) > 0:
        notes_str = utils.trans_notes_to_str(notes)
    else:
        notes_str = ""
    return notes_str


def report_note(qq: int, uid: int, description: str) -> bool:
    """举报小纸条"""

    status = False
    notes = crud.note.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        report: list = json.loads(note[3])
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
        note_str = utils.trans_note_to_str(note)
    return note_str


def get_note_report_by_uid(uid: int) -> str:
    pass
