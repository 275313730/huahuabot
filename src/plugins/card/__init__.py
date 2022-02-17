import nonebot
from nonebot import on_command, logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment

# from . import card_pre
from . import card_get
from . import image
from . import crew_battle

roles = on_command("全部式神", aliases={"所有式神"}, priority=2, block=True)

role_cards = on_command("式神", priority=2, block=True)

set_battle_day = on_command("比赛日期", priority=3, block=True)

sign_up = on_command("参加比赛", aliases={"报名比赛，报名参赛"}, priority=3, block=True)

check_battle_stats = on_command("查看比赛", priority=3, block=True)


@roles.handle()
async def _(bot: Bot, event: Event):
    await roles.send(message=card_get.get_roles())


@role_cards.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        file_base64 = card_get.get_role_cards(args[1])
        if file_base64 == "":
            return await role_cards.send("名字打错了，记得/要改成-，例如：鬼使黑-鬼使白")
        else:
            await role_cards.send(MessageSegment(type="image", data={"file": file_base64}))
    else:
        await role_cards.send("式神名字呢？")


@set_battle_day.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        crew_battle.set_battle_day(args[1])
        await set_battle_day.send(f"比赛日期已经设定为{args[1]}（注意修改比赛日期会重置报名信息）")
    else:
        await set_battle_day.send("比赛日期呢？")


@sign_up.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        await sign_up.send(crew_battle.sign_up(args[1]))
    else:
        await sign_up.send("虚空参赛是吧？")


@check_battle_stats.handle()
async def _(bot: Bot, event: Event):
    await check_battle_stats.send(crew_battle.check_battle_stats())
