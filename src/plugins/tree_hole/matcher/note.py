import nonebot.adapters.onebot.v11.bot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.typing import T_State

from ..handle import user, note

add_note = on_command("投递小纸条", rule=to_me(), priority=2, block=True)


@add_note.handle()
async def _(event: PrivateMessageEvent):
    qq = event.user_id
    exist = user.check_qq_exist(qq)
    ban = user.check_qq_ban(qq)
    if not exist:
        await add_note.finish("加入树洞才能投递小纸条哦")
    if ban:
        await add_note.finish("账号封禁中，如有疑问可以通过'/反馈树洞'提交意见")


@add_note.got("content", prompt="随便写点什么都可以哦（目前只支持纯文字消息，请勿发送表情和图片等其他内容）")
async def _(state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    content = str(state['content'])

    user.update_last_use_time(qq)
    status = note.post_note(qq=qq, content=content)
    if status:
        await add_note.finish("小纸条已投递")
    else:
        await add_note.finish("小纸条投递失败")


random_note = on_command("捡个小纸条", rule=to_me(), priority=2, block=True)


@random_note.handle()
async def _(event: PrivateMessageEvent):
    qq = event.user_id

    user.update_last_use_time(qq)
    exist = user.check_qq_exist(qq)
    if exist:
        note_str = note.get_random_note(qq)
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
    exist = user.check_qq_exist(qq)
    if not exist:
        await random_note.finish("你还没有加入树洞呢")


@my_notes.handle()
async def _(event: PrivateMessageEvent):
    qq = event.user_id

    user.update_last_use_time(qq)
    note_str = note.get_my_notes(qq)
    if note_str != "":
        await random_note.finish(note_str)
    else:
        await random_note.finish("暂无小纸条")


delete_note = on_command("删除小纸条", rule=to_me(), priority=2, block=True)


@delete_note.handle()
async def _(event: PrivateMessageEvent):
    qq = event.user_id
    exist = user.check_qq_exist(qq)
    if not exist:
        await delete_note.finish("你还没有加入树洞呢")


@delete_note.got("uid", prompt="请输入小纸条编号")
async def _(state: T_State, event: PrivateMessageEvent):
    uid = int(str(state['uid']))
    if not note.check_note_exist(uid):
        await delete_note.finish("编号错误")
    qq = user.get_qq_by_note(uid)
    if qq != str(event.user_id):
        pass
    note_str = note.get_note_by_uid(uid)
    await delete_note.send(f"你选择的小纸条内容如下："
                           f"\n{note_str}")


@delete_note.got("confirm", prompt="如确认删除，请再次输入小纸条编号")
async def _(state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    uid = int(str(state['uid']))
    confirm = int(str(state['uid']))
    if uid == confirm:
        note.delete_note(qq, uid)


report_note = on_command("举报小纸条", rule=to_me(), priority=2, block=True)


@report_note.handle()
async def _(event: PrivateMessageEvent):
    exist = user.check_qq_exist(event.user_id)
    if not exist:
        await report_note.finish("请加入树洞后再使用其他命令")


@report_note.got("uid", prompt="请输入小纸条编号")
async def _(state: T_State):
    uid = int(str(state['uid']))
    if not note.check_note_exist(uid):
        await report_note.finish("编号错误")


@report_note.got("description", prompt="请输入具体描述")
async def _(bot: nonebot.adapters.onebot.v11.Bot, state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    uid = int(str(state['uid']))
    description = str(state['description'])

    user.update_last_use_time(qq)
    status = note.report_note(qq, uid, description)
    if status:
        note_str = note.get_note_by_uid(uid)
        qq = user.get_qq_by_note(uid)
        await bot.send_private_msg(user_id=275313730, message=f"叮咚！有一个小纸条被举报"
                                                              f"\n被举报人qq：{qq}"
                                                              f"\n{note_str}"
                                                              f"\n--------------------"
                                                              f"\n举报人qq：{qq}"
                                                              f"\n举报描述：{description}")
        await report_note.finish("举报成功")
    else:
        await report_note.finish("举报失败")
