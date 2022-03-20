from . import db


def create_note(qq: int, content: str, time: str) -> bool:
    """创建小纸条"""

    script = fr"insert into note (qq,content,post_time) values ({qq},'{content}','{time}')"
    return db.write_data(script)


def get_notes_from(qq: int, options: str = '*') -> list:
    """获取指定用户的全部小纸条"""

    script = fr"select {options} from note where qq = {qq}"
    return db.get_data(script)


def get_others_notes(qq: int, options: str = '*', expect: list = []) -> list:
    """获取除指定用户外的全部小纸条"""

    script = fr"select {options} from note where qq != {qq} and visible != 0"

    for uid in expect:
        script += fr" and uid != {uid}"

    return db.get_data(script)


def get_note_by_uid(uid: int, options: str = "*") -> list:
    """通过uid获取小纸条"""

    script = fr"select {options} from note where uid = '{uid}'"
    return db.get_data(script)


def update_note(uid: int, option: str, content: str) -> bool:
    """更新小纸条"""

    script = fr"update note set {option} = '{content}' where uid = {uid}"
    return db.write_data(script)


def delete_note(uid: int) -> bool:
    """删除小纸条"""

    script = fr"update note set visible = 0 where uid = {uid}"
    return db.write_data(script)
