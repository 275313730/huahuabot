from nonebot import on_command
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State
from ...config import TREE_HOLE_PRIORITY
from ..handle import user, admin, note

ban_user = on_command("禁用用户", rule=to_me(), priority=TREE_HOLE_PRIORITY,
                      block=True, permission=SUPERUSER)


@ban_user.got("qq", prompt="请输入用户qq")
async def _(state: T_State):
    qq = int(str(state['qq']))

    exist = user.check_qq_exist(qq)
    if not exist:
        await ban_user.finish("用户不存在")


@ban_user.got("ban_end", prompt="请输入禁用结束时间(yyyy/mm/dd)")
async def _(state: T_State):
    qq = int(str(state['qq']))
    ban_end = str(state['ban_end'])

    status = admin.ban_qq(qq, ban_end)
    if status:
        await ban_user.finish("禁用成功")
    else:
        await ban_user.finish("禁用失败")


check_note_reports = on_command(
    "查看举报", rule=to_me(), priority=TREE_HOLE_PRIORITY, block=True, permission=SUPERUSER)


@check_note_reports.handle()
async def _(event: PrivateMessageEvent):
    args = str(event.get_message()).split(" ")
    if len(args) < 2:
        await check_note_reports.finish("小纸条编号没有填写哦")

    uid = int(str(args[1]))

    if not note.check_note_exist(uid):
        await check_note_reports.finish("小纸条不存在")

    report_str = note.get_note_reports_by_uid(uid)
    await check_note_reports.finish(report_str)
