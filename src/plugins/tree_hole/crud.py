import os
import sqlite3

from nonebot import logger


def empty_db() -> bool:
    """清空数据库"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(r"DELETE FROM sqlite_sequence WHERE name = ‘note’")
    cursor.close()
    conn.commit()
    conn.close()
    return True


def create_user(qq: str, nickname: str) -> bool:
    """创建用户"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"insert into user values ('{qq}','{nickname}')")
    cursor.close()
    conn.commit()
    conn.close()
    return True


def get_all_users() -> list:
    """获取所有用户"""

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


def get_notes_from(qq: str) -> list:
    """获取指定用户的全部小纸条"""

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
    """获取除指定用户外的全部小纸条"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select uid,nickname,content from note where qq != '{qq}'")
    notes = list(cursor)
    cursor.close()
    conn.commit()
    return notes


def get_nickname(qq: str) -> str:
    """获取指定用户的昵称"""

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


def create_note(qq: str, nickname: str, content: str) -> bool:
    """创建小纸条"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    status = False
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    if nickname:
        cursor.execute(fr"insert into note (qq,nickname,content) values ('{qq}','{nickname}','{content}')")
        status = True
    cursor.close()
    conn.commit()
    conn.close()
    return status


def get_user(qq: str) -> list:
    """获取用户信息"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select * from user where qq = '{qq}'")
    user = list(cursor)
    cursor.close()
    conn.commit()
    conn.close()

    return user


def get_note_by_uid(uid: int) -> list:
    """通过uid获取小纸条"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select * from note where uid = '{uid}'")
    note = list(cursor)
    cursor.close()
    conn.commit()
    conn.close()

    return note


def update_note(uid: int, option: str, content: str) -> bool:
    """更新小纸条内容"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"update note set {option} = '{content}' where uid = {uid}")
    cursor.close()
    conn.commit()
    conn.close()

    return True
