import json
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent
from nonebot.typing import T_State
from nonebot.rule import to_me

from bilireq.user import get_user_info
from bilireq.exceptions import ResponseCodeError

from ..database import db

add_sub = on_command("关注", aliases={"添加主播"},
                     rule=to_me(), priority=2, block=True)
add_sub.__doc__ = """关注 UID"""


@add_sub.got("uid", prompt="请输入要关注的UID")
async def _(event: PrivateMessageEvent, state: T_State):
    """根据 UID 订阅 UP 主"""

    uid = state["uid"]
    name = db.get_up_name(uid)
    if not name:
        try:
            name = (await get_user_info(uid, reqtype="web"))['name']
        except ResponseCodeError as e:
            if e.code == -400 or e.code == -404:
                await add_sub.finish("UID不存在，注意UID不是房间号")
            elif e.code == -412:
                await add_sub.finish("操作过于频繁IP暂时被风控，请半小时后再尝试")
            else:
                await add_sub.finish(
                    f"未知错误，请联系开发者反馈，错误内容：\n\
                                    {str(e)}"
                )

    data = db.get_push_list(uid, "dynamic")
    result = False
    if len(data) > 0:
        push_list_str = data[0]
        push_list: list = json.loads(push_list_str)
        push_list.append(event.user_id)
        result = db.add_sub(uid, json.dumps(push_list))
    if result:
        await add_sub.finish(f"已关注 {name}（{uid}）")
    await add_sub.finish(f"{name}（{uid}）已经关注了")
