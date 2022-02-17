import nonebot
from nonebot import on_command, logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment

_help = on_command("help", aliases={"帮助"}, priority=1, block=True)


@_help.handle()
async def _(bot: Bot, event: Event):
    await _help.send(f"目前功能:\n/全部式神 or /所有式神：查看所有式神的名称"
                     f"\n/式神 xx：查看指定式神的卡牌（例如：/式神 不知火）"
                     f"\n/比赛日期 xx：设置比赛时间（注意每次设置会重置比赛信息）"
                     f"\n/参加比赛 xx or /报名比赛 xx or /报名参赛 xx：报名参加比赛"
                     f"\n/查看比赛：获取比赛信息")
