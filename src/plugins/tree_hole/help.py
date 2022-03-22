from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import PrivateMessageEvent

_help = on_command("help 树洞", aliases={
    "帮助 树洞"}, rule=to_me(), priority=2, block=True)


@_help.handle()
async def _(event: PrivateMessageEvent):
    await _help.finish(f"树洞目前可以使用的功能有"
                       f"（请将UID改为小纸条编号）"
                       f"\n个人相关："
                       f"\n/加入树洞（必须先加入树洞，才可以使用其他指令哦）"
                       f"\n/修改昵称"
                       f"\n/我的小纸条"
                       f"\n/删除小纸条"
                       f"\n"
                       f"\n小纸条的投递与捡取："
                       f"\n/投递小纸条"
                       f"\n/捡取小纸条（已经捡取过的小纸条不会再重复捡取）"
                       f"\n"
                       f"\n小纸条收藏："
                       f"\n/收藏小纸条 UID"
                       f"\n/取消收藏小纸条 UID"
                       f"\n/我的收藏"
                       f"\n"
                       f"\n其他："
                       f"\n/举报小纸条（请不要恶意举报）"
                       f"\n/树洞规则"
                       f"\n"
                       f"\n注：1.以上功能只有私聊才有效"
                       f"\n2.为了方便操作，所有指令中的'小纸条'可以省略不输入")

rule = on_command("树洞规则", rule=to_me(), priority=2, block=True)


@rule.handle()
async def _():
    rule_str = str(f"欢迎加入树洞，在你正式使用树洞之前，希望你能认真阅读并严格遵守以下规则"
                   f"\n风控类规则："
                   f"\n（违反将会根据实际情况封禁账号一段时间）"
                   f"\n1.违反国家法律规定"
                   f"\n2.色情，暴力，血腥等不合规内容"
                   f"\n3.泄漏他人隐私/恶意冒充他人/人身攻击等侵害他人权利的行为"
                   f"\n4.垃圾内容（无意义的标点符号，重复发布相同内容等行为）"
                   f"\n5.广告、诱导信息等"
                   f"\n注：如果你在使用过程中发现其他人存在以上行为，请及时使用举报指令进行举报"
                   f"\n"
                   f"\n一般类规则："
                   f"\n1.投递小纸条时，请不要发送除文字外的其他消息，包括表情、图片和视频等，并保持小纸条字数在300字以内"
                   f"\n2.bot全时间无人监控，如果遇到使用异常等情况，请使用反馈指令向开发者反馈"
                   f"\n"
                   f"\n最后，祝你使用愉快")

    await rule.finish(rule_str)
