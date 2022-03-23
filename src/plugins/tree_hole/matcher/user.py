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
    if user.check_nickname_exist(nickname):
        await add_user.reject("昵称已存在，请输入其他昵称")
    status = user.join_tree_hole(qq=qq, nickname=nickname)
    if status:
        rule_str = str(f"欢迎加入树洞，以下为树洞的一些规则："
                       f"\n1.请勿发布任何违反法律的信息"
                       f"\n2.目前小纸条只支持纯文字，请勿输入图片等其他内容（反正发了也不会生效），并保持小纸条字数在300字以内"
                       f"\n3.bot全时间无人监控，如果遇到使用异常等情况，请使用反馈指令向开发者反馈"
                       f"\n——最后，祝你使用愉快")

        await add_user.finish(rule_str)

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
