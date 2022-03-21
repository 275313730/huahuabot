from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.rule import to_me
from ...database import db

sub_list = on_command(
    "关注列表", aliases={"主播列表"}, rule=to_me(), priority=2, block=True)
sub_list.__doc__ = """关注列表"""


@sub_list.handle()
async def _(event: MessageEvent):
    """发送当前位置的订阅列表"""

    message = handle_sub_list(event.user_id)
    await sub_list.finish(message)


def handle_sub_list(qq: int):
    message = "关注列表\n\n"
    subs = db.get_all()
    for sub in subs:
        if qq in sub[2]:
            message += (
                f"{sub[1]}（{sub[0]}）"
            )
    return message
