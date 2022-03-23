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
        rule_str = str(f"欢迎加入树洞，在你正式使用树洞之前，希望你能认真阅读并严格遵守以下规则"
                       f"\n风控类规则："
                       f"\n（违反将会根据实际情况封禁账号一段时间）"
                       f"\n1.违反国家法律规定"
                       f"\n2.色情，暴力，血腥等不合规内容"
                       f"\n3.泄漏他人隐私/恶意冒充他人/人身攻击等侵害他人权利的行为"
                       f"\n4.垃圾内容（无意义的标点符号，重复发布相同内容等行为）"
                       f"\n5.广告、诱导信息等"
                       f"\n注：如果你在使用过程中发现其他人存在以上行为，请及时使用举报指令进行举报"
                       f"\n一般类规则："
                       f"\n1.投递小纸条时，请不要发送除文字外的其他消息，包括表情、图片和视频等，并保持小纸条字数在300字以内"
                       f"\n2.bot全时间无人监控，如果遇到使用异常等情况，请使用反馈指令向开发者反馈"
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
