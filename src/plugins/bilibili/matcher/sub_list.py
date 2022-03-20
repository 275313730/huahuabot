from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from ..database import DB
from ..utils import get_type_id, to_me

sub_list = on_command(
    "关注列表", aliases={"主播列表"}, rule=to_me(), priority=2, block=True)
sub_list.__doc__ = """关注列表"""


@sub_list.handle()
async def _(event: MessageEvent):
    """发送当前位置的订阅列表"""

    message = "关注列表\n\n"
    async with DB() as db:
        subs = await db.get_sub_list(event.message_type, get_type_id(event))
        for sub in subs:
            user = await db.get_user(sub.uid)
            assert user is not None
            message += (
                f"{user.name}（{user.uid}）"
            )
    await sub_list.finish(message)
