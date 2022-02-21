# coding: UTF-8

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State

# from . import card_pre
from . import card_get
from . import game_data
from . import image
from .game_data import Role, Card

roles = on_command("全部式神", aliases={"所有式神"}, priority=2, block=True)


@roles.handle()
async def _():
    await roles.send(card_get.get_roles())


role_cards = on_command("式神", priority=2, block=True)


@role_cards.handle()
async def _(event: Event):
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


# 以下为数据管理功能

added_roles = on_command("已有式神", priority=1, block=True)


@added_roles.handle()
async def _(event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        await added_roles.send(game_data.get_faction_roles_name(args[1]))
    else:
        await added_roles.send(game_data.get_all_roles_name())


check_role = on_command("查看式神", priority=1, block=True)


@check_role.handle()
async def _(event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        if game_data.role_exist(args[1]):
            role_data: Role = game_data.get_role(args[1])
            role_str: str = game_data.trans_role_to_str(role=role_data)
            cards_str: str = game_data.trans_cards_to_str(cards=role_data.cards)
            await check_role.send(
                f"式神信息如下：\n{role_str}"
                f"\n\n卡牌信息如下："
                f"\n{cards_str}")
        else:
            await check_role.send("式神不存在")
    else:
        await check_role.send("式神名字呢？")


add_role = on_command("添加式神", rule=to_me(), permission=SUPERUSER, priority=1, block=True)


@add_role.got("name", prompt="请输入式神名字")
async def _(state: T_State):
    if game_data.role_exist(str(state['name'])):
        await add_role.finish(f"式神已存在，请直接修改式神")


@add_role.got("sex", prompt="请输入式神性别（不确定或无性别填无）")
@add_role.got("keywords", prompt="请输入式神关键词（用空格间隔开）")
@add_role.got("faction", prompt="请输入式神派系（红莲/紫岩/青岚/苍叶）")
@add_role.got("series", prompt="请输入式神系列（经典/不夜之火/月夜幻响/沧海刀鸣/吉运缘结/四相琉璃/善恶无明/繁花入梦/浮生方醒）")
@add_role.got("strength", prompt="请输入式神力量")
@add_role.got("hp", prompt="请输入式神血量")
@add_role.got("description", prompt="请输入式神本体描述")
async def _(state: T_State):
    role = Role(name=str(state['name']),
                sex=str(state['sex']),
                keywords=str(state['keywords']),
                faction=str(state['faction']),
                series=str(state['series']),
                strength=str(state['strength']),
                hp=str(state['hp']),
                description=str(state['description']),
                cards=[])
    game_data.add_role(role)
    await add_role.finish(message=f"式神已添加，信息如下：\n{game_data.trans_role_to_str(role=role)}")


modify_role = on_command("修改式神", rule=to_me(), permission=SUPERUSER, priority=1, block=True)


@modify_role.got("name", prompt="请输入式神名字")
async def _(state: T_State):
    role_name: str = str(state['name'])
    if not game_data.role_exist(role_name=role_name):
        await modify_role.finish(message=f"式神不存在，请先添加式神")
    else:
        role: Role = game_data.get_role(role_name=role_name)
        await modify_role.send(message=f"式神信息如下：\n{game_data.trans_role_to_str(role=role)}")


@modify_role.got("option", prompt="请问要修改哪一项（名字/性别/关键词/派系/系列/力量/血量/描述）")
@modify_role.got("new_data", prompt="请输入修改内容")
async def _(state: T_State):
    role_name: str = str(state['name'])
    option: str = str(state["option"])
    new_data: str = str(state["new_data"])
    options = dict(名字="name",
                   性别="sex",
                   关键词="keywords",
                   派系="faction",
                   系列="series",
                   力量="strength",
                   血量="hp",
                   描述="description")
    status: bool = game_data.modify_role_data(
        old_role_name=role_name,
        option=options[option],
        new_data=new_data)
    if status:
        if options[option] == "name":
            role: Role = game_data.get_role(role_name=new_data)
            await modify_role.finish(message=f"式神修改完成，信息如下：\n{game_data.trans_role_to_str(role=role)}")
        else:
            role: Role = game_data.get_role(role_name=role_name)
            await modify_role.finish(message=f"式神修改完成，信息如下：\n{game_data.trans_role_to_str(role=role)}")


add_card = on_command("添加卡牌", rule=to_me(), permission=SUPERUSER, priority=1, block=True)


@add_card.got("role_name", prompt="请输入式神名字")
async def _(state: T_State):
    role_name: str = str(state['role_name'])
    if not game_data.role_exist(role_name=role_name):
        await modify_role.finish(f"式神不存在，请先添加式神")


@add_card.got("card_name", prompt="请输入卡牌名字")
async def _(state: T_State):
    role_name: str = str(state['role_name'])
    card_name: str = str(state['card_name'])
    role = game_data.get_role(role_name=role_name)

    if game_data.card_exist(game_data.get_role_cards(role.name), card_name=card_name):
        await modify_role.finish(f"卡牌已存在，请直接修改")


@add_card.got("magatama", prompt="请输入卡牌勾次（1/2/3）")
@add_card.got("rarity", prompt="请输入卡牌稀有度（r，sr，ssr）")
@add_card.got("type", prompt="请输入卡牌类型（形态卡/法术卡/战斗卡/幻境卡）")
@add_card.got("strength", prompt="请输入力量改变值（没有则填0）")
@add_card.got("hp", prompt="请输入血量改变值（没有则填0）")
@add_card.got("armor", prompt="请输入护甲改变值（没有则填0）")
@add_card.got("description", prompt="请输入卡牌的卡面描述")
async def _(state: T_State):
    role_name: str = str(state['role_name'])
    card: Card = Card(name=str(state['card_name']),
                      magatama=str(state['magatama']),
                      rarity=str(state['rarity']),
                      type=str(state['type']),
                      strength=str(state['strength']),
                      hp=str(state['hp']),
                      armor=str(state['armor']),
                      description=str(state['description']))
    status = game_data.add_card(role_name=role_name, card=card)
    if status is True:
        await add_card.finish(f"添加成功，卡牌信息如下："
                              f"\n{game_data.trans_card_to_str(card=card)}")
    else:
        await add_card.finish("添加失败，式神名字错误或式神卡牌已满")


modify_card = on_command("修改卡牌", rule=to_me(), permission=SUPERUSER, priority=1, block=True)


@modify_card.got("role_name", prompt="请输入式神名字")
async def _(state: T_State):
    if not game_data.role_exist(str(state['role_name'])):
        await modify_card.finish(f"式神不存在，请先添加式神")
    else:
        cards = game_data.get_role_cards(str(state['role_name']))
        await modify_card.send(f"式神卡牌信息如下：\n{game_data.trans_cards_to_str(cards)}")


@modify_card.got("card_name", prompt="请输入卡牌名字")
async def _(state: T_State):
    role: Role = game_data.get_role(str(state['role_name']))
    if not game_data.card_exist(role.cards, str(state['card_name'])):
        await modify_card.finish(f"卡牌不存在，请先添加卡牌")


@modify_card.got("option", prompt="请问要修改哪一项（名字/勾次/稀有度/类型/力量/血量/护甲/描述）")
@modify_card.got("new_data", prompt="请输入修改内容")
async def _(state: T_State):
    options = dict(名字="name",
                   勾次="magatama",
                   稀有度="rarity",
                   类型="type",
                   力量="strength",
                   血量="hp",
                   护甲="armor",
                   描述="description")
    status: bool = game_data.modify_card_data(
        role_name=str(state['role_name']),
        old_card_name=str(state['card_name']),
        option=options[str(state["option"])],
        new_data=str(state['new_data']))
    if status:
        if options[str(state['option'])] == "name":
            card: Card = game_data.get_card(role_name=str(state['role_name']), card_name=str(state["new_data"]))
            await modify_card.finish(f"卡牌修改完成，信息如下：\n{game_data.trans_card_to_str(card)}")
        else:
            card: Card = game_data.get_card(role_name=str(state['role_name']), card_name=str(state['card_name']))
            await modify_card.finish(f"卡牌修改完成，信息如下：\n{game_data.trans_card_to_str(card)}")
