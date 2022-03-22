import json
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent
from nonebot.rule import to_me

from bilibili_api.user import User
from bilibili_api.exceptions import ResponseCodeException

from ..database import db

add_sub = on_command("关注", aliases={"添加主播"},
                     rule=to_me(), priority=2, block=True)
add_sub.__doc__ = """关注 UID"""


@add_sub.handle()
async def _(event: PrivateMessageEvent):
    """根据UID订阅UP主"""

    uid: int = -1
    name: str = ""

    args = str(event.get_message()).split(" ")
    if len(args) == 2:
        arg = args[1]
        if arg.isdigit():
            uid = int(arg)
        else:
            await add_sub.finish("请不要输入无关内容噢")
    else:
        await add_sub.finish("是不是忘了输入uid捏")

    data = db.get_up_name(uid)
    if len(data) > 0:
        name = data[0][0]

    if not name:
        try:
            user = User(uid)
            res = await user.get_user_info()

            if not res:
                return

            name = res['name']
        except ResponseCodeException as e:
            if e.code == -400 or e.code == -404:
                await add_sub.finish("UID不存在")
            elif e.code == -412:
                await add_sub.finish("操作过于频繁IP暂时被风控，请半小时后再尝试")
            else:
                await add_sub.finish(
                    f"未知错误，请联系开发者反馈，错误内容：\n\
                                    {str(e)}"
                )

    result = handle_add_sub(uid, name, event.user_id)
    if result:
        await add_sub.finish(f"已关注 {name}（{uid}）")
    await add_sub.finish(f"{name}（{uid}）已经关注了")


def handle_add_sub(uid: int, name: str, qq: int) -> bool:
    result = False
    data = db.get_sub_list(uid)
    if len(data) == 0:
        db.add_up(uid, name)
        result = db.modify_sub(uid, f'[{qq}]')
    else:
        data = db.get_sub_list(uid)
        sub_list_str: str = db.get_sub_list(uid)[0][0]
        sub_list: list = json.loads(sub_list_str)
        sub_list.append(qq)
        sub_list_str = json.dumps(sub_list)
        result = db.modify_sub(uid, sub_list_str)
    return result
