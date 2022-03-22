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

    data = db.get_up_name(uid)
    if len(data) > 0:
        name = data[0][0]
        result = handle_delete_sub(uid, event.user_id)

        if result:
            await delete_sub.finish(f"已取关 {name}（{uid}）")
        await delete_sub.finish(f"UID（{uid}）未关注")
    else:
        await delete_sub.finish("UID不存在")


def handle_delete_sub(uid: int, qq: int):
    data = db.get_sub_list(uid)
    logger.debug(data)
    result = False
    if len(data) > 0:
        push_list_str = data[0][0]
        push_list: list = json.loads(push_list_str)
        push_list.remove(qq)
        result = db.modify_sub(uid, json.dumps(push_list))
    return result
