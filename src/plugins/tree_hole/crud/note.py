from . import crud


def create_note(qq: int, content: str) -> bool:
    """创建小纸条"""

    script = fr"insert into note (qq,content,report) values ({qq},'{content}','[]')"

    return crud.write_data(script)


def get_notes_from(qq: int) -> list:
    """获取指定用户的全部小纸条"""

    script = fr"select * from note where qq = {qq}"
    return crud.get_data(script)


def get_others_notes(qq: int) -> list:
    """获取除指定用户外的全部小纸条"""

    script = fr"select * from note where qq != {qq}"
    return crud.get_data(script)


def get_note_by_uid(uid: int) -> list:
    """通过uid获取小纸条"""

    script = fr"select * from note where uid = '{uid}'"
    return crud.get_data(script)


def update_note(uid: int, option: str, content: str) -> bool:
    """更新小纸条"""

    script = fr"update note set {option} = '{content}' where uid = {uid}"
    return crud.write_data(script)


def delete_note(uid: int) -> bool:
    """删除小纸条"""

    script = fr"delete from note where uid = {uid}"
    return crud.write_data(script)
