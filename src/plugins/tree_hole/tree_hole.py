# -*- coding: utf-8 -*-

import os
import sqlite3
from random import randint

from nonebot import logger


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
    cursor.execute(fr"select nickname,content from note where qq != '{qq}'")
    rows = -cursor.rowcount
    if rows > 0:
        random_index = randint(1, rows)
        index = 1
        for row in cursor:
            if index == random_index:
                note['nickname'] = row[0]
                note['content'] = row[1]
                break
            index += 1
    cursor.close()
    conn.commit()
    conn.close()
    return note
