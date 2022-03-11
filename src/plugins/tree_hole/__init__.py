import nonebot
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Event
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.typing import T_State

from . import tree_hole

# 帮助相关

_help = on_command("help", aliases={"帮助"}, priority=1, block=True)


@_help.handle()
async def _():
    await _help.finish(f"这里是树洞bot，目前可以使用的功能有（只有私聊才有效）："
                       f"\n/加入树洞：必须先加入树洞，才可以使用其他指令哦"
                       f"\n/投递小纸条：根据指示投递小纸条到树洞中"
                       f"\n/捡个小纸条：随机捡取一张别人投递的小纸条"
                       f"\n/我的小纸条：查看自己投递过的小纸条"
                       f"\n/删除小纸条：删除一条自己投递过的小纸条"
                       f"\n/举报小纸条：遇到违反规则的小纸条请及时举报哦（请不要恶意举报）")


# 管理相关

ban_user = on_command("禁用用户", rule=to_me(), priority=1, block=True, permission=SUPERUSER)


@ban_user.got("qq", prompt="请输入用户qq")
async def _(state: T_State):
    qq = int(str(state['qq']))

    exist = tree_hole.check_qq_exist(qq)
    if not exist:
        await ban_user.finish("用户不存在")


@ban_user.got("ban_end", prompt="请输入禁用结束时间(yyyy/mm/dd)")
async def _(state: T_State):
    qq = int(str(state['qq']))
    ban_end = str(state['ban_end'])

    status = tree_hole.ban_qq(qq, ban_end)
    if status:
        await ban_user.finish("禁用成功")
    else:
        await ban_user.finish("禁用失败")


# 用户相关

add_user = on_command("加入树洞", rule=to_me(), priority=2, block=True)


@add_user.handle()
async def _(event: PrivateMessageEvent):
    exist = tree_hole.check_qq_exist(event.user_id)
    if exist:
        await add_user.finish("你已经加入树洞啦，请勿重复操作哦")


@add_user.got("nickname", prompt="输入你的树洞昵称")
async def _(state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    nickname = str(state['nickname'])

    status = tree_hole.join_tree_hole(qq=qq, nickname=nickname)
    if status:
        tree_hole.update_last_use_time(qq)
        await add_user.finish("欢迎加入树洞")
    else:
        await add_user.finish("加入树洞失败")


# 小纸条相关

add_note = on_command("投递小纸条", rule=to_me(), priority=2, block=True)


@add_note.handle()
async def _(event: PrivateMessageEvent):
    exist = tree_hole.check_qq_exist(event.user_id)
    if not exist:
        await add_note.finish("加入树洞才能投递小纸条哦")


@add_note.got("content", prompt="随便写点什么都可以哦（目前只支持纯文字消息，请勿发送表情和图片等其他内容）")
async def _(state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    content = str(state['content'])

    tree_hole.update_last_use_time(qq)
    status = tree_hole.post_note(qq=qq, content=content)
    if status:
        await add_note.finish("小纸条已投递")
    else:
        await add_note.finish("小纸条投递失败")


random_note = on_command("捡个小纸条", rule=to_me(), priority=2, block=True)


@random_note.handle()
async def _(event: PrivateMessageEvent):
    qq = event.user_id

    tree_hole.update_last_use_time(qq)
    exist = tree_hole.check_qq_exist(qq)
    if exist:
        note_str = tree_hole.get_random_note(qq)
        if note_str != "":
            await random_note.finish(note_str)
        else:
            await random_note.finish("暂无小纸条")
    else:
        await random_note.finish("加入树洞才能看到别人的小纸条哦")


my_notes = on_command("我的小纸条", rule=to_me(), priority=2, block=True)


@my_notes.handle()
async def _(event: PrivateMessageEvent):
    qq = event.user_id
    exist = tree_hole.check_qq_exist(qq)
    if not exist:
        await random_note.finish("你还没有加入树洞呢")


@my_notes.handle()
async def _(event: PrivateMessageEvent):
    qq = event.user_id

    tree_hole.update_last_use_time(qq)
    note_str = tree_hole.get_my_notes(qq)
    if note_str != "":
        await random_note.finish(note_str)
    else:
        await random_note.finish("暂无小纸条")


delete_note = on_command("删除小纸条", rule=to_me(), priority=2, block=True)


@delete_note.handle()
async def _(event: PrivateMessageEvent):
    qq = event.user_id
    exist = tree_hole.check_qq_exist(qq)
    if not exist:
        await delete_note.finish("你还没有加入树洞呢")


@delete_note.got("uid", prompt="请输入小纸条编号")
async def _(state: T_State, event: PrivateMessageEvent):
    uid = int(str(state['uid']))
    if not tree_hole.check_note_exist(uid):
        await delete_note.finish("编号错误")
    qq = tree_hole.get_qq_by_note(uid)
    if qq != str(event.user_id):
        pass
    note_str = tree_hole.get_note_by_uid(uid)
    await delete_note.send(f"你选择的小纸条内容如下："
                           f"\n{note_str}")


@delete_note.got("confirm", prompt="如确认删除，请再次输入小纸条编号")
async def _(state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    uid = int(str(state['uid']))
    confirm = int(str(state['uid']))
    if uid == confirm:
        tree_hole.delete_note(qq, uid)


report_note = on_command("举报小纸条", rule=to_me(), priority=2, block=True)


@report_note.handle()
async def _(event: PrivateMessageEvent):
    exist = tree_hole.check_qq_exist(event.user_id)
    if not exist:
        await report_note.finish("请加入树洞后再使用其他命令")


@report_note.got("uid", prompt="请输入小纸条编号")
async def _(state: T_State):
    uid = int(str(state['uid']))
    if not tree_hole.check_note_exist(uid):
        await report_note.finish("编号错误")


@report_note.got("description", prompt="请输入具体描述")
async def _(bot: nonebot.adapters.onebot.v11.Bot, state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    uid = int(str(state['uid']))
    description = str(state['description'])

    tree_hole.update_last_use_time(qq)
    status = tree_hole.report_note(qq, uid, description)
    if status:
        note_str = tree_hole.get_note_by_uid(uid)
        qq = tree_hole.get_qq_by_note(uid)
        await bot.send_private_msg(user_id=275313730, message=f"叮咚！有一个小纸条被举报"
                                                              f"\n被举报人qq：{qq}"
                                                              f"\n{note_str}"
                                                              f"\n--------------------"
                                                              f"\n举报人qq：{qq}"
                                                              f"\n举报描述：{description}")
        await report_note.finish("举报成功")
    else:
        await report_note.finish("举报失败")
