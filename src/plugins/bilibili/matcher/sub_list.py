import json
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.rule import to_me

from ..database import db

sub_list = on_command(
    "关注列表", aliases={"主播列表"}, rule=to_me(), priority=2, block=True)
sub_list.__doc__ = """关注列表"""


@sub_list.handle()
async def _(event: MessageEvent):
    """发送当前位置的订阅列表"""

    message = handle_sub_list(event.user_id)
    await sub_list.finish(message)


def handle_sub_list(qq: int) -> str:
    data = db.get_all()

    message = "关注列表\n\n"
    for up in data:
        uid = up[0]
        name = up[1]
        _sub_list = json.loads(up[2])
        if qq in _sub_list:
            message += (
                f"{name}（{uid}）"
            )
    return message
