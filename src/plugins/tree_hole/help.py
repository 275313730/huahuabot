from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import PrivateMessageEvent


rule_str = str(f"欢迎加入树洞，以下为树洞的不完全使用指南："
               f"\n1.请勿发布任何违反法律的信息"
               f"\n2.目前小纸条只支持纯文字，请勿输入图片等其他内容（反正发了也不会生效），并保持小纸条字数在300字以内"
               f"\n3.bot全时间无人监管，如果遇到使用异常等情况，请使用反馈指令向开发者反馈"
               f"\n——最后，祝你使用愉快")

th_help = on_command("help 树洞", aliases={
    "帮助 树洞"}, rule=to_me(), priority=2, block=True)


@th_help.handle()
async def _(event: PrivateMessageEvent):
    await th_help.finish(str(f"树洞目前可以使用的功能有"
                             f"（请将UID改为小纸条编号）"
                             f"\n个人相关："
                             f"\n/加入树洞（必须先加入树洞，才可以使用其他指令哦）"
                             f"\n/修改昵称"
                             f"\n/我的小纸条"
                             f"\n/删除小纸条"
                             f"\n小纸条的投递与捡取："
                             f"\n/投递小纸条"
                             f"\n/捡取小纸条（已经捡取过的小纸条不会再重复捡取）"
                             f"\n小纸条收藏："
                             f"\n/收藏小纸条 UID"
                             f"\n/取消收藏小纸条 UID"
                             f"\n/我的收藏"
                             f"\n其他："
                             f"\n/举报小纸条（请不要恶意举报）"
                             f"\n/树洞规则"
                             f"\n注：1.以上功能只有私聊才有效"
                             f"\n2.为了方便操作，所有指令中的'小纸条'可以省略不输入"))

rule = on_command("树洞规则", rule=to_me(), priority=2, block=True)


@rule.handle()
async def _():
    await rule.finish(rule_str)
