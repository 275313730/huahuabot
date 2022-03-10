import os
import sqlite3


def get_notes_from(qq: str) -> list:
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


def create_note(qq: str, content: str) -> bool:
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
