from . import crud


def create_user(qq: int, nickname: str, time: str) -> bool:
    """创建用户"""

    script = fr"insert into user (qq,nickname,join_time,last_use_time,ban_end_time,favorite) values \
    ({qq},'{nickname}','{time}','{time}','{time}','[]')"
    return crud.write_data(script)


def get_all_users() -> list:
    """获取所有用户"""

    script = "select * from user"
    return crud.get_data(script)


def get_user(qq: int, option: str = "*") -> list:
    """获取用户信息"""

    script = fr"select {option} from user where qq = {qq}"
    return crud.get_data(script)


def get_user_by_nickname(nickname: str) -> list:
    """通过昵称获取用户"""
    script = fr"select * from user where nickname = {nickname}"
    return crud.get_data(script)


def update_user(qq: int, option: str, content: str) -> bool:
    """更新用户信息"""

    script = fr"update user set {option} = '{content}' where qq = {qq}"
    return crud.write_data(script)
