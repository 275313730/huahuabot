from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.typing import T_State

from ..handle import user

add_user = on_command("加入树洞", rule=to_me(), priority=2, block=True)


@add_user.handle()
async def _(event: PrivateMessageEvent):
    exist = user.check_qq_exist(event.user_id)
    if exist:
        await add_user.finish("你已经加入树洞啦，请勿重复操作哦")


@add_user.got("nickname", prompt="输入你的树洞昵称")
async def _(state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    nickname = str(state['nickname'])

    status = user.join_tree_hole(qq=qq, nickname=nickname)
    if status:
        user.update_last_use_time(qq)
        await add_user.finish("欢迎加入树洞")
    else:
        await add_user.finish("加入树洞失败")


modify_nickname = on_command("修改昵称", rule=to_me(), priority=2, block=True)


@modify_nickname.got("nickname", prompt="请输入要修改的昵称")
async def _(state: T_State, event: PrivateMessageEvent):
    qq = event.user_id
    nickname = str(state['nickname'])

    if user.check_nickname_exist(nickname):
        await add_user.reject("昵称已存在，请重新修改")
    status = user.modify_nickname(qq, nickname)
    if status:
        await add_user.finish("修改成功")
    else:
        await add_user.finish("修改失败")
