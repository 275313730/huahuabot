from typing import Dict, Any

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State

# from . import card_pre
from . import card_get
from . import image
from . import game_data

roles = on_command("全部式神", aliases={"所有式神"}, priority=2, block=True)


@roles.handle()
async def _(bot: Bot, event: Event):
    await roles.send(card_get.get_roles())


role_cards = on_command("式神", priority=2, block=True)


@role_cards.handle()
async def _(bot: Bot, event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        file_base64 = card_get.get_role_cards(args[1])
        if file_base64 == "":
            await role_cards.send("名字打错了！")
            pass
        else:
            await role_cards.send(MessageSegment(type="image", data={"file": file_base64}))
    else:
        await role_cards.send("式神名字呢？")


add_role = on_command("添加式神", rule=to_me(), priority=1, block=True)


@add_role.got("name", prompt="请输入式神名字")
@add_role.got("sex", prompt="请输入式神性别（不确定或无性别发送空消息即可）")
@add_role.got("keywords", prompt="请输入式神相关词条（用空格间隔开）")
@add_role.got("description", prompt="请输入式神本体描述")
async def _(bot: Bot, event: Event, state: T_State):
    role = {
        'name': str(state['name']),
        'sex': str(state['sex']),
        'keywords': str(state['keywords']),
        'descriptions': str(state['description'])
    }
    game_data.add_role(role)


modify_role = on_command("修改式神", rule=to_me(), priority=1, block=True)


@modify_role.got("name", prompt="请输入式神名字")
@modify_role.got("option", prompt="请问要修改哪一项（名字，性别，词条，描述）")
@modify_role.got("new_data", prompt="请输入修改内容")
async def _(bot: Bot, event: Event, state: T_State):
    options = {
        "名字": "name",
        "性别": "sex",
        "词条": "keywords",
        "描述": "description"
    }
    game_data.modify_role_data(str(state['name']), options[str(state["option"])], str(state["new_data"]))


added_roles = on_command("已有式神", rule=to_me(), priority=1, block=True)


@added_roles.handle()
async def _():
    await added_roles.send(game_data.get_all_roles_name())


check_role = on_command("查看式神", rule=to_me(), priority=1, block=True)


@check_role.handle()
async def _(event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        role_data = game_data.get_role_data(args[1])
        if role_data is not None:
            await check_role.send(f"名字：{role_data['name']}"
                                  f"\n性别：{role_data['sex']}"
                                  f"\n词条：{role_data['keywords']}"
                                  f"\n描述：{role_data['description']}")
        else :
            await check_role.send("式神不存在")
    else:
        await check_role.send("式神名字呢？")
