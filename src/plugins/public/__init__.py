import nonebot
from nonebot import on_command, logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment

from . import activity

_help = on_command("help", aliases={"帮助"}, priority=1, block=True)


@_help.handle()
async def _(bot: Bot, event: Event):
    await _help.send(f"目前功能:\n/全部式神 or /所有式神：查看所有式神的名称"
                     f"\n/式神 xx：查看指定式神的卡牌（例如：/式神 不知火）"
                     f"\n/比赛日期 xx：设置比赛时间（注意每次设置会重置比赛信息）"
                     f"\n/参加比赛 xx or /报名比赛 xx or /报名参赛 xx：报名参加比赛"
                     f"\n/查看比赛：获取比赛信息")


set_activity_day = on_command("比赛日期", priority=3, block=True)


@set_activity_day.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        activity.set_activity_day(args[1])
        await set_activity_day.send(f"比赛日期已经设定为{args[1]}（注意修改比赛日期会重置报名信息）")
    else:
        await set_activity_day.send("比赛日期呢？")


sign_up = on_command("参加比赛", aliases={"报名比赛，报名参赛"}, priority=3, block=True)


@sign_up.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        await sign_up.send(activity.sign_up(args[1]))
    else:
        await sign_up.send("虚空参赛是吧？")


check_activity_stats = on_command("查看比赛", priority=3, block=True)


@check_activity_stats.handle()
async def _(bot: Bot, event: Event):
    await check_activity_stats.send(activity.check_activity_stats())
