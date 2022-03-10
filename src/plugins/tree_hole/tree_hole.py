# -*- coding: utf-8 -*-

import os
import sqlite3
from random import randint

from nonebot import logger


def empty_db() -> bool:
    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(r"DELETE FROM sqlite_sequence WHERE name = ‘note’")
    cursor.close()
    conn.commit()
    conn.close()
    return True


def check_qq_exist(qq: str) -> bool:
    exist = False

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select * from user")
    for row in cursor:
        if qq == row[0]:
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


def get_random_note(qq: str) -> dict:
    note = dict(nickname="", contnet="")

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    rows = cursor.execute("SELECT COUNT(*) FROM table_name").fetchone()[0]
    random_index = randint(1, rows)
    index = 1
    cursor.execute(fr"select uid,nickname,content from note where qq != '{qq}'")
    for row in cursor:
        if index == random_index:
            note['uid'] = row[0]
            note['nickname'] = row[1]
            note['content'] = row[2]
            break
        index += 1
    cursor.close()
    conn.commit()

    conn.close()
    return note


def get_my_notes(qq: str) -> str:
    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select uid,nickname,content from note where qq = '{qq}'")
    notes_str = trans_notes_to_str(list(cursor))
    cursor.close()
    conn.commit()
    return notes_str


def trans_note_to_str(note: dict) -> str:
    return str(f"来自'{note[1]}'的小纸条(uid:{note[0]})："
               f"\n{note[2]}")


def trans_notes_to_str(notes: list) -> str:
    notes_str = ""
    for note in notes:
        notes_str += f"{trans_note_to_str(note)}\n\n"
    return notes_str
