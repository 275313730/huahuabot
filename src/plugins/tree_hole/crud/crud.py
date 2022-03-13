import os
import sqlite3


def get_database_path() -> str:
    return os.path.join(os.getcwd(), 'src/plugins/tree_hole/database/tree_hole.db')


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
