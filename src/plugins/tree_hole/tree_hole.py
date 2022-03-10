# -*- coding: utf-8 -*-

import os
import sqlite3
from random import randint

from nonebot import logger


def empty_db() -> bool:
    """清空小纸条"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(r"DELETE FROM sqlite_sequence WHERE name = ‘note’")
    cursor.close()
    conn.commit()
    conn.close()
    return True


def get_all_users() -> list:
    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select * from user")
    users = list(cursor)
    cursor.close()
    conn.commit()
    conn.close()
    return users


def check_qq_exist(qq: str) -> bool:
    exist = ""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select * from user where qq = '{qq}'")
    if len(list(cursor)) > 0:
        exist = True
    cursor.close()
    conn.commit()
    conn.close()

    return exist


def get_nickname(qq: str) -> str:
    nickname = ""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select * from user where qq = '{qq}'")
    for row in cursor:
        nickname = row[1]
    cursor.close()
    conn.commit()
    conn.close()

    return nickname


def add_user(qq: str, nickname: str) -> bool:
    """加入树洞"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"insert into user values ('{qq}','{nickname}')")
    cursor.close()
    conn.commit()
    conn.close()
    return True


def add_note(qq: str, content: str) -> bool:
    """投递小纸条"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    status = False
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    nickname = get_nickname(qq)
    if nickname:
        cursor.execute(fr"insert into note (qq,nickname,content) values ('{qq}','{nickname}','{content}')")
        status = True
    cursor.close()
    conn.commit()
    conn.close()
    return status


def get_someone_notes(qq: str) -> list:
    """获取某个人的小纸条"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select uid,nickname,content from note where qq = '{qq}'")
    notes = list(cursor)
    cursor.close()
    conn.commit()
    return notes


def get_others_notes(qq: str) -> list:
    """获取别人的小纸条"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select uid,nickname,content from note where qq != '{qq}'")
    notes = list(cursor)
    cursor.close()
    conn.commit()
    return notes


def get_random_note(qq: str) -> str:
    """随机获取一个小纸条"""

    note_str = ""
    notes = get_others_notes(qq)
    random_index = randint(1, len(notes))
    index = 1
    for note in notes:
        if index == random_index:
            note_str = trans_note_to_str(note)
        index += 1
    return note_str


def get_my_notes(qq: str) -> str:
    """获取我的小纸条"""

    notes = get_someone_notes(qq)

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
