from nonebot import on_command
from nonebot.adapters.onebot.v11 import PrivateMessageEvent

_help = on_command("help", aliases={"帮助"}, priority=1, block=True)


@_help.handle()
async def _(event: PrivateMessageEvent):
    await _help.finish(f"这里是滑滑bot，目前已有的功能如下"
                       f"\n（'help'可替换为'帮助‘）"
                       f"\n树洞：/help 树洞"
                       f"\nb站小帮手：/help bilibli，/help b站")
