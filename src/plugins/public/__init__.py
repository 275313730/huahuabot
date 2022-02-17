import nonebot
from nonebot import on_command, logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment

_help = on_command("help", aliases={"帮助"}, priority=1, block=True)


@_help.handle()
async def _(bot: Bot, event: Event):
    await _help.send("目前功能:\n/全部式神or/所有式神：查看所有式神的名称\n/式神 xx：查看指定式神的卡牌（例如：/式神 不知火）")
