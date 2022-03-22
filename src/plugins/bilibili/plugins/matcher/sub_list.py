import json
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.rule import to_me
<<<<<<< HEAD:src/plugins/bilibili/matcher/sub_list.py

from ..database import db
=======
from ...database import db
>>>>>>> d2a5994fd68b6daf811e09f5962fb772e155d4ea:src/plugins/bilibili/plugins/matcher/sub_list.py

sub_list = on_command(
    "关注列表", aliases={"主播列表"}, rule=to_me(), priority=2, block=True)
sub_list.__doc__ = """关注列表"""


@sub_list.handle()
async def _(event: MessageEvent):
    """发送当前位置的订阅列表"""

    message = handle_sub_list(event.user_id)
    await sub_list.finish(message)


<<<<<<< HEAD:src/plugins/bilibili/matcher/sub_list.py
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
=======
def handle_sub_list(qq: int):
    message = "关注列表\n\n"
    subs = db.get_all()
    for sub in subs:
        if qq in sub[2]:
            message += (
                f"{sub[1]}（{sub[0]}）"
>>>>>>> d2a5994fd68b6daf811e09f5962fb772e155d4ea:src/plugins/bilibili/plugins/matcher/sub_list.py
            )
    return message
