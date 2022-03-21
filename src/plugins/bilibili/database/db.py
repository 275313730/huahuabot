import os
import sqlite3

up_list: list = []

index = 0


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
    cursor.close()
    conn.commit()
    conn.close()


def next_uid() -> int:
    global index
    global up_list
    if len(up_list) == 0:
        return 0

    if index+1 > len(up_list):
        index = 0
    uid = up_list[index]['uid']
    index += 1
    return uid


def update_up_list():
    if len(get_all()) == 0:
        return
    global up_list
    up_list = get_data("select (uid,sub_list) from sub")


def add_up(uid: int, name: str):
    """添加up主"""

    script = fr"insert into sub (uid,name) values ({uid},'{name}')"
    return write_data(script)


def add_sub(uid: int, sub_list_str: str) -> bool:
    """添加订阅"""

    script = fr"update sub set sub_list = '{sub_list_str}' where uid = {uid}"
    return write_data(script)


def get_up_name(uid: int) -> list:
    """获取up昵称"""

    script = fr"select name from sub where uid = {uid}"
    return get_data(script)


def get_sub_list(uid: int) -> list:
    """获取推送列表"""

    script = fr"select (sub_list) from sub where uid = {uid}"
    return get_data(script)


def delete_sub(uid: int, qq: int) -> bool:
    return True


def get_uid_list() -> list:
    return get_data("select uid from sub")


def update_user(uid: int, name: str):
    write_data(fr"update sub set name = '{name}' where uid = {uid}")


def get_all() -> list:
    return get_data(fr"select * from sub")
