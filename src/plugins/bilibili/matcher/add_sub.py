import json
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent
from nonebot.rule import to_me
from nonebot.log import logger

from bilibili_api.user import User
from bilibili_api.exceptions import ResponseCodeException

from ..database import db

add_sub = on_command("关注", aliases={"添加主播"},
                     rule=to_me(), priority=2, block=True)
add_sub.__doc__ = """关注 UID"""


@add_sub.handle()
async def _(event: PrivateMessageEvent):
    """根据UID订阅UP主"""

    if user_sub_num(event.user_id) >= 5:
        await add_sub.finish("关注up数量已达到最大值请先取关主播或等数量开放")

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

    name = db.get_up_name(uid)

    if name == "":
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


def user_sub_num(user_id: int) -> int:
    num = 0

    up_list = db.get_all()
    if len(up_list) > 0:
        for up in up_list:
            sub_list = up[2]
            if sub_list.find(str(user_id)) > -1:
                num += 1
    return num


def handle_add_sub(uid: int, name: str, qq: int) -> bool:
    sub_list = db.get_sub_list(uid)
    if len(sub_list) == 0:
        db.add_up(uid, name)
        return db.modify_sub(uid, f'[{qq}]')
    else:
        if qq in sub_list:
            return False
        sub_list.append(qq)
        return db.modify_sub(uid, json.dumps(sub_list))
