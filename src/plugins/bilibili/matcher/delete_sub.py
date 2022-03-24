import json
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.log import logger

from ..database import db

delete_sub = on_command(
    "取关", aliases={"删除主播"}, rule=to_me(), priority=2, block=True)
delete_sub.__doc__ = """取关 UID"""


@delete_sub.handle()
async def _(event: MessageEvent, state: T_State):
    """根据 UID 删除 UP 主订阅"""

    uid: int = -1

    args = str(event.get_message()).split(" ")
    if len(args) == 2:
        arg = args[1]
        if arg.isdigit():
            uid = int(arg)
        else:
            await delete_sub.finish("请不要输入无关内容噢")
    else:
        await delete_sub.finish("是不是忘了输入uid捏")

    name = db.get_up_name(uid)
    if name != "":
        result = handle_delete_sub(uid, event.user_id)

        if result:
            await delete_sub.finish(f"已取关 {name}（{uid}）")
        await delete_sub.finish(f"UID（{uid}）未关注")
    else:
        await delete_sub.finish("UID不存在")


def handle_delete_sub(uid: int, qq: int):
    sub_list = db.get_sub_list(uid)
    result = False
    if len(sub_list) > 0:
        sub_list.remove(qq)
        result = db.modify_sub(uid, json.dumps(sub_list))
    return result
