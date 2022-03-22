import json
from loguru import logger
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent
from nonebot.rule import to_me

from bilireq.user import get_user_info
from bilireq.exceptions import ResponseCodeError

from ..database import db

add_sub = on_command("关注", aliases={"添加主播"},
                     rule=to_me(), priority=2, block=True)
add_sub.__doc__ = """关注 UID"""


@add_sub.handle()
async def _(event: PrivateMessageEvent):
    """根据 UID 订阅 UP 主"""

    uid: int = 0
    args = str(event.get_message()).split(" ")
    if len(args) == 2:
        uid = int(args[1])
    if uid == 0:
        await add_sub.finish("请输入uid")
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

    result = handle_add_sub(uid, name, event.user_id)
    if result:
        await add_sub.finish(f"已关注 {name}（{uid}）")
    await add_sub.finish(f"{name}（{uid}）已经关注了")


def handle_add_sub(uid: int, name: str, qq: int) -> bool:
    result = False
    data = db.get_sub_list(uid)
    if len(data) == 0:
        db.add_up(uid, name)
        result = db.add_sub(uid, f'[{qq}]')
    else:
        sub_list_str: str = db.get_sub_list(uid)[0]
        sub_list: list = json.loads(sub_list_str)
        sub_list.append(qq)
        sub_list_str = json.dumps(sub_list)
        result = db.add_sub(uid, sub_list_str)
    return result
