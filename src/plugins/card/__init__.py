import nonebot
from nonebot import on_command, logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment

# from . import card_pre
from . import card_get
from . import image

roles = on_command("全部式神", aliases={"所有式神"}, priority=2, block=True)

role_cards = on_command("式神", priority=2, block=True)


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
