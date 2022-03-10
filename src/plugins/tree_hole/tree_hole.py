# -*- coding: utf-8 -*-
import json
import os
import sqlite3
from random import randint

from nonebot import logger

from . import crud


def check_qq_exist(qq: str) -> bool:
    exist = False

    users = crud.get_user(qq)
    if len(users) > 0:
        exist = True

    return exist


def join_tree_hole(qq: str, nickname: str) -> bool:
    """加入树洞"""

    return crud.create_user(qq, nickname)


def post_note(qq: str, content: str) -> bool:
    """投递小纸条"""
    status = False

    nickname = crud.get_nickname(qq)
    if nickname:
        status = crud.create_note(qq, nickname, content)

    return status


def get_someone_notes(qq: str) -> str:
    """获取某人的小纸条"""

    notes = crud.get_notes_from(qq)
    if len(notes) > 0:
        return trans_notes_to_str(notes)
    return ""


def get_random_note(qq: str) -> str:
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


def get_my_notes(qq: str) -> str:
    """获取我的小纸条"""

    notes = crud.get_notes_from(qq)

    if len(notes) > 0:
        notes_str = trans_notes_to_str(notes)
    else:
        notes_str = ""
    return notes_str


def trans_note_to_str(note: dict) -> str:
    return str(f"来自'{note[1]}'的小纸条(uid:{note[0]})："
               f"\n{note[2]}")


def trans_notes_to_str(notes: list) -> str:
    notes_str = ""
    for note in notes:
        notes_str += f"{trans_note_to_str(note)}\n\n"
    return notes_str


def report_note(uid: int, qq: str, nickname: str, content: str):
    notes = crud.get_note_by_uid(uid)
    if len(notes) > 0:
        note = notes[0]
        report: list = json.loads(note["report"])
        report.append(dict(qq=qq, nickname=nickname, content=content))
        report_str = json.dumps(report)
        note["report"] = report_str
        crud.update_note_report(uid, report_str)
    else:
        return False
