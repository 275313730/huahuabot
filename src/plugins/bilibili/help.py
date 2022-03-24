from nonebot import on_command
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.rule import to_me

bili_help = on_command("help bilibili", aliases={
    "帮助 bilibili", "help b站", "帮助 b站"}, rule=to_me(), priority=2, block=True)


@bili_help.handle()
async def _(event: PrivateMessageEvent):
    await bili_help.finish(f"b站小帮手目前已有的功能如下"
                           f"\n（UID替换为up主的uid）"
                           f"\n/关注 UID"
                           f"\n/取关 UID"
                           f"\n/关注列表"
                           f"\n注：由于功能限制，目前每个人最多只能关注5位up主，后续可能会开放更多数量")
