import os
import sqlite3
from typing import Dict, List, Optional
from webbrowser import get

from nonebot import get_driver
from nonebot.log import logger
from tortoise.expressions import Q
from tortoise.queryset import QuerySet


uid_list = {"live": {"list": [], "index": 0},
            "dynamic": {"list": [], "index": 0}}

up_list = [{"uid": 0, "list": []}]


def get_database_path() -> str:
    return os.path.join(os.getcwd(), 'data/bilibili.db')


def write_data(script: str) -> bool:
    db_file = get_database_path()
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(script)
    cursor.close()
    conn.commit()
    conn.close()
    return True


def get_data(script: str) -> list:
    db_file = get_database_path()
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(script)
    data = list(cursor)
    cursor.close()
    conn.commit()
    conn.close()
    return data


def check_tables():
    db_file = get_database_path()
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(str('''CREATE TABLE if not exists "sub" (
	"uid"	INTEGER NOT NULL UNIQUE,
    "name"  text not null ,
	"sub_list"	TEXT NOT NULL DEFAULT '[]',
	PRIMARY KEY("uid"))'''))
    data = list(cursor)
    cursor.close()
    conn.commit()
    conn.close()
    return data


def add_up(uid: int):
    """添加up主"""

    script = fr"insert into sub uid values {uid}"
    return write_data(script)


def add_sub(uid: int, sub_list_str: str) -> bool:
    """添加订阅"""

    script = fr"update sub set sub_list = '{sub_list_str}' where uid = {uid}"
    return write_data(script)


def get_up_name(uid: int) -> list:
    """获取up昵称"""

    script = fr"select name from sub where uid = {uid}"
    return get_data(script)


def get_push_list(uid: int) -> list:
    """获取推送列表"""

    script = fr"select sub_list from sub where uid = {uid}"
    return get_data(script)


def delete_sub(uid: int, qq: int) -> bool:
    return True
