import os
import sqlite3


def get_database_path() -> str:
    return os.path.join(os.getcwd(), 'data/tree_hole.db')


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
    cursor.execute(str('''CREATE TABLE if not exists "user" (
	"qq"	INTEGER NOT NULL UNIQUE,
	"nickname"	TEXT NOT NULL,
	"join_time"	TEXT NOT NULL,
	"last_use_time"	TEXT NOT NULL,
	"ban_end_time"	TEXT NOT NULL,
	"favorites"	TEXT NOT NULL DEFAULT '[]',
	"read"	TEXT NOT NULL DEFAULT '[]',
	PRIMARY KEY("qq"))'''))
    cursor.execute(str('''CREATE TABLE if not exists "note" (
	"uid"	INTEGER NOT NULL UNIQUE,
	"qq"	INTEGER NOT NULL,
	"content"	TEXT NOT NULL,
	"post_time"	TEXT NOT NULL,
	"reports"	TEXT NOT NULL DEFAULT '[]',
	"visible"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("uid" AUTOINCREMENT))'''))
    data = list(cursor)
    cursor.close()
    conn.commit()
    conn.close()
    return data


check_tables()
