from nonebot.internal.matcher import Matcher, matchers
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.message import run_preprocessor

from ..handle import user

ignore_cmds = ['/help', '/帮助', '/加入树洞']


@run_preprocessor
async def _(matcher: Matcher, event: PrivateMessageEvent):
    # 识别树洞matcher
    if matcher.plugin_name and not matcher.plugin_name.startswith("tree_hole"):
        return

    # 忽略特殊指令
    args = str(event.get_message()).split(" ")
    if args[0] in ignore_cmds:
        return

    # 检查用户状态
    qq = event.user_id
    exist = user.check_qq_exist(qq)
    ban = user.check_qq_ban(qq)
    if not exist:
        await matcher.finish("加入树洞才能使用其他指令哦")
    if ban:
        await matcher.finish("账号封禁中，如有疑问可以通过'/反馈树洞'提交意见")
    user.update_last_use_time(qq)
