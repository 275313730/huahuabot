import json
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.typing import T_State
from nonebot.rule import to_me

from ..database import db

delete_sub = on_command(
    "取关", aliases={"删除主播"}, rule=to_me(), priority=2, block=True)
delete_sub.__doc__ = """取关 UID"""


@delete_sub.got("uid", prompt="请输入要取关的UID")
async def _(event: MessageEvent, state: T_State):
    """根据 UID 删除 UP 主订阅"""

    uid = int(str(state["uid"]))
    up_name = db.get_up_name(uid)
    if not up_name:
        await delete_sub.finish("主播不存在")

    result = handle_delete_sub(uid, event.user_id)

    if result:
        await delete_sub.finish(f"已取关 {up_name}（{uid}）")
    await delete_sub.finish(f"UID（{uid}）未关注")


def handle_delete_sub(uid: int, qq: int):
    data = db.get_sub_list(uid)
    result = False
    if len(data) > 0:
        push_list_str = data[0]
        push_list: list = json.loads(push_list_str)
        push_list.remove(qq)
        result = db.add_sub(uid, json.dumps(push_list))
    return result
