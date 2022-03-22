from nonebot import on_command
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.rule import to_me

_help = on_command("help", aliases={"帮助"}, priority=2, block=True)


@_help.handle()
async def _(event: PrivateMessageEvent):
    await _help.finish(f"这里是滑滑bot，目前已有的功能如下"
                       f"\n（'help'可替换为'帮助‘）"
                       f"\n树洞：/help 树洞"
                       f"\nb站小帮手：/help bilibli，/help b站"
                       f"\nbot反馈：/反馈")


feedback = on_command("反馈", rule=to_me(), priority=2, block=True)


@feedback.got("description", prompt="请输入反馈内容")
async def _():
    pass
