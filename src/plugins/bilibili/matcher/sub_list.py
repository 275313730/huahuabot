import json
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.rule import to_me

from ...config import BILIBILI_PRIORITY
from ..database import db

sub_list = on_command(
    "关注列表", aliases={"主播列表"}, rule=to_me(), priority=BILIBILI_PRIORITY, block=True)
sub_list.__doc__ = """关注列表"""


@sub_list.handle()
async def _(event: MessageEvent):
    """发送当前位置的订阅列表"""

    data = db.get_all()

    message = "关注列表:"
    for up in data:
        uid = up[0]
        name = up[1]
        _sub_list = json.loads(up[2])
        if event.user_id in _sub_list:
            message += (
                f"\n{name}（{uid}）"
            )
    await sub_list.finish(message)
