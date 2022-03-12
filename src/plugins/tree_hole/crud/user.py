import os
import sqlite3


def create_user(qq: int, nickname: str, time: str) -> bool:
    """创建用户"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        fr"insert into user (qq,nickname,join_time,last_use_time,ban_end_time,favorite) values ({qq},'{nickname}','{time}','{time}','{time}','[]')")
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


def get_user(qq: int, option: str = "*") -> list:
    """获取用户信息"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"select {option} from user where qq = {qq}")
    user = list(cursor)
    cursor.close()
    conn.commit()
    conn.close()

    return user


def update_user(qq: int, option: str, content: str) -> bool:
    """更新用户信息"""

    db_file = os.path.join(os.path.dirname(__file__), 'tree_hole.db')
    # 初始数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(fr"update user set {option} = '{content}' where qq = {qq}")
    cursor.close()
    conn.commit()
    conn.close()

    return True

