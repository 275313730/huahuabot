from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Event
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.typing import T_State

from . import tree_hole

delete_notes = on_command("清除树洞数据", rule=to_me(), priority=1, block=True)


@delete_notes.got("confirm", prompt="请输入'确认清除'以确认操作")
async def _(state: T_State):
    confirm = str(state['confirm'])
    pass


add_user = on_command("加入树洞", rule=to_me(), priority=1, block=True)


@add_user.handle()
async def _(event: PrivateMessageEvent):
    exist = tree_hole.check_qq_exist(str(event.user_id))
    if exist:
        await add_user.finish("你已经加入树洞啦，请勿重复操作哦")


@add_user.got("nickname", prompt="输入你的树洞昵称")
async def _(state: T_State, event: PrivateMessageEvent):
    nickname = str(state['nickname'])
    tree_hole.add_user(qq=str(event.user_id), nickname=nickname)
    await add_user.finish("欢迎加入树洞")


add_note = on_command("投递小纸条", rule=to_me(), priority=1, block=True)


@add_note.handle()
async def _(event: PrivateMessageEvent):
    exist = tree_hole.check_qq_exist(str(event.user_id))
    if not exist:
        await add_note.finish("加入树洞才能投递小纸条哦")


@add_note.got("content", prompt="随便写点什么都可以哦（目前只支持纯文字消息，请勿发送表情和图片等其他内容）")
async def _(state: T_State, event: PrivateMessageEvent):
    content = str(state['content'])
    status = tree_hole.add_note(qq=str(event.user_id), content=content)
    if status:
        await add_note.finish("小纸条已投递")
    else:
        await add_note.finish("小纸条投递失败")


random_note = on_command("捡个小纸条", rule=to_me(), priority=2, block=True)


@random_note.handle()
async def _(state: T_State, event: PrivateMessageEvent):
    exist = tree_hole.check_qq_exist(str(event.user_id))
    if exist:
        note_str = tree_hole.get_random_note(str(event.user_id))
        if note_str != "":
            await random_note.finish(note_str)
        else:
            await random_note.finish("暂无小纸条")
    else:
        await random_note.finish("加入树洞才能看到别人的小纸条哦")


my_notes = on_command("我的小纸条", rule=to_me(), priority=2, block=True)


@my_notes.handle()
async def _(event: PrivateMessageEvent):
    exist = tree_hole.check_qq_exist(str(event.user_id))
    if exist:
        note_str = tree_hole.get_my_notes(str(event.user_id))
        if note_str != "":
            await random_note.finish(note_str)
        else:
            await random_note.finish("暂无小纸条")
    else:
        await random_note.finish("你还没有加入树洞呢")
