from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State

from ..handle import user, admin

# 管理相关

ban_user = on_command("禁用用户", rule=to_me(), priority=1, block=True, permission=SUPERUSER)


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


