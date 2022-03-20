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
        rule_str = f"在加入树洞之前，希望你能认真阅读并严格遵守以下规则" \
                   f"\n风控类规则：" \
                   f"\nA类（违反将会永久封禁账号）" \
                   f"\n1.反对宪法所确定的基本原则的" \
                   f"\n2.危害国家安全，泄露国家秘密，颠覆国家政权，破坏国家统一的" \
                   f"\n3.损害国家荣誉和利益的" \
                   f"\n4.煽动民族仇恨、民族歧视，破坏民族团结的" \
                   f"\n5.破坏国家宗教政策，宣扬邪教和封建迷信的" \
                   f"\n6.散布谣言，扰乱社会秩序，破坏社会稳定的" \
                   f"\n7.散布淫秽、色情、赌博、暴力、凶杀、恐怖或者教唆犯罪的" \
                   f"\n8.侮辱或者诽谤他人，侵害他人合法权益的" \
                   f"\n9.含有法律、行政法规禁止的其他内容的" \
                   f"\n" \
                   f"\nB类（违反将会封禁账号一段时间，据情节严重而定）" \
                   f"\n1.泄漏他人隐私" \
                   f"\n2.恶意冒充他人" \
                   f"\n3.人身攻击" \
                   f"\n4.垃圾内容（无意义的标点符号，重复发布相同内容等行为）" \
                   f"\n5.广告、诱导信息等" \
                   f"\n" \
                   f"\n如果你在使用过程中发现以上行为，请及时使用'/举报用户'或'/举报小纸条'的指令进行举报" \
                   f"\n" \
                   f"\n一般类规则" \
                   f"\n小纸条：" \
                   f"\n1.投递小纸条时，请不要发送除文字外的其他消息，包括表情、图片和视频等，并保持小纸条字数在140字以内" \
                   f"\n2."

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
