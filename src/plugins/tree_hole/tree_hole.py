# -*- coding: utf-8 -*-
import datetime
import json
from random import randint

from nonebot import logger
from nonebot.adapters.onebot.v11 import unescape

from . import crud


# 管理相关

def ban_qq(qq: int, ban_end: str) -> bool:
    """禁用qq号"""
    exist = check_qq_exist(qq)
    if not exist:
        return False
    status = crud.update_user(qq, "ban_end", ban_end)
    return status


# 用户相关

def join_tree_hole(qq: int, nickname: str) -> bool:
    """加入树洞"""

    stamp = datetime.datetime.now()
    time = stamp.strftime("%y/%m/%d")
    return crud.create_user(qq, nickname, time)


def check_qq_exist(qq: int) -> bool:
    """查看qq号是否存在"""

    exist = False
    users = crud.get_user(qq)
    if len(users) > 0:
        exist = True
    return exist


def update_last_use_time(qq: int) -> bool:
    """更新用户最后使用时间"""

    stamp = datetime.datetime.now()
    last_use = stamp.strftime('%Y/%m/%d')
    status = crud.update_user(qq, "last_use_time", last_use)
    return status


def get_qq_by_note(uid: int) -> str:
    """获取小纸条的所属用户"""

    qq = ""
    notes = crud.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        qq = note[1]
    return qq


# 小纸条相关

def check_note_exist(uid: int) -> bool:
    """查看指定编号的小纸条是否存在"""

    exist = False
    notes = crud.get_note_by_uid(uid)
    if len(notes) > 0:
        exist = True
    return exist


def post_note(qq: int, content: str) -> bool:
    """投递小纸条"""
    status = False

    nickname = crud.get_nickname(qq)
    if nickname:
        status = crud.create_note(qq, nickname, content)

    return status


def get_someone_notes(qq: int) -> str:
    """获取某人的小纸条"""

    note_str = ""
    notes = crud.get_notes_from(qq)
    if len(notes) > 0:
        note_str = trans_notes_to_str(notes)
    return note_str


def get_random_note(qq: int) -> str:
    """随机获取一个小纸条"""

    note_str = ""
    notes = crud.get_others_notes(qq)
    random_index = randint(1, len(notes))
    index = 1
    for note in notes:
        if index == random_index:
            note_str = trans_note_to_str(note)
        index += 1
    return note_str


def get_my_notes(qq: int) -> str:
    """获取我的小纸条"""

    notes = crud.get_notes_from(qq)

    if len(notes) > 0:
        notes_str = trans_notes_to_str(notes)
    else:
        notes_str = ""
    return notes_str


def report_note(qq: int, uid: int, description: str) -> bool:
    """举报小纸条"""

    status = False
    notes = crud.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        report: list = json.loads(note[3])
        report.append(dict(qq=qq, description=description))
        report_str = unescape(json.dumps(report))
        status = crud.update_note(uid, "report", report_str)
    return status


def delete_note(qq: int, uid: int) -> bool:
    """删除小纸条"""

    status = False
    notes = crud.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        if note[1] == qq:
            status = crud.delete_note(uid)
    return status


def get_note_by_uid(uid: int) -> str:
    """根据uid获取小纸条"""

    note_str = ""
    notes = crud.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        note_str = trans_note_to_str(note)
    return note_str


def get_note_report_by_uid(uid: int) -> str:
    pass


# 辅助功能

def trans_note_to_str(note: dict) -> str:
    """将小纸条dict转化为字符串"""

    nickname = crud.get_nickname(note[1])
    return str(f"来自'{nickname}'的小纸条(编号:{note[0]})："
               f"\n{note[2]}")


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
